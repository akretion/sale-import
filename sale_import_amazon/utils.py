import dateutil
from sp_api.api import Orders
from sp_api.base import Marketplaces
from sp_api.util import load_all_pages, throttle_retry


@throttle_retry()
@load_all_pages()
def load_order_pages(credentials, country_code, last_updated_after, **kwargs):
    """
    A generator function to return a list of Amazon orders, grouped by pages and
    filtered by  `last_updated_after`.

    Using python-amazon-sp-api tools.
    """
    marketplace = Marketplaces.__getattr__(country_code)

    # FIXME: SSLError when last_updated_after > 100 days
    # `Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING]
    # EOF occurred in violation of protocol (_ssl.c:1007)')))`

    return Orders(credentials=credentials, marketplace=marketplace).get_orders(
        LastUpdatedAfter=last_updated_after, **kwargs
    )


def load_order_items(credentials, country_code, amazon_ref):
    """Return a list of dict with order's items data

    Amazon SP-API sadly force to do distinct calls : one to catch the orders IDs
    and one for each order to get their items.
    """
    marketplace = Marketplaces.__getattr__(country_code)

    return Orders(credentials=credentials, marketplace=marketplace).get_order_items(
        amazon_ref
    )


def get_amz_date(amazon_date):
    return dateutil.parser.parse(amazon_date).replace(tzinfo=None)
