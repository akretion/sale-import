# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "sale.channel.hook.mixin"]

    def write(self, vals):
        result = super().write(vals)
        for rec in self:
            if "state" in vals.keys():
                rec.trigger_hook("sale_state", rec)
        return result

    def _get_hook_content_sale_state(self, sale_order):
        state = sale_order.state
        name = sale_order.name
        content = "Sale Order %s has been updated to state %s" % name, state
        return content
