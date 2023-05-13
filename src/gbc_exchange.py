import math
import logging
from enum import Enum
from datetime import datetime, timedelta
from .validate import validate_price
from abc import ABC, abstractmethod
from .custom_exceptions import (
    InvalidStockQuantityError,
    InvalidTradeIndicatorError,
    InvalidStockPriceError,
)

logger = logging.getLogger(__name__)


class TradeIndicator(Enum):
    BUY = "BUY"
    SELL = "SELL"


class Stock(ABC):
    """
    This is an interface for the Stock Object.

    Methods:
        calc_dividend_yield: calculate the dividend yield for a given stock
        calc_pe_ratio      : calculate the P/E ratio for a given stock
    """

    DEFAULT_TIME: int = 5

    def __init__(self, stock_symbol: str, last_dividend: float, par_value: float):
        self.stock_symbol: str = stock_symbol
        self.last_dividend: float = last_dividend
        self.par_value: float = par_value
        self.trades: list[dict] = []

    @abstractmethod
    def calc_dividend_yield(self, price: float) -> float:
        """
        Calculate the dividend yield for a given stock price

        Args:
            price (float): price of a stock

        Returns:
            float: dividend yield value of a particular stock
        """
        pass

    @abstractmethod
    def calc_pe_ratio(self, price: float) -> float:
        """
        Calculate the P/E ratio for a given stock price.

        Args:
            price (float): price of a stock

        Returns:
            float: P/E ratio value of a particular stock
        """
        pass

    def record_trade(
        self, quantity: int, buy_sell_indicator: str, price: float
    ) -> None:
        """
        This function will record or do the entry of all
        the trade as soon as it happens

        Args:
           quantity: quantity of the trade
           buy_sell_indicator: whether trade is for BUY or SELL
           price: For what price, stock get traded

        Returns:
            None
        """
        if quantity <= 0:
            logger.error("Quantity should be greater than zero")
            raise InvalidStockQuantityError("Quantity should be greater than zero")

        if price <= 0:
            logger.error("Price should be greater than zero")
            raise InvalidStockPriceError("Price should be greater than zero")

        try:
            buy_sell_indicator = TradeIndicator(buy_sell_indicator)
        except ValueError:
            raise InvalidTradeIndicatorError("Valid Trade Indicators are BUY and SELL")

        trade: dict = {
            "timestamp": datetime.now(),
            "quantity": quantity,
            "buy_sell_indicator": buy_sell_indicator,
            "price": price,
        }

        self.trades.append(trade)

    def calc_vol_weighted_stock_price(self) -> float:
        """
        Calculate the volume weighted stock price for a all trade of a particular stock
        """
        print(self.trades)
        total_value = 0
        total_quantity = 0
        for trade in self.trades:
            print(trade)
            total_value += trade["price"] * trade["quantity"]
            total_quantity += trade["quantity"]
        if total_quantity < 1:
            return 0
        volume_weighted_stock_price = total_value / total_quantity
        return volume_weighted_stock_price

    def calc_vol_weighted_stock_price_last_5_mins(self) -> float:
        """
        Calculate the Volume weighted Stock Price for the last 5 minutes trade.

        Returns:
             float: Returns the weighted stock price volume
                    for the last 5-minute trade.
        """
        last_5_min_trades: list[dict] = []
        current_time = datetime.now()
        last_5_min_time = current_time - timedelta(minutes=Stock.DEFAULT_TIME)

        for trade in self.trades:
            if last_5_min_time <= trade["timestamp"] <= current_time:
                last_5_min_trades.append(trade)

        if len(last_5_min_trades) == 0:
            logger.warning("No trade occurs in last 5 minutes")
            return None

        total_volume = sum(
            [trade["price"] * trade["quantity"] for trade in last_5_min_trades]
        )
        total_quantity = sum([trade["quantity"] for trade in last_5_min_trades])
        volume_Weighted_stock_price = total_volume / total_quantity

        logger.info(
            f"Volume Weighted Stock Price for {self.stock_symbol} : "
            f"{volume_Weighted_stock_price}"
        )

        return round(volume_Weighted_stock_price, 3)


class CommonStock(Stock):
    """Class for a Common Type of Stock"""

    def __init__(self, stock_symbol: str, last_dividend: float, par_value: float):
        super().__init__(stock_symbol, last_dividend, par_value)

    @validate_price
    def calc_dividend_yield(self, price: float) -> float:
        """
        Implementation of abstract method calc_dividend_yield
        which will calculate the dividend yield for a given COMMON type stock

        Args:
            price (float): price of a stock

        Returns:
            float: dividend yield value of a particular stock
        """
        dividend_yield = self.last_dividend / price
        logger.info(f"Dividend yield for {self.stock_symbol} " f"is {dividend_yield}")

        return dividend_yield

    @property
    def dividend(self):
        return self.last_dividend

    def calc_pe_ratio(self, price: float) -> float:
        """
        Implementation of abstract method cal_pe_ratio
        which will calculate the P/E ratio for a given COMMON type stock

        Args:
            price (float): price of a stock

        Returns:
            float: P/E ratio value of a particular stock
        """
        try:
            pe_ratio = price / self.dividend
            logger.info(f"P/E ratio for the {self.stock_symbol} is {pe_ratio}")
            return pe_ratio
        except ZeroDivisionError as e:
            logger.error("ZeroDivisionError occurred while calculating the PE Ratio")
            raise ZeroDivisionError


class PreferredStock(Stock):
    """Class for a Preferred Type of Stock"""

    def __init__(
        self,
        stock_symbol: str,
        last_dividend: float,
        par_value: float,
        fixed_dividend: float,
    ):
        super().__init__(stock_symbol, last_dividend, par_value)
        self.fixed_dividend = fixed_dividend

    @validate_price
    def calc_dividend_yield(self, price: float) -> float:
        """
        Implementation of abstract method cal_dividend_yield
        which will calculate the dividend yield for a given
        PREFERRED type stock

        Args:
            price (float): price of a stock to calculate the dividend yield

        Returns:
            float: calculated dividend yield for a common type of stock
        """
        dividend_yield = (self.fixed_dividend * self.par_value) / price
        logger.info(f"Dividend yield for {self.stock_symbol} is " f"{dividend_yield}")

        return dividend_yield

    @property
    def dividend(self):
        return self.fixed_dividend * self.par_value

    def calc_pe_ratio(self, price: float) -> float:
        """
        Implementation of abstract method cal_pe_ratio
        which will calculate the P/E ratio for a given PREFERRED type stock

        Args:
            price (float): price of a stock

        Returns:
            float: calculated P/E ratio value for a given
                   PREFERRED type stock
        """
        try:
            pe_ratio = price / self.dividend
            logger.info(f"P/E ratio for the {self.stock_symbol} is {pe_ratio}")
            return pe_ratio
        except ZeroDivisionError as e:
            logger.info("Zero Division Error occurred while calculating the PE Ratio")
            raise ZeroDivisionError


class GBCExchange:
    """
    Global Beverage Corporation Exchange class
    """

    def __init__(self):
        self.stocks = {}

    def add_stock(self, stock: Stock):
        """
        Add the Stock
        """
        self.stocks[stock.stock_symbol] = stock

    def get_stock(self, stock_symbol):
        """
        Get the stock
        """
        return self.stocks.get(stock_symbol)

    def calc_gbce_all_share_index(self) -> float:
        """
          Calculate the GBCE All Share Index using the geometric mean of
          the Volume Weighted Stock Price for all stocks

        Returns:
             float : Geometric mean of the Volume Weighted Stock Price
        """
        total_value = 1.0
        total_quantity = 0
        for stock in self.stocks.values():
            stock_value = stock.calc_vol_weighted_stock_price()
            total_value *= stock_value
            if stock_value > 0:
                total_quantity += 1
        if total_quantity == 0:
            return 0.0
        else:
            return round(total_value ** (1.0 / total_quantity), 3)

    def __repr__(self):
        return f"GBCExchange(stocks={list(self.stocks.keys())})"
