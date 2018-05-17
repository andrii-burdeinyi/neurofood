import os
import json
import csv

from flask import Flask, request
from web.forms.RunForm import RunForm
from neuro import learn_neural_network
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'food')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'food')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'food')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_PORT'] = os.getenv('MYSQL_PORT', 3306)

mysql.init_app(app)

@app.route('/')
def hello():
    return 'Hello Neurofood!'

@app.route('/run', methods=['POST'])
def run():
    form = RunForm(data=request.get_json())
    if not form.validate():
        return json.dumps(form.errors)
    return 'Neiurofood has been run'


@app.cli.command()
def train():
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT mi.id, food_id from `menu_item` mi LEFT JOIN dish d on mi.dish_id = d.id")
    menu_items_path = os.getcwd() + '/data/menu_items.csv'
    write_to_csv(menu_items_path, cursor.fetchall())

    cursor.execute("SELECT menu_item_id, food_id, user_id from `order_line` ol LEFT JOIN menu_item mi on ol.menu_item_id = mi.id LEFT JOIN dish d on mi.dish_id = d.id")
    orders_path = os.getcwd() + '/data/orders.csv'
    write_to_csv(orders_path, cursor.fetchall())

    # TODO: write sql query for generating features csv
    # cursor.execute("")
    # features_path = os.getcwd() + '/data/features.csv'
    # write_to_csv(features_path, cursor.fetchall())

    # TODO: call learn_neural_network func to train network
    #learn_neural_network('', menu_items_path, orders_path, None)

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
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', True))
