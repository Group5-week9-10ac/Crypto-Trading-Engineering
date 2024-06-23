from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BacktestResult(Base):
    __tablename__ = 'backtest_results'

    id = Column(Integer, primary_key=True)
    strategy_name = Column(String)
    symbol = Column(String)
    from_date = Column(DateTime)
    to_date = Column(DateTime)
    total_return = Column(Float)
    trades = Column(Integer)
    winning_trades = Column(Integer)
    losing_trades = Column(Integer)
    max_drawdown = Column(Float)
    sharpe_ratio = Column(Float)
