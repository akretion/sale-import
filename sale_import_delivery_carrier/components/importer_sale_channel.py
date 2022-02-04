#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
from odoo import _
from odoo.exceptions import ValidationError
from odoo.tools import float_compare

from odoo.addons.component.core import Component


class ImporterSaleChannel(Component):
    _inherit = "importer.sale.channel"

    def _prepare_sale_vals(self, data):
        vals = super()._prepare_sale_vals(data)
        if not data.get("delivery_carrier"):
            return vals
        carrier_id = self.env["delivery.carrier"].search(
            [("code", "=", data["delivery_carrier"]["code"])]
        )
        if not carrier_id:
            raise ValidationError(_("Couldn't find a carrier with given code"))
        vals.update({"carrier_id": carrier_id.id})
        return vals

    def _prepare_sale_line_vals(self, data, sale_order):
        vals = super()._prepare_sale_line_vals(data, sale_order)
        delivery_line = self._prepare_delivery_line(data, sale_order)
        if delivery_line:
            vals += [delivery_line]
        return vals

    def _prepare_delivery_line(self, data, sale_order):
        precision = self.env["decimal.precision"].precision_get("Product Price")
        price = float(data["delivery_carrier"]["price_unit"])
        no_delivery_charges = float_compare(price, 0.0, precision_digits=precision)
        if not data.get("delivery_carrier") or no_delivery_charges == 0:
            return
        delivery_carrier = self.env["delivery.carrier"].search(
            [("code", "=", data["delivery_carrier"]["code"])]
        )
        partner = sale_order.partner_id
        carrier_with_partner_lang = delivery_carrier.with_context(lang=partner.lang)
        description = data["delivery_carrier"].get("description")
        if not description:
            if carrier_with_partner_lang.product_id.description_sale:
                description = "{}: {}".format(
                    carrier_with_partner_lang.name,
                    description
                    or carrier_with_partner_lang.product_id.description_sale,
                )
            else:
                description = carrier_with_partner_lang.name
        vals = {
            "name": description,
            "product_uom_qty": 1,
            "product_uom": delivery_carrier.product_id.uom_id.id,
            "product_id": delivery_carrier.product_id.id,
            "price_unit": price,
            "discount": data["delivery_carrier"].get("discount"),
            "is_delivery": True,
            "order_id": sale_order.id,
        }
        return self.env["sale.order.line"].play_onchanges(vals, ["product_id"])
