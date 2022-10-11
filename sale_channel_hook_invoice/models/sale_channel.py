#  Copyright (c) Akretion 2020
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    hook_active_create_invoice = fields.Boolean("Active invoice hook")
    hook_active_create_invoice_send_pdf = fields.Boolean("Send PDF")
    hook_active_create_invoice_report = fields.Many2one(
        "ir.actions.report",
        default=lambda self: self.env.ref("account.account_invoices_without_payment"),
        required=True,
        string="Document report",
    )

    @api.onchange("hook_active_create_invoice")
    def _onchange_hook_active_create_invoice(self):
        for rec in self:
            if not rec.hook_active_create_invoice:
                rec.hook_active_create_invoice_send_pdf = False
