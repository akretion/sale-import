# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "sale.channel.hook.mixin"]

    def _create_delivery_line(self, carrier, price_unit):
        result = super()._create_delivery_line(carrier, price_unit)
        self.trigger_hook("delivery", result)
        return result

    def _get_hook_content_delivery(self, sale_order_line):
        delivery_no = sale_order_line.name
        content = "Delivery line created %s" % delivery_no
        return content
