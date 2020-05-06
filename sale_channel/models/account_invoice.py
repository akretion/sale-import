# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    sale_channel_id = fields.Many2one(
        "sale.channel", string="Sale Channel", ondelete="set null"
    )
