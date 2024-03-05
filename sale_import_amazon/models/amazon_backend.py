# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


class AmazonBackend(models.Model):
    _name = "amazon.backend"
    _description = "Amazon Backend App"

    name = fields.Char()

    def _prepare_shipping_address(self, shipping_address):
        # TODO: Access to Personally Identifiable Information (PII) about Amazon Buyers
        # is required to catch the other shipping info

        country_id = self.env["res.country"].search(
            [("code", "=", shipping_address.get("CountryCode", ""))], limit=1
        )

        return {
            "zip": shipping_address.get("PostalCode", ""),
            "city": shipping_address.get("City", ""),
            "country_id": country_id.id,
        }

    def _get_partner_vals(self, order, amazon_email):
        """Extract partner and shipping values from order's data"""

        buyer_name = order["BuyerInfo"].get(
            "BuyerName", "Amazon Customer #%s" % order["AmazonOrderId"]
        )
        shipping_vals = self._prepare_shipping_address(order.get("ShippingAddress", {}))
        partner_vals = {
            "name": buyer_name,
            "company_id": self.company_id.id,
            "amazon_email": amazon_email,
        }
        # TODO: with Access to PII, return both partner_vals AND distinct shipping_vals
        partner_vals.update(shipping_vals)

        return partner_vals

    def _get_product_id(self, item):
        default_code = item["SellerSKU"]
        product_id = self.env["product.product"].search(
            [
                ("default_code", "=", default_code),
                "|",
                ("product_tmpl_id.company_id", "=", False),
                ("product_tmpl_id.company_id", "=", self.company_id.id),
            ],
            limit=1,
        )
        if not product_id:
            product_id = self.env["product.product"].create(
                {"default_code": default_code, "name": item.get("Title", "")}
            )

        return product_id

    def _get_line_vals(self, item):
        product_id = self._get_product_id(item)

        curr_code = item["ItemPrice"].get("CurrencyCode")
        currency_id = self.env["res.currency"].search([("name", "=", curr_code)])

        # FIXME: what's the best way to define if ItemPrice is tax incl. ou excl. ?

        # TODO:
        # - check if Amazon 'ItemPrice' is tax-excluded or not => TAX INCLUDED
        # - start from Amazon tax-excluded amount, Amazon tax amount and the tax needed
        # to be applied on the product
        # - compute the line's subtotal (tax-excluded) from the tax amount and the tax
        # that will be applied to ensure the same tax-excluded total amount in Amazon
        # and Odoo
        # - compute the line's price_unit from the computed subtotal and the qty

        orig_amount_tax_incl = item["ItemPrice"]["Amount"]
        taxes = item["ItemTax"]["Amount"]
        product_tax_ids = product_id.taxes_id

        return {
            "name": item["Title"],
            "currency_id": currency_id.id,
            "product_id": product_id.id,
        }

    def _get_order_vals(self, order):
        """Translate Amazon's response into Odoo Sale Order values"""

        lines_vals = []
        amazon_email = order["BuyerInfo"].get("BuyerEmail", "")
        existing_partner_id = self.env["res.partner"].search(
            [("amazon_email", "=", amazon_email)]
        )
        partner_vals = self._get_partner_vals(order, amazon_email)
        partner_id = existing_partner_id or self.env["res.partner"].create(partner_vals)

        for item in order["OrderItems"]:
            if item.get("SellerSKU"):
                lines_vals.append(self._get_line_vals(item))

        marketplace_id = self.env["amazon.marketplace"].search(
            [("marketplace_ref", "=", order.get("MarketplaceId"))]
        )
        last_upd = get_amz_date(order["LastUpdateDate"])
        date_order = get_amz_date(order["PurchaseDate"])

        vals = {
            "amazon_ref": order["AmazonOrderId"],
            "is_fulfilled_by_amazon": order["FulfillmentChannel"] == "AFN",
            "amazon_last_update": last_upd,
            "amazon_backend_id": self.id,
            "team_id": self.crm_team_id.id,
            "date_order": date_order,
            "amazon_marketplace_id": marketplace_id.id,
            "partner_id": partner_id.id,
            "partner_shipping_id": partner_id.id,  # TODO: change with access to PII
            "order_line": [Command.create(l) for l in lines_vals],
        }
        return vals

    def action_sync_orders(self):
        """ """
        self.ensure_one()
        orders_values = []
        orders = self._import_orders_data()

        for order in orders:
            existing_order_id = self.env["sale.order"].search(
                [("amazon_ref", "=", order["AmazonOrderId"])]
            )
            last_upd = get_amz_date(order["LastUpdateDate"])
            if existing_order_id and existing_order_id.amazon_last_update >= last_upd:
                continue

            order_vals = self._get_order_vals(order)

            if existing_order_id:
                # TODO: update order lines or shipping status if necessary
                pass
            else:
                orders_values.append(order_vals)

        order_ids = self.env["sale.order"].create(orders_values)

        return order_ids
