#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
from odoo.addons.component.core import Component


class ImporterSaleChannel(Component):
    _inherit = "importer.sale.channel"

    def _prepare_sale_line_vals(self, data, sale_order):
        vals = super()._prepare_sale_line_vals(data, sale_order)
        delivery_line = self._prepare_delivery_line(data, sale_order)
        return vals + [delivery_line]

    def _prepare_delivery_line(self, data, sale_order):
        if not data.get("delivery_carrier"):
            return
        delivery_carrier = self.env["delivery.carrier"].search(
            [("name", "=", data["delivery_carrier"]["name"])]
        )
        partner = sale_order.partner_id
        carrier_with_partner_lang = delivery_carrier.with_context(lang=partner.lang)
        if carrier_with_partner_lang.product_id.description_sale:
            description = "{}: {}".format(
                carrier_with_partner_lang.name,
                carrier_with_partner_lang.product_id.description_sale,
            )
        else:
            description = carrier_with_partner_lang.name
        vals = {
            "name": description,
            "product_uom_qty": 1,
            "product_uom": delivery_carrier.product_id.uom_id.id,
            "product_id": delivery_carrier.product_id.id,
            "price_unit": data["delivery_carrier"]["price_unit"],
            "discount": data["delivery_carrier"]["discount"],
            "is_delivery": True,
            "order_id": sale_order.id,
        }
        return self.env["sale.order.line"].play_onchanges(vals, ["product_id"])
