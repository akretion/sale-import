#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import _
from odoo.tests import TransactionCase


class TestHookSaleState(TransactionCase):
    def test_hook_sale_state(self):
        sale = self.env.ref("sale.sale_order_1")
        for state in "draft", "sent", "sale", "done", "cancel":
            sale.write({"state": state})
            message = _("Sale Order SO001 has been updated to state %s" % state)
            content = {"message": message}
            self.assertEqual(content, sale.get_hook_content_sale_state())
