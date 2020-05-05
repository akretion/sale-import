# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tools import float_compare

from .common_sale_order_import import SaleImportCase


class TestSaleOrderDatamodel(SaleImportCase):
    def setUp(self):
        super().setUp()

    def test_basic_syntax_validation(self):
        lines = [self.line_valid_1, self.line_valid_2]
        json_import = {
            "address_customer": self.addr_customer_minimum,
            "address_shipping": self.addr_shipping_minimum,
            "address_invoicing": self.addr_invoicing_minimum,
            "lines": lines,
            "amount": self.amount_valid,
            "channel_id": self.sale_channel_ebay.name,
        }
        self.env.datamodels["sale.order"].validate(json_import)

    def test_basic_syntax_validation_errors(self):
        lines = [self.line_invalid]
        json_import = {
            "address_customer": self.addr_customer_missing_field,
            "address_shipping": self.addr_shipping_missing_field,
            "address_invoicing": self.addr_invoicing_missing_field,
            "lines": lines,
            "amount": self.amount_valid,
        }
        result = self.env.datamodels["sale.order"].validate(json_import)
        for el in (
            "address_customer",
            "address_shipping",
            "address_invoicing",
            "lines",
        ):
            self.assertIn(el, result.keys())

    def test_sale_order_import_workflow(self):  # TODO check discount, (taxes)?
        json_import = self.sale_order_example_vals
        sale_order = self.env["sale.order"].process_json_import(json_import)
        self._check_so_partners_updated(sale_order, json_import)
        self._check_so_onchanges_applied(sale_order, json_import)
        self._check_binding_created(sale_order)
        self._check_delivery_carrier_charges_applied(sale_order, json_import)
        sale_order.action_confirm()

    def _check_so_partners_updated(self, sale_order, values):
        def check_record_vals(record, vals_dict):
            simple_compare = ["name", "street", "street2", "zip", "city"]
            for field in simple_compare:
                self.assertEqual(getattr(record, field), vals_dict.get(field))
            m2o_mapping = {
                "state_id": ("code", "state_code", "res.country.state"),
                "country_id": ("code", "country_code", "res.country"),
            }
            for field, v in m2o_mapping.items():
                so_m2o_val = getattr(record, field).id
                expected_value_search_param = v[0]
                expected_value_search_value = vals_dict.get(v[1])
                model = v[2]
                if not expected_value_search_value:
                    continue
                expected_value = (
                    self.env[model]
                    .search(
                        [
                            (
                                expected_value_search_param,
                                "=",
                                expected_value_search_value,
                            )
                        ]
                    )
                    .id
                )
                if so_m2o_val:
                    self.assertEqual(so_m2o_val, expected_value)
                else:
                    self.assertFalse(expected_value)

        record_example_mappings = {
            "partner_id": values["address_customer"],
            "partner_shipping_id": values["address_shipping"],
            "partner_invoice_id": values["address_invoicing"],
        }
        for partner, data_example in record_example_mappings.items():
            check_record_vals(getattr(sale_order, partner), data_example)

    def _check_so_onchanges_applied(self, sale_order, values):
        # check tax applied on first line
        first_line = sale_order.order_line[0]
        second_line = sale_order.order_line[1]
        self.assertEqual(first_line.tax_id, self.tax)
        self.assertEqual(second_line.tax_id, self.env["account.tax"])
        # check description applied on line
        self.assertEqual(first_line.name, self.line_valid_1["description"])
        expected_desc = (
            "[" + self.product_deliver.default_code + "] " + self.product_deliver.name
        )
        self.assertEqual(second_line.name, expected_desc)

    def _check_binding_created(self, sale_order):
        binding = self.env["res.partner.binding"].search([])[-1]
        self.assertEqual(binding.partner_id.id, self.partner_thomasjean.id)
        self.assertEqual(binding.sale_channel_id.id, self.sale_channel_ebay.id)
        self.assertEqual(binding.sale_order_id.id, sale_order.id)

    def _check_delivery_carrier_charges_applied(
        self, sale_order, values
    ):  # TODO confirm it's ok (fpos ?)
        delivery_line = sale_order.order_line.filtered(lambda r: r.is_delivery)
        self.assertTrue(delivery_line)
        delivery_amount = delivery_line.price_total
        expected_delivery_amount = 10.0
        equal_delivery = float_compare(
            delivery_amount, expected_delivery_amount, precision_digits=2
        )
        self.assertEqual(equal_delivery, 0)

    def test_amounts_exception(self):  # TODO not good
        json_import = self.sale_order_example_vals
        json_import["amount"]["amount_total"] += 500.0
        sale_order = self.env["sale.order"].process_json_import(json_import)
        sale_order.action_confirm()