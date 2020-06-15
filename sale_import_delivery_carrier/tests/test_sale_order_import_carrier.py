#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import json

from odoo.tools import float_compare

from odoo.addons.sale_import_base.tests.common_sale_order_import import SaleImportCase


class TestSaleOrderImport(SaleImportCase):
    @property
    def sale_data(self):
        data = super().sale_data
        data["delivery_carrier"] = {
            "name": "Normal Delivery Charges",
            "price_unit": 10.0,
            "discount": 0.0,
        }
        return data

    def setUp(self):
        super().setUp()
        self.env.ref("delivery.product_product_delivery_normal").taxes_id = self.tax

    def test_delivery_carrier_id(self):
        """ Test sale order has the correct delivery carrier """
        sale_order = self.importer_component.run(json.dumps(self.sale_data))
        self.assertEqual(
            sale_order.carrier_id, self.env.ref("delivery.normal_delivery_carrier")
        )

    def test_delivery_carrier_charges_applied(self):
        """ Test delivery line is created with correct amount """
        sale_order = self.importer_component.run(json.dumps(self.sale_data))
        delivery_line = sale_order.order_line.filtered(lambda r: r.is_delivery)
        self.assertEqual(len(delivery_line.ids), 1)
        equal_delivery = float_compare(
            delivery_line.price_total, 10.9, precision_digits=2
        )
        self.assertEqual(equal_delivery, 0)

    def test_deliver_country_with_tax(self):
        """ Test fiscal position and tax is applied correctly
        to the delivery line """
        data = self.sale_data
        data["address_shipping"]["country_code"] = "CH"
        new_sale_order = self.importer_component.run(json.dumps(data))
        delivery_line = new_sale_order.order_line.filtered(lambda r: r.is_delivery)
        self.assertEqual(delivery_line.tax_id, self.tax_swiss)
