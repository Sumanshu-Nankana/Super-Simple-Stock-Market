import logging
from .custom_exceptions import InvalidStockPriceError

logger = logging.getLogger(__name__)


def validate_price(method):
    def wrapper(self, price):
        if price <= 0:
            logger.error("Stock price should be greater than zero")
            raise InvalidStockPriceError("Stock price should be greater than zero")
        return method(self, price)

    return wrapper
