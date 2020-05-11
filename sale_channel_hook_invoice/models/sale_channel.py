# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

FIELDS_SIMPLE_COPY = ["name", "amount_total_signed"]


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    hook_active_create_invoice = fields.Boolean("Active invoice hook")

    def _get_hook_content_create_invoice(self, invoice):
        content = dict()
        for field in FIELDS_SIMPLE_COPY:
            content[field] = getattr(invoice, field)
        return content
