# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    hook_active_delivery = fields.Boolean("Active delivery hook")
