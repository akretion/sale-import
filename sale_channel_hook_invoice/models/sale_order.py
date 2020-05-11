# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _finalize_invoices(self, invoices, references):
        result = super()._finalize_invoices(invoices, references)
        for invoice, order in references.keys():
            channel = order.channel_id
            if channel:
                channel.execute_hook("create_invoice", invoice)
        return result
