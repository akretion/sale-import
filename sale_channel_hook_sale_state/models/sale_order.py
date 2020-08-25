#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import _, models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "sale.channel.hook.mixin"]

    def write(self, vals):
        result = super().write(vals)
        for rec in self:
            if "state" in vals.keys():
                rec.trigger_channel_hook("sale_state", rec)
        return result

    def get_hook_content_sale_state(self, sale_order):
        state = sale_order.state
        name = sale_order.name
        message = _("Sale Order %s has been updated to state %s" % name, state)
        content = {"message": message}
        return content
