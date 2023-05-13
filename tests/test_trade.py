import pytest
from src.custom_exceptions import (
    InvalidTradeIndicatorError,
    InvalidStockQuantityError,
    InvalidStockPriceError,
)
from src.gbc_exchange import CommonStock, TradeIndicator
from datetime import datetime, timedelta


def test_record_trade_invalid_indicator(invalid_trade_indicator):
    with pytest.raises(InvalidTradeIndicatorError):
        common_stock = CommonStock("TEA", 0.0, 100)
        common_stock.record_trade(10, invalid_trade_indicator, 50)


def test_record_trade_valid():
    stock = CommonStock("TEA", 0.0, 100)
    stock.record_trade(100, "BUY", 50)
    assert len(stock.trades) == 1
    assert stock.trades[0]["quantity"] == 100
    assert stock.trades[0]["buy_sell_indicator"] == TradeIndicator.BUY
    assert stock.trades[0]["price"] == 50


def test_record_trade_invalid_quantity():
    stock = CommonStock("TEA", 0, 100)
    with pytest.raises(InvalidStockQuantityError):
        stock.record_trade(0, "SELL", 50)


def test_record_trade_invalid_price():
    stock = CommonStock("TEA", 0.0, 100)
    with pytest.raises(InvalidStockPriceError):
        stock.record_trade(100, "BUY", 0)


def test_record_trade_last_5_min():
    stock = CommonStock("TEA", 0, 100)
    current_time = datetime.now()
    trade_time = current_time - timedelta(minutes=4)
    stock.trades = [
        {
            "timestamp": trade_time,
            "quantity": 100,
            "buy_sell_indicator": TradeIndicator.BUY,
            "price": 50.0,
        },
        {
            "timestamp": trade_time,
            "quantity": 50,
            "buy_sell_indicator": TradeIndicator.SELL,
            "price": 60.0,
        },
    ]
    assert stock.calc_vol_weighted_stock_price_last_5_mins() == 53.333
