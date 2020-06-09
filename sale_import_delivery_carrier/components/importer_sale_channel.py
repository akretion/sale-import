#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
from odoo.addons.component.core import Component


class ImporterSaleChannel(Component):
    _inherit = "importer.sale.channel"

    def _prepare_vals(self, data):
        vals = super()._prepare_vals(data)
        return self._add_delivery_line(vals, data)

    def _add_delivery_line(self, vals, data):
        if not data.get("delivery_carrier"):
            return vals
        delivery_carrier = self.env["delivery.carrier"].search(
            [("name", "=", data["delivery_carrier"]["name"])]
        )
        price = data["delivery_carrier"]["price_unit"]
        discount = data["delivery_carrier"]["discount"]
        partner = self.env["res.partner"].browse(vals["partner_id"])
        carrier_with_partner_lang = delivery_carrier.with_context(lang=partner.lang)
        if carrier_with_partner_lang.product_id.description_sale:
            description = "{}: {}".format(
                carrier_with_partner_lang.name,
                carrier_with_partner_lang.product_id.description_sale,
            )
        else:
            description = carrier_with_partner_lang.name
        new_line_vals = {
            "name": description,
            "product_uom_qty": 1,
            "product_uom": delivery_carrier.product_id.uom_id.id,
            "product_id": delivery_carrier.product_id.id,
            "price_unit": price,
            "discount": discount,
            "is_delivery": True,
        }
        vals["order_line"].append((0, 0, new_line_vals))
        return vals
