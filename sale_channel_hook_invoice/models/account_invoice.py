#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import base64

from odoo import models

FIELDS_SIMPLE_COPY = ["name", "amount_total_signed"]


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = ["account.invoice", "sale.channel.hook.mixin"]

    def action_invoice_paid(self):
        result = super().action_invoice_paid()
        for rec in self:
            rec.trigger_channel_hook("create_invoice")
        return result

    def get_hook_content_create_invoice(self):
        content = {
            "invoice_no": self.number,
            "amount_total": self.amount_total_signed,
            "origin": self.origin,
        }
        if self.sale_channel_id.hook_active_create_invoice_send_pdf:
            report = self.sale_channel_id.hook_active_create_invoice_report
            pdf_bin = report.render_qweb_pdf([self.id])[0]
            pdf_encoded = base64.b64encode(pdf_bin)
            content["pdf_document"] = pdf_encoded
        return content
