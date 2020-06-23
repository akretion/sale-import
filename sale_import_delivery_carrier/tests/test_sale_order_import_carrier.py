#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.tools import float_compare

from odoo.addons.sale_import_base.tests.common_sale_order_import import SaleImportCase


class TestSaleOrderImport(SaleImportCase):
    @property
    def chunk_vals(self):
        chunk_vals = super().chunk_vals
        chunk_vals["data_str"]["delivery_carrier"] = {
            "name": "Normal Delivery Charges",
            "price_unit": 10.0,
            "discount": 0.0,
            "description": "CustomDescription",
        }
        return chunk_vals

    def setUp(self):
        super().setUp()
        self.env.ref("delivery.product_product_delivery_normal").taxes_id = self.tax

    def test_delivery_carrier_id(self):
        """ Test sale order has the correct delivery carrier """
        self._helper_create_chunk(self.chunk_vals)
        self.assertEqual(
            self.get_created_sales().carrier_id,
            self.env.ref("delivery.normal_delivery_carrier"),
        )

    def test_delivery_carrier_charges_applied(self):
        """ Test delivery line is created with correct amount """
        self._helper_create_chunk(self.chunk_vals)
        delivery_line = self.get_created_sales().order_line.filtered(
            lambda r: r.is_delivery
        )
        self.assertEqual(len(delivery_line.ids), 1)
        equal_delivery = float_compare(
            delivery_line.price_total, 10.9, precision_digits=2
        )
        self.assertEqual(equal_delivery, 0)

    def test_deliver_country_with_tax(self):
        """ Test fiscal position and tax is applied correctly
        to the delivery line """
        chunk_vals = self.chunk_vals
        chunk_vals["data_str"]["address_shipping"]["country_code"] = "CH"
        self._helper_create_chunk(chunk_vals)
        delivery_line = self.get_created_sales().order_line.filtered(
            lambda r: r.is_delivery
        )
        self.assertEqual(delivery_line.tax_id, self.tax_swiss)

    def test_deliver_line_name(self):
        """ Test description is applied, or fallback on default
         carrier description """
        chunk_vals1, chunk_vals2 = self.chunk_vals, self.chunk_vals
        chunk_vals2["data_str"]["payment"]["reference"] = "PMT-002"
        del chunk_vals2["data_str"]["delivery_carrier"]["description"]
        self._helper_create_chunk(chunk_vals1)
        delivery_line = self.get_created_sales().order_line.filtered(
            lambda r: r.is_delivery
        )
        self.assertEqual(delivery_line.name, "CustomDescription")
        self._helper_create_chunk(chunk_vals2)
        delivery_line = self.get_created_sales()[0].order_line.filtered(
            lambda r: r.is_delivery
        )
        self.assertEqual(delivery_line.name, "Normal Delivery Charges")
