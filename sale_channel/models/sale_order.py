# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_channel_id = fields.Many2one("sale.channel", ondelete="set null")

    def _finalize_invoices(self, invoices, references):
        super()._finalize_invoices(invoices, references)
        for invoice, order in references.items():
            invoice.sale_channel_id = order.sale_channel_id
