# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_delivery_line(self, carrier, price_unit):
        result = super()._create_delivery_line(carrier, price_unit)
        channel = self.channel_id
        if channel:
            channel.execute_hook("delivery", result)
        return result
