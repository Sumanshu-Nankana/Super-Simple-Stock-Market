import pytest
from src.custom_exceptions import InvalidStockPriceError
from src.gbc_exchange import CommonStock, PreferredStock


@pytest.mark.parametrize(
    "stock_symbol, last_dividend, par_value",
    [("TEA", 0, 100), ("POP", 8, 100), ("ALE", 23, 60), ("JOE", 13, 250)],
)
def test_dividend_yield_valid_price_common_stock(
    common_stock, stock_symbol, last_dividend, par_value
):
    assert common_stock.calc_dividend_yield(110) == last_dividend / 110


def test_dividend_yield_invalid_price_common_stock(invalid_price):
    with pytest.raises(InvalidStockPriceError):
        common_stock = CommonStock("TEA", 0, 100)
        common_stock.calc_dividend_yield(invalid_price)


@pytest.mark.parametrize(
    "stock_symbol, last_dividend, par_value, fixed_dividend", [("GIN", 8, 100, 0.02)]
)
def test_dividend_yield_valid_price_preferred_stock(
    preferred_stock, stock_symbol, last_dividend, par_value, fixed_dividend
):
    assert (
        preferred_stock.calc_dividend_yield(110) == (fixed_dividend * par_value) / 110
    )


def test_dividend_yield_invalid_price_preferred_stock(invalid_price):
    with pytest.raises(InvalidStockPriceError):
        preferred_stock = PreferredStock("GIN", 8, 100, 0.02)
        preferred_stock.calc_dividend_yield(invalid_price)
