import pytest
from src.gbc_exchange import CommonStock, PreferredStock, GBCExchange


@pytest.fixture
def invalid_trade_indicator():
    return "INVALID"


@pytest.fixture
def invalid_price():
    return -1


@pytest.fixture
def common_stock(stock_symbol, last_dividend, par_value):
    return CommonStock(stock_symbol, last_dividend, par_value)


@pytest.fixture
def preferred_stock(stock_symbol, last_dividend, par_value, fixed_dividend):
    return PreferredStock(stock_symbol, last_dividend, par_value, fixed_dividend)


@pytest.fixture
def gbce_exchange():
    gbce = GBCExchange()
    gbce.add_stock(CommonStock("TEA", 0, 100))
    gbce.add_stock(CommonStock("POP", 8, 100))
    gbce.add_stock(CommonStock("ALE", 23, 60))
    gbce.add_stock(PreferredStock("GIN", 8, 2, 100))
    gbce.add_stock(CommonStock("JOE", 13, 250))
    return gbce
