# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tools import float_compare

from odoo.addons.sale_import_base.tests.common_sale_order_import import SaleImportCase


class TestSaleOrderImport(SaleImportCase):
    def setUp(self):
        super().setUp()
        self.sale_order_example_vals["delivery_carrier"] = {
            "name": "Normal Delivery Charges",
            "price_unit": 10.0,
            "discount": 0.0,
        }
        json_import = self.sale_order_example_vals
        self.sale_order = self.env["sale.order"].process_json_import(json_import)

    def test_delivery_carrier_charges_applied(self):
        delivery_line = self.sale_order.order_line.filtered(lambda r: r.is_delivery)
        self.assertTrue(delivery_line)
        delivery_amount = delivery_line.price_total
        expected_delivery_amount = 10.0
        equal_delivery = float_compare(
            delivery_amount, expected_delivery_amount, precision_digits=2
        )
        self.assertEqual(equal_delivery, 0)
