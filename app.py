import os
import json
import csv
import requests

from flask import Flask, request
from web.forms.RunForm import RunForm
from neuro.learn_neural_network import learn_neural_network
from neuro.predict_order import predict_order
from flask import jsonify
import datetime

app = Flask(__name__)

# API secret
api_secret = os.getenv('API_SECRET', 'food2017')

# API URLs
foods_features_api_url = 'https://api.food.dev.norse.digital/neurofood/features'
chances_and_prices_api_url = 'https://api.food.dev.norse.digital/neurofood/prices'
menu_items_api_url = 'https://api.food.dev.norse.digital/neurofood/menuitems'
orders_api_url = 'https://api.food.dev.norse.digital/neurofood/orders'
new_menu_items_api_url = 'https://api.food.dev.norse.digital/neurofood/new/menuitems'


@app.route('/')
def hello():
    return 'Hello Neurofood!'


@app.route('/run', methods=['POST'])
def run():
    form = RunForm(data=request.get_json())

    if not form.validate():
        return jsonify(form.day_of_week)

    new_orders = json.loads(requests.get(
        url=new_menu_items_api_url,
        params={"day_of_week": str(form.day_of_week.data)},
        headers={"secret": api_secret}
    ).text)

    food_features = json.loads(requests.get(
        url=foods_features_api_url,
        headers={"secret": api_secret}
    ).text)

    chance_and_prices = json.loads(requests.get(
        url=chances_and_prices_api_url,
        headers={"secret": api_secret}
    ).text)

    result = predict_order(food_features, chance_and_prices, new_orders, form.user_id.data)

    return jsonify(serialize(result.tolist()))


def serialize(data):
    res = {}
    for item in data:
        res[int(item[0])] = item[1]
    return res


@app.cli.command()
def train():
    print("Starting training : ")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    foods_features = json.loads(requests.get(
        url=foods_features_api_url,
        headers={"secret": api_secret}
    ).text)

    chances_and_prices = json.loads(requests.get(
        url=chances_and_prices_api_url,
        headers={"secret": api_secret}
    ).text)

    menu_items = json.loads(requests.get(
        url=menu_items_api_url,
        headers={"secret": api_secret}
    ).text)

    orders = json.loads(requests.get(
        url=orders_api_url,
        headers={"secret": api_secret}
    ).text)

    learn_neural_network(foods_features, chances_and_prices, menu_items, orders)

    print("Training is finished : ")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return


def write_to_csv(file_path, results):
    with open(file_path, 'w') as out:
        csv_out = csv.writer(out)
        for row in results:
            csv_out.writerow(row)
        return


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 80.
    port = int(os.environ.get('PORT', os.getenv('CONTAINER_FLASK_PORT', 5000)))
    app.run(host='0.0.0.0', port=5000, debug=True)
