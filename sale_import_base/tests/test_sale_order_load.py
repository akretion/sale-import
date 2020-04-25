# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.datamodel.tests.common import TransactionDatamodelCase


class TestSaleOrderDatamodel(TransactionDatamodelCase):
    """Tests datamodel-level validation"""

    def setUp(self):
        super().setUp()
        self._setup_data()

    # def test_basic_syntax_validation(self):
    #     lines = [self.line_valid_1, self.line_valid_2]
    #     json_import = {
    #         "address_customer": self.addr_customer_minimum,
    #         "address_shipping": self.addr_shipping_minimum,
    #         "address_invoicing": self.addr_invoicing_minimum,
    #         "lines": lines,
    #         "amount": self.amount_valid,
    #     }
    #     self.env.datamodels["sale.order"].validate(json_import)
    #
    # def test_basic_syntax_validation_errors(self):
    #     lines = [self.line_invalid]
    #     json_import = {
    #         "address_customer": self.addr_customer_missing_field,
    #         "address_shipping": self.addr_shipping_missing_field,
    #         "address_invoicing": self.addr_invoicing_missing_field,
    #         "lines": lines,
    #         "amount": self.amount_valid,
    #     }
    #     with self.assertRaises(ValidationError):
    #         self.env.datamodels["sale.order"].validate(json_import)

    def test_sale_order_created(self):
        json_import = self.sale_order_example
        sale_order = self.env["sale.order"].process_json_import(json_import)
        self._check_expected_values(sale_order, json_import)

    def _check_expected_values(self, sale_order, values):
        self._check_partners_updated(sale_order, values)
        self._check_onchanges_applied(sale_order, values)

    def _check_partners_updated(self, sale_order, values):
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

    def _check_onchanges_applied(self, sale_order, values):
        # TODO
        pass

    def _setup_data(self):
        self.partner_thomasjean = self.env["res.partner"].create(
            {
                "name": "Thomas Jean",
                "email": "thomasjean@gmail.com",
                "street": "initial address",
                "street2": "initial address2",
                "zip": "0",
                "city": "initial city",
                "country_id": self.env.ref("base.fr").id,
            }
        )
        self.addr_customer_minimum = {
            "name": "Thomas Jean",
            "street": "1 rue de xyz",
            # street2: not required
            "zip": "69100",
            "city": "Lyon",
            "email": "thomasjean@gmail.com",
            # state_code: not required
            # "state_code": 69001,
            "country_code": "FR",
        }
        self.addr_shipping_minimum = {
            "name": "does not matter",
            "street": "2 rue de xyz",
            "zip": "69100",
            # street2: not required
            "city": "Lyon",
            # email: not required
            # state_code: not required
            "country_code": "FR",
        }
        self.addr_invoicing_minimum = {
            "name": "does not matter",
            "street": "3 rue de xyz",
            "zip": "69100",
            # street2: not required
            "city": "Lyon",
            # email: not required
            # state_code: not required
            "country_code": "FR",
        }
        self.addr_customer_example = {
            "name": "Thomas Jean",
            "street": "1 rue de Jean",
            "street2": "bis",
            "zip": "69100",
            # 'state_code': 'CR-SJ',
            "city": "Lyon",
            "email": "thomasjean@gmail.com",
            "country_code": "FR",
        }
        self.addr_shipping_example = {
            "name": "shipping contact name",
            "street": "2 rue de shipping",
            "street2": "bis",
            "zip": "69100",
            # 'state_code': 'CR-SJ',
            "city": "Lyon",
            "email": "not-required@not-required.com",
            "country_code": "FR",
        }
        self.addr_invoicing_example = {
            "name": "invoicing contact name",
            "street": "3 rue de invoicing",
            "street2": "bis",
            "zip": "69100",
            "city": "Lyon",
            "email": "whatever@whatever.io",
            # 'state_code': 'CR-SJ',
            "country_code": "FR",
        }
        self.addr_customer_missing_field = {
            "name": "Thomas Jean",
            "street": "1 rue de xyz",
            # street2: not required
            "city": "Lyon",
            "email": "thomasjean@gmail.com",
            # state_code: not required
            # country_code: required, missing
            # external_id: not required
        }
        self.addr_shipping_missing_field = {
            "name": "does not matter",
            # street: required, missing
            # street2: not required
            "city": "Lyon",
            # email: not required
            # state_code: not required
            "country_code": "FR",
            # external_id: not required
        }
        self.addr_invoicing_missing_field = {
            # name: required, missing
            "street": "3 rue de xyz",
            # street2: not required
            "city": "Lyon",
            # email: not required
            # state_code: not required
            "country_code": "FR",
            # external_id: not required
        }
        self.line_valid_1 = {
            "product_code": "FURN_0096",
            "qty": 5,
            "price_unit": 500.0,
            "description": "Some description",
            "discount": 0.0,
        }
        self.line_valid_2 = {
            "product_code": "E-COM10",
            "qty": 2,
            "price_unit": 200.0,
            "description": "",
            "discount": 0.0,
        }
        self.line_invalid = {
            "product_code": "DOES NOT EXIST",
            "qty": 5,
            "price_unit": 500.0,
            "description": "",
            "discount": 0.0,
        }
        self.amount_valid = {
            "amount_tax": 2500.0 * 5 * 0.15,
            "amount_untaxed": 2500.0 * 5,
            "amount_total": 2500.0 * 5 * 1.15,
        }
        self.amount_invalid = {
            # note: this is for syntax check only
            "amount_tax": "this should not",
            "amount_untaxed": "happen",
            "amount_total": dict(),
        }
        self.invoice_history_example = {"date": "1900-12-30", "number": "IN-123"}
        self.sale_order_example = {
            "address_customer": self.addr_customer_example,
            "address_shipping": self.addr_shipping_example,
            "address_invoicing": self.addr_invoicing_example,
            "lines": [self.line_valid_1, self.line_valid_2],
            "amount": self.amount_valid,
            "payment_mode": "Does not matter",
            "transaction_id": 123,
            "status": "Does not matter",
            "invoice": self.invoice_history_example,
        }
