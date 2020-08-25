#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import base64

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

    def get_hook_content_create_invoice(self, invoice):
        content = {
            "invoice_no": invoice.name,
            "amount_total": invoice.amount_total_signed,
            "origin": invoice.origin,
        }
        if self.channel_id.hook_active_send_pdf:
            pdf_bin = self.channel_id.hook_invoice_report.render_qweb_pdf([self.id])
            pdf_encoded = base64.b64encode(pdf_bin)
            content["pdf_document"] = pdf_encoded
        return content
