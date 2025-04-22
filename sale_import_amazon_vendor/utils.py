import dateutil
from sp_api.api import VendorOrders
from sp_api.base import Marketplaces
from sp_api.util import load_all_pages, throttle_retry


@throttle_retry()
@load_all_pages()
def load_purchase_order_pages(
    credentials, country_code, date_filtering_type, date_filtering, **kwargs
):
    """
    A generator function to return a list of Amazon Purchase Orders, grouped by pages
    and filtered by  `date_filtering_type`.

    Using python-amazon-sp-api tools.
    """
    marketplace = Marketplaces.__getattr__(country_code)

    return VendorOrders(
        credentials=credentials, marketplace=marketplace
    ).get_purchase_orders(
        **{date_filtering_type: date_filtering}, includeDetails="true", **kwargs
    )


def get_amz_date(amazon_date):
    return dateutil.parser.parse(amazon_date).replace(tzinfo=None)
