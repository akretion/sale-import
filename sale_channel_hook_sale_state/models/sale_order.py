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
                rec.trigger_channel_hook("sale_state")
        return result

    def get_hook_content_sale_state(self, *args):
        state = self.state
        name = self.name
        message = _("Sale Order {} has been updated to state {}".format(name, state))
        content = {"message": message}
        return content
