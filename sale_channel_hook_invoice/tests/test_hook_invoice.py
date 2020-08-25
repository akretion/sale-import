#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.tools import float_compare

from odoo.addons.account.tests.account_test_classes import AccountingTestCase


class TestHookInvoice(AccountingTestCase):
    def test_hook_create_invoice(self):
        invoice = self.env.ref("l10n_generic_coa.demo_invoice_3")
        channel = self.env.ref("sale_channel.sale_channel_amazon")
        invoice.sale_channel_id = channel
        channel.hook_active_create_invoice = True
        channel.hook_active_create_invoice_send_pdf = True
        content = invoice.get_hook_content_create_invoice()
        self.assertEqual(content["invoice_no"], "INV/2020/0003")
        self.assertEqual(
            0, float_compare(content["amount_total"], 525, precision_digits=2)
        )
        self.assertEqual(content["origin"], False)
        self.assertTrue(content["pdf_document"])
