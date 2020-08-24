# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "sale.channel.hook.mixin"]

    def _finalize_invoices(self, invoices, references):
        result = super()._finalize_invoices(invoices, references)
        for invoice, order in references.keys():
            order.trigger_hook("create_invoice", invoice)
        return result
