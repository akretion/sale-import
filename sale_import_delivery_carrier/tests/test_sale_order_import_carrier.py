#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import json

from odoo.tools import float_compare

from odoo.addons.sale_import_base.tests.common_sale_order_import import SaleImportCase


class TestSaleOrderImport(SaleImportCase):
    def setUp(self):
        super().setUp()

    def test_delivery_carrier_charges_applied(self):
        data = self.sale_data
        data["delivery_carrier"] = {
            "name": "Normal Delivery Charges",
            "price_unit": 10.0,
            "discount": 0.0,
        }
        sale_order = self.importer_component.run(json.dumps(data))
        delivery_line = sale_order.order_line.filtered(lambda r: r.is_delivery)
        self.assertEqual(len(delivery_line.ids), 1)
        delivery_amount = delivery_line.price_total
        expected_delivery_amount = 10.0
        equal_delivery = float_compare(
            delivery_amount, expected_delivery_amount, precision_digits=2
        )
        self.assertEqual(equal_delivery, 0)

    def test_deliver_country_with_tax(self):
        """ Test fiscal position is applied correctly """
        data = self.sale_data
        data["address_shipping"]["country_code"] = "CH"
        new_sale_order = self.importer_component.run(json.dumps(data))
        delivery_line = new_sale_order.order_line.filtered(lambda r: r.is_delivery)
        self.assertEqual(delivery_line.tax_id, self.tax_swiss)
