from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Scene(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_path = db.Column(db.String(255), nullable=False)
    fromdate = db.Column(db.String(10), nullable=False)
    todate = db.Column(db.String(10), nullable=False)
    cash = db.Column(db.Float, nullable=False)
    strategies = db.Column(db.JSON, nullable=False)

    def __init__(self, data_path, fromdate, todate, cash, strategies):
        self.data_path = data_path
        self.fromdate = fromdate
        self.todate = todate
        self.cash = cash
        self.strategies = strategies

class BacktestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scene_id = db.Column(db.Integer, db.ForeignKey('scene.id', ondelete='CASCADE'), nullable=False)
    strategy_name = db.Column(db.String(255))
    symbol = db.Column(db.String(10))
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    total_return = db.Column(db.Float)
    trades = db.Column(db.Integer)
    winning_trades = db.Column(db.Integer)
    losing_trades = db.Column(db.Integer)
    max_drawdown = db.Column(db.Float)
    sharpe_ratio = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'scene_id': self.scene_id,
            'strategy_name': self.strategy_name,
            'symbol': self.symbol,
            'from_date': self.from_date.strftime('%Y-%m-%d'),
            'to_date': self.to_date.strftime('%Y-%m-%d'),
            'total_return': self.total_return,
            'trades': self.trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'max_drawdown': self.max_drawdown,
            'sharpe_ratio': self.sharpe_ratio
        }
