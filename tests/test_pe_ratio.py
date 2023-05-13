import pytest


@pytest.mark.parametrize(
    "stock_symbol, last_dividend, par_value",
    [("POP", 8, 100), ("ALE", 23, 60), ("JOE", 13, 250)],
)
def test_pe_ratio_valid_price_common_stock(
    common_stock, stock_symbol, last_dividend, par_value
):
    assert common_stock.calc_pe_ratio(110) == 110 / last_dividend


@pytest.mark.parametrize(
    "stock_symbol, last_dividend, par_value",
    [("TEA", 0, 80)],
)
def test_pe_ratio_invalid_price_common_stock(common_stock):
    with pytest.raises(ZeroDivisionError):
        common_stock.calc_pe_ratio(100)


@pytest.mark.parametrize(
    "stock_symbol, last_dividend, par_value, fixed_dividend", [("GIN", 8, 100, 0.02)]
)
def test_pe_ratio_valid_price_preferred_stock(
    preferred_stock, stock_symbol, last_dividend, par_value, fixed_dividend
):
    assert preferred_stock.calc_pe_ratio(110) == 110 / (fixed_dividend * par_value)


@pytest.mark.parametrize(
    "stock_symbol, last_dividend, par_value, fixed_dividend", [("GIN", 8, 100, 0)]
)
def test_pe_ratio_invalid_price_preferred_stock(preferred_stock):
    with pytest.raises(ZeroDivisionError):
        preferred_stock.calc_pe_ratio(100)
