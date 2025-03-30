#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakes = [bake.to_dict() for bake in Bakery.query.all()]
    return make_response(jsonify(bakes), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bake = Bakery.query.get(id)

    if not bake:
        return make_response(jsonify({"error": "Bakery not found"}), 404)

    return make_response(jsonify(bake.to_dict(rules=("-baked_goods.bakery",))), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    by_price = [bake.to_dict() for bake in BakedGood.query.order_by(BakedGood.price.desc()).all()]
    return make_response(jsonify(by_price), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if not most_expensive:
        return make_response(jsonify({"error": "No baked goods found"}), 404)

    return make_response(jsonify(most_expensive.to_dict()), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
