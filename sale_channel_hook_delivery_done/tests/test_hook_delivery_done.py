#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.tools import float_compare
from odoo.addons.sale.tests.test_sale_common import TestSale
from odoo import _

class TestHookSaleDeliveryDone(TestSale):

    def test_01_sale_stock_order(self):
        """
        Create SO, mark pickings as delivered
        """
        sale = self.env.ref("sale.sale_order_3")
        for sol in sale.order_line:
            sol.product_id.invoice_policy = 'order'
        sale.action_confirm()
        sale.picking_ids.state = "done"
        content = sale.picking_ids.get_hook_content_delivery_done()
        self.assertEqual(content["message"], _("Delivery complete SO003"))
