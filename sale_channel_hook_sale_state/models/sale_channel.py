# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    hook_active_sale_state = fields.Boolean("Active sale state hook")

    def _get_hook_content_sale_state(self, sale_order):
        state = sale_order.state
        name = sale_order.name
        content = "Sale Order %s has been updated to state %s" % name, state
        return content
