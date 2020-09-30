#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import base64
import logging

from odoo import models

FIELDS_SIMPLE_COPY = ["name", "amount_total_signed"]

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = ["account.invoice", "sale.channel.hook.mixin"]

    def action_invoice_paid(self):
        result = super().action_invoice_paid()
        for rec in self:
            origin = rec.invoice_line_ids.mapped("sale_line_ids").mapped("order_id")
            if len(origin.ids) > 1:
                _logger.warning("Two possible SOs detected for invoice hook")
            if origin and origin[0].sale_channel_id.hook_active_create_invoice:
                rec.trigger_channel_hook("create_invoice", origin[0])
        return result

    def get_hook_content_create_invoice(self, origin):
        content = {"sale_name": origin.name, "invoice": self.number}
        if self.sale_channel_id.hook_active_create_invoice_send_pdf:
            report = self.sale_channel_id.hook_active_create_invoice_report
            pdf_bin = report.render_qweb_pdf([self.id])[0]
            pdf_encoded = base64.b64encode(pdf_bin)
            content["pdf"] = pdf_encoded
        return content
