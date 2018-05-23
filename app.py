import os
import json
import csv
import shutil

import MySQLdb
from flask import Flask, request
from web.forms.RunForm import RunForm
from neuro.learn_neural_network import learn_neural_network
from neuro.predict_order import predict_order
from flask_mysqldb import MySQL
from neuro.load_data import transform_data
from flask import jsonify

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'food')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'food')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'food')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_PORT'] = os.getenv('MYSQL_PORT', 3306)

mysql.init_app(app)

food_feature_path = os.getcwd() + '/data/food_features.csv'
chance_and_price_path = os.getcwd() + '/data/chance_and_price.csv'
menu_items_path = os.getcwd() + '/data/menu_items.csv'
orders_path = os.getcwd() + '/data/orders.csv'


@app.route('/')
def hello():
    return 'Hello Neurofood!'


@app.route('/run', methods=['POST'])
def run():
    form = RunForm(data=request.get_json())

    if not form.validate():
        return json.dumps(form.errors)

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT menu_item.id, dish.food_id FROM menu_item JOIN dish ON menu_item.dish_id = dish.id "
                   "WHERE dish.food_id IS NOT NULL AND menu_item.menu_id = (SELECT max(id) FROM menu) "
                   "and  menu_item.day_of_week = " + str(form.day_of_week.data) + " ORDER BY menu_item.day_of_week ASC;")

    result = predict_order(food_feature_path, chance_and_price_path, transform_data(cursor.fetchall()), form.user_id.data)

    return jsonify(serialize(result.tolist()))


def serialize(data):
    res = {}
    for item in data:
        res[int(item[0])] = item[1]
    return res


@app.cli.command()
def train():
    fetch_from_database_to_csv()
    learn_neural_network(food_feature_path, chance_and_price_path, menu_items_path, orders_path)

    return


def fetch_from_database_to_csv():
    shutil.rmtree(food_feature_path)
    shutil.rmtree(chance_and_price_path)
    shutil.rmtree(menu_items_path)
    shutil.rmtree(orders_path)

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT food_id, feature_id FROM food_feature;")
    write_to_csv(food_feature_path, cursor.fetchall())

    cursor.execute("SELECT food.id, count(menu_item.id)/(SELECT count(*) FROM "
                   "(select distinct menu_id, day_of_week from menu_item) mi), IFNULL(sum(menu_item.price)/count(menu_item.id), 0) from food "
                   "LEFT JOIN dish on dish.food_id = food.id LEFT JOIN menu_item on menu_item.dish_id = dish.id "
                   "group by food.id order by food.id ASC")
    write_to_csv(chance_and_price_path, cursor.fetchall())

    cursor.execute(
        "SELECT mi.id, food_id FROM `menu_item` mi LEFT JOIN dish d ON mi.dish_id = d.id WHERE d.food_id IS NOT NULL")
    write_to_csv(menu_items_path, cursor.fetchall())

    cursor.execute("SELECT menu_item_id, food_id, user_id FROM `order_line` ol "
                   "LEFT JOIN menu_item mi ON ol.menu_item_id = mi.id LEFT JOIN dish d ON mi.dish_id = d.id "
                   "WHERE food_id IS NOT NULL ORDER BY user_id ASC")
    write_to_csv(orders_path, cursor.fetchall())

    return


def write_to_csv(file_path, results):
    with open(file_path, 'w') as out:
        csv_out = csv.writer(out)
        for row in results:
            csv_out.writerow(row)
        return

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 80.
    port = int(os.environ.get('PORT', os.getenv('CONTAINER_FLASK_PORT', 80)))
    app.run(host='0.0.0.0', port=port, debug=True)
