import json
from datetime import datetime
from flask import Flask
from flask_app.models import db, Scene
from flask_app.config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Musy19@localhost:5432/wk9_trade_crypto'
db.init_app(app)

def load_scenes_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        scenes = []
        for strategy in data['strategies']:
            scene = Scene(
                data_path=data['data_path'],
                fromdate=data['fromdate'],
                todate=data['todate'],
                cash=data['cash'],
                strategies=[{
                    'name': strategy['name'],
                    'params': strategy['params']
                }]
            )
            scenes.append(scene)
        return scenes

with app.app_context():
    scenes = load_scenes_from_json('/home/moraa/Documents/10_academy/Week-9/Crypto-Trading-Engineering/MLOps/backend/backtest/backtest_config.json')
    for scene in scenes:
        db.session.add(scene)
    db.session.commit()