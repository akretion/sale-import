# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def write(self, vals):
        result = super().write(vals)
        if "state" in vals.keys():
            for rec in self.filtered(lambda r: r.channel_id):
                rec.channel_id.execute_hook("sale_state", rec.state)
        return result
