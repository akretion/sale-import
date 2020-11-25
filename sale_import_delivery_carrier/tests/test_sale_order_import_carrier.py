#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.tools import float_compare

from odoo.addons.sale_import_base.tests.common_sale_order_import import SaleImportCase


class TestSaleOrderImport(SaleImportCase):
    @classmethod
    def patch_vals_carrier(cls, chunk_vals, which_data):
        if which_data in ("all"):
            chunk_vals["data_str"]["delivery_carrier"] = {
                "name": "Normal Delivery Charges",
                "price_unit": 10.0,
                "discount": 0.0,
                "description": "CustomDescription",
            }
        elif which_data in ("mixed", "minimum"):
            chunk_vals["data_str"]["delivery_carrier"] = {
                "name": "Normal Delivery Charges",
                "price_unit": 10.0,
            }
        else:
            raise NotImplementedError
        return chunk_vals

    @classmethod
    def get_chunk_vals(cls, which_data):
        vals = super().get_chunk_vals(which_data)
        return cls.patch_vals_carrier(vals, which_data)

    def setUp(self):
        super().setUp()
        self.env.ref(
            "delivery.product_product_delivery_normal"
        ).taxes_id = self.tax_sale_a

    def test_basic_all(self):
        self._helper_create_chunk(self.get_chunk_vals("all"))

    def test_basic_mixed(self):
        self._helper_create_chunk(self.get_chunk_vals("mixed"))

    def test_basic_minimum(self):
        self._helper_create_chunk(self.get_chunk_vals("minimum"))

    def test_delivery_carrier_id(self):
        """ Test sale order has the correct delivery carrier """
        self._helper_create_chunk(self.get_chunk_vals("all"))
        self.assertEqual(
            self.get_created_sales().carrier_id,
            self.env.ref("delivery.normal_delivery_carrier"),
        )

    def test_delivery_empty_charges(self):
        """ Test when total delivery price == 0, no line is created """
        vals = self.get_chunk_vals("all")
        vals["data_str"]["delivery_carrier"]["price_unit"] = 0.00
        self._helper_create_chunk(vals)
        delivery_line = self.get_created_sales().order_line.filtered(
            lambda r: r.is_delivery
        )
        self.assertEqual(len(delivery_line.ids), 0)

    def test_delivery_carrier_charges_applied(self):
        """ Test delivery line is created with correct amount """
        self._helper_create_chunk(self.get_chunk_vals("all"))
        delivery_line = self.get_created_sales().order_line.filtered(
            lambda r: r.is_delivery
        )
        self.assertEqual(len(delivery_line.ids), 1)
        equal_delivery = float_compare(
            delivery_line.price_total, 11.5, precision_digits=2
        )
        self.assertEqual(equal_delivery, 0)

    def test_deliver_country_with_tax(self):
        """Test fiscal position and tax is applied correctly
        to the delivery line"""
        chunk_vals = self.get_chunk_vals("all")
        self.fiscal_pos_a.country_id = self.env.ref("base.ch")
        chunk_vals["data_str"]["address_shipping"]["country_code"] = "CH"
        del chunk_vals["data_str"]["address_shipping"]["state_code"]
        self._helper_create_chunk(chunk_vals)
        delivery_line = self.get_created_sales().order_line.filtered(
            lambda r: r.is_delivery
        )
        self.assertEqual(delivery_line.tax_id, self.tax_sale_b)

    def test_deliver_line_name(self):
        """Test description is applied, or fallback on default
        carrier description"""
        chunk_vals1, chunk_vals2 = (
            self.get_chunk_vals("all"),
            self.get_chunk_vals("all"),
        )
        chunk_vals2["data_str"]["payment"]["reference"] = "PMT-EXAPLE-002"
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
