#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    hook_active_create_invoice = fields.Boolean("Active invoice hook")
    hook_active_create_invoice_send_pdf = fields.Boolean("Send PDF")
    hook_active_create_invoice_report = fields.Many2one(
        "ir.ui.view",
        default=lambda self: self.env.ref("account.report_invoice_document"),
        required=True,
        string="Document generation template",
    )
