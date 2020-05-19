# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import json

from odoo.tools import float_compare

from odoo.addons.sale_import_base.tests.common_sale_order_import import SaleImportCase


class TestSaleOrderImport(SaleImportCase):
    def setUp(self):
        super().setUp()

    def test_delivery_carrier_charges_applied(self):
        json_import = self.sale_data
        json_import["delivery_carrier"] = {
            "name": "Normal Delivery Charges",
            "price_unit": 10.0,
            "discount": 0.0,
        }
        json_import["pricelist_id"] = (
            self.env["product.pricelist"]
            .search([("currency_id", "=", self.env.ref("base.USD").id)])[0]
            .id
        )
        sale_order = self.importer_component.run(json.dumps(json_import))
        delivery_line = sale_order.order_line.filtered(lambda r: r.is_delivery)
        self.assertTrue(delivery_line)
        delivery_amount = delivery_line.price_total
        expected_delivery_amount = 10.0
        equal_delivery = float_compare(
            delivery_amount, expected_delivery_amount, precision_digits=2
        )
        self.assertEqual(equal_delivery, 0)
