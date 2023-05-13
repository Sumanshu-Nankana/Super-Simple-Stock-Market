# Super Simple Stock Market

This is an object-oriented system built for the Global Beverage Corporation Exchange, a new stock market trading in drinks companies.

## Requirements

For a given stock, this system must be able to:

- Given any price as input, calculate the dividend yield
- Given any price as input, calculate the P/E Ratio
- Record a trade, with timestamp, quantity, buy or sell indicator and price
- Calculate Volume Weighted Stock Price based on trades in past 5 minutes
- Calculate the GBCE All Share Index using the geometric mean of the Volume Weighted Stock Price for all stocks

## Implementation

This implementation is written in Python and It implements the following formulae:

### Formula

#### Common Stock

- Dividend Yield = Last Dividend / Price
- P/E Ratio = Price / Dividend

#### Preferred Stock

- Dividend Yield = (Fixed Dividend x Par Value) / Price
- P/E Ratio = Price / Dividend

#### All Stocks

- Geometric Mean = Square Root of (n & p1 & p2 & p3 ... pn)
- Volume Weighted Stock Price = (Σ Traded Pricei x Quantityi) / (Σ Quantityi)
- GBCE All Share Index = Geometric Mean of the Volume Weighted Stock Price for all stocks

## How to use

1. Clone the repository or download the source code
2. Open the terminal and navigate to the directory where the files are located
3. Install the test packages `pipenv install`
4. To execute the unit tests run the command `pipenv run pytest -v`
5. To calculate the code coverage, run the command `pipenv run pytest --cov=src tests/ --cov-report html`

## Files
Source code resides in the `src` folder.
Unit Tests resides in the `tests` folder

### `gbc_exchange.py`

This file contains the `Stock` class and its subclasses `CommonStock` and `PreferredStock`. 
It also contains the `GBCExchange` class. And all the required methods

### `custom_exceptions.py`

This file contains the custom exceptions classes


### `validate.py`

This file contains the function which is used as a decorator in `gbc_exchange.py` to validate the price of a stock

### `conftest.py`

This file contains the fixtures for the unit tests

### `test_dividend_yield.py`

This file contains the unit tests for testing the dividend_yield for both Common and Preferred Type of stocks.

### `test_pe_ratio.py`

This file contains the unit tests for testing the pe_ratio for both Common and Preferred Type of stocks.

### `test_trade.py`

This file contains the unit tests for testing the record_trade and test case for volume weighted stock
price for last 5 min trades.

### `test_gbce_exchange.py`

This file contains the unit tests for testing the GBCE all share index.