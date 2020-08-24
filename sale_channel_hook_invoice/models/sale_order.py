# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models

FIELDS_SIMPLE_COPY = ["name", "amount_total_signed"]


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "sale.channel.hook.mixin"]

    def _finalize_invoices(self, invoices, references):
        result = super()._finalize_invoices(invoices, references)
        for invoice, order in references.keys():
            order.trigger_channel_hook("create_invoice", invoice)
        return result

    def _get_hook_content_create_invoice(self, invoice):
        content = dict()
        for field in FIELDS_SIMPLE_COPY:
            content[field] = getattr(invoice, field)
        return content
