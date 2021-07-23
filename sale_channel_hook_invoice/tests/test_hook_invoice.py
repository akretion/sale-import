#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)


from odoo import SUPERUSER_ID

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


class TestHookInvoice(AccountTestInvoicingCommon):
    def setUp(self):
        super().setUp()
        # As the env.user is superuser anyways for our controllers,
        # for now we neglect it for tests
        superuser = self.env["res.users"].browse([SUPERUSER_ID])
        self.env = self.env(user=superuser)
        self.cr = self.env.cr

    def test_hook_create_invoice(self):
        invoice = self.env.ref("l10n_generic_coa.demo_invoice_3")
        channel = self.env.ref("sale_channel.sale_channel_amazon")
        sale = self.env.ref("sale.sale_order_1")
        invoice.sale_channel_id = channel
        channel.hook_active_create_invoice = True
        channel.hook_active_create_invoice_send_pdf = True
        content = invoice.get_hook_content_create_invoice(sale)["data"]
        self.assertEqual(content["invoice"], invoice.name)
        self.assertEqual(content["sale_name"], sale.client_order_ref)
        self.assertTrue(content["pdf"])
