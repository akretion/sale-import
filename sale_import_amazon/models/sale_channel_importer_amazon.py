# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.addons.sale_import_amazon.utils import get_amz_date


class SaleChannelImporterAmazon(models.TransientModel):
    _inherit = "sale.channel.importer"
    _name = "sale.channel.importer.amazon"
    _description = "Sale Channel Importer Amazon"

    # TODO: manage existing SO shipped or canceled

    def _get_line_vals(self, item):
        qty = item["QuantityOrdered"]
        discount_amount = float(item.get("PromotionDiscount", {}).get("Amount", 0))
        total_incl_tax = float(item.get("ItemPrice", {}).get("Amount", 0))

        discount = 0
        if discount_amount and total_incl_tax:
            discount = discount_amount / total_incl_tax

        return {
            "product_code": item["SellerSKU"],
            "description": item["Title"],
            "qty": qty,
            # We assume the product is configured with the correct tax included in price
            "price_unit": total_incl_tax / qty if qty else 0,
            "discount": discount,
        }

    def _get_formatted_data(self):
        raw = super()._get_formatted_data()

        # We suppose we do not have access to Personally Identifiable Information (PII)
        # about Amazon Buyers :
        # no customer name, only an encoded email (used as Amazon's identifier),
        # shipping city, zip and country code.

        customer_name = _("Amazon Customer #%s" % raw["AmazonOrderId"])
        shipping = raw.get("ShippingAddress", {})
        address = {
            "name": customer_name,
            "street": "",
            "zip": shipping.get("PostalCode", ""),
            "city": shipping.get("City", ""),
            "country_code": shipping.get("CountryCode", ""),
        }

        formatted_data = {
            "name": raw["AmazonOrderId"],
            "date_order": get_amz_date(raw["PurchaseDate"]).date(),
            "address_customer": {
                "external_id": raw["BuyerInfo"].get("BuyerEmail", ""),
                **address,
            },
            "address_shipping": address,
            "address_invoicing": address,
            "lines": [self._get_line_vals(item) for item in raw["OrderItems"]],
            "state": raw["OrderStatus"].lower(),
            "is_fulfilled_by_amazon": raw["FulfillmentChannel"] == "AFN",
        }

        if raw.get("OrderTotal"):
            formatted_data.update(
                {
                    "currency_code": raw["OrderTotal"]["CurrencyCode"],
                    "amount": {"amount_total": raw["OrderTotal"]["Amount"]},
                }
            )

        return formatted_data

    def _manage_existing_so(self, existing_so, data):
        if data["state"] == "canceled" and existing_so.state != "cancel":
            existing_so._action_cancel()
        if data["state"] == "shipped" and existing_so.delivery_status != "full":
            existing_so._deliver_order_by_amazon()

    def _prepare_sale_vals(self, data):
        so_vals = super()._prepare_sale_vals(data)
        so_vals["is_fulfilled_by_amazon"] = data["is_fulfilled_by_amazon"]
        # TODO: add markerplace_id

        return so_vals

    def _finalize(self, new_sale_order, raw_import_data):
        super()._finalize(new_sale_order, raw_import_data)
        if raw_import_data["state"] == "shipped":
            new_sale_order._deliver_order_by_amazon()
        if raw_import_data["state"] == "canceled":
            new_sale_order._action_cancel()
