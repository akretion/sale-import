# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.exceptions import ValidationError

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
            "channel_id": self.channel_ebay,
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
        with self.assertRaises(ValidationError):  # TODO marshmallow exceptions
            self.env.datamodels["sale.order"].validate(json_import)

    def test_sale_order_created(self):
        json_import = self.sale_order_example
        sale_order = self.env["sale.order"].process_json_import(json_import)
        self.check_expected_values(sale_order, json_import)

    def check_expected_values(self, sale_order, values):
        self.check_partners_updated(sale_order, values)
        self.check_onchanges_applied(sale_order, values)

    def check_partners_updated(self, sale_order, values):
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

    def check_onchanges_applied(self, sale_order, values):
        # TODO
        pass
