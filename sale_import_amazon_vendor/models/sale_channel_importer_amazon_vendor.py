# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import ValidationError

from ..utils import get_amz_date


class SaleChannelImporterAmazon(models.TransientModel):
    _inherit = "sale.channel.importer"
    _name = "sale.channel.importer.amazon.vendor"
    _description = "Sale Channel Importer Amazon Vendor"

    def _find_partner(self, customer_data):
        """The Amazon Vendor API works only with the External ID to identify
        the customer and its addresses"""
        partner_id = super()._find_partner(customer_data)
        external_id = customer_data["external_id"]
        if not partner_id:
            raise ValidationError(
                _("No partner found with the External ID '%s'." % external_id)
            )
        return partner_id

    def _process_partner(self, customer_data):
        """If the partner is catched by External ID, do not update its values"""
        partner = self._find_partner(customer_data)
        return partner

    def _process_addresses(
        self, parent, address_invoice, address_shipping, archive_addresses
    ):
        """Catch Invoice and Shipping address by Amazon's External ID too"""
        address_invoice_id = self._find_partner(address_invoice)
        address_shipping_id = self._find_partner(address_shipping)
        return address_invoice_id, address_shipping_id

    def _get_line_vals(self, item):
        # TODO : in case of "unitOfMeasure": "Cases" we can extract the size of the
        # packs with param "unitSize"

        price_unit_incl_tax = float(item.get("netCost", {}).get("amount", 0))
        qty = float(item.get("orderedQuantity", {}).get("amount", 0))

        line_vals = {
            "product_code": item["vendorProductIdentifier"],
            "description": "ASIN: " + item["amazonProductIdentifier"],
            "qty": qty,
            # We assume the product is configured with the correct tax included in price
            "price_unit": price_unit_incl_tax,
        }

        return line_vals

    def _get_formatted_data(self):
        raw = super()._get_formatted_data()
        details = raw["orderDetails"]
        basic_addr = {
            "name": "",
            "street": "",
            "zip": "",
            "city": "",
            "country_code": "",
        }
        customer = {**basic_addr, "external_id": details["buyingParty"]["partyId"]}
        shipping = {**basic_addr, "external_id": details["shipToParty"]["partyId"]}
        invoicing = {**basic_addr, "external_id": details["billToParty"]["partyId"]}

        date_order = get_amz_date(details["purchaseOrderDate"]).strftime("%Y-%m-%d")

        formatted_data = {
            "name": raw["purchaseOrderNumber"],
            "date_order": date_order,
            "address_customer": customer,
            "address_shipping": shipping,
            "address_invoicing": invoicing,
            "lines": [self._get_line_vals(item) for item in details["items"]],
        }

        amount = sum(l["qty"] * l["price_unit"] for l in formatted_data["lines"])
        formatted_data["amount"] = {"amount_total": amount}

        currency_code = details["items"][-1]["netCost"]["currencyCode"]
        currency_pricelist = self.chunk_id.reference.pricelist_id.currency_id.name
        if currency_code != currency_pricelist:
            raise ValidationError(
                _(
                    " The Curency code %(currency_code)s is different from "
                    "Sale Channel pricelist's currency %(currency_pricelist)s"
                    % {
                        "currency_code": currency_code,
                        "currency_pricelist": currency_pricelist,
                    }
                )
            )
        return formatted_data

    # def _manage_existing_so(self, existing_so, data):
    #     if data["state"] == "canceled" and existing_so.state != "cancel":
    #         existing_so._action_cancel()
    #     else:
    #         res = super()._manage_existing_so(existing_so, data)
    #         return res

    # def _finalize(self, new_sale_order, raw_import_data):
    #     res = super()._finalize(new_sale_order, raw_import_data)
    #     if raw_import_data["state"] == "canceled":
    #         new_sale_order._action_cancel()
    #     return res
