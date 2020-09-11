#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from datetime import datetime

from odoo.tools import float_compare

from odoo.addons.account.tests.account_test_classes import AccountingTestCase


class TestHookInvoice(AccountingTestCase):
    def test_hook_create_invoice(self):
        invoice = self.env.ref("l10n_generic_coa.demo_invoice_3")
        invoice.origin = "SOXYZ"
        channel = self.env.ref("sale_channel.sale_channel_amazon")
        invoice.sale_channel_id = channel
        channel.hook_active_create_invoice = True
        channel.hook_active_create_invoice_send_pdf = True
        content = invoice.get_hook_content_create_invoice()
        year = datetime.now().year
        self.assertEqual(content["invoice"], "INV/%s/0003" % year)
        self.assertEqual(content["sale_name"], "SOXYZ")
        self.assertTrue(content["pdf"])
