# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
#
# from odoo.addons.datamodel.tests.common import TransactionDatamodelCase
#
#
# class TestSaleOrderDatamodel(TransactionDatamodelCase):
#     """Tests datamodel-level validation"""
#
#     def setUp(self):
#         super().setUp()
#         self.product_id = self.env.ref("product.product_product_4")
#         self.product_code = "FURN_0096"
#         self.product_price = 500.0
#         self._setup_data()
#
#     def test_valid_minimum_info(self):
#         json_import = {
#             "address_customer": self.addr_customer_minimum,
#             "address_shipping": self.addr_shipping_minimum,
#             "address_invoicing": self.addr_invoicing_minimum,
#             "lines": self.content_line_valid,
#             "amount": self.content_amount_valid,
#         }
#         self.env["sale.order"]._process_json_import(json_import)
#         so_dm = self.env.datamodels["sale.order"]
#         load_import_data = so_dm.load(json_import, many=False)
#         dumped_load = load_import_data.dump()
#         self.env.datamodels["sale.order"].validate(json_import)

# def test_valid_full_info(self):
#     # TODO complete
#     json_import = {
#         "address_customer": self.addr_customer_minmum,
#         "address_shipping": self.addr_shipping_minimum,
#         "address_invoicing": self.addr_invoicing_minimum,
#         "line": self.content_line_valid,
#         "amount": self.content_amount_valid,
#     }
#     self.env.datamodels["sale.order"].validate(json_import)
#
# def test_validation_customer(self):
#     json_import = {
#         "address_customer": self.addr_customer_missing_field,
#         "address_shipping": self.addr_shipping_minimum,
#         "address_invoicing": self.addr_invoicing_minimum,
#         "line": self.content_line_valid,
#         "amount": self.content_amount_valid,
#     }
#     self.env.datamodels["sale.order"].validate(json_import)
#
# def test_validation_shipping(self):
#     json_import = {
#         "address_customer": self.addr_customer_minimum,
#         "address_shipping": self.addr_shipping_missing_field,
#         "address_invoicing": self.addr_invoicing_minimum,
#         "line": self.content_line_valid,
#         "amount": self.content_amount_valid,
#     }
#     self.env.datamodels["sale.order"].validate(json_import)
#
# def test_validation_invoicing(self):
#     json_import = {
#         "address_customer": self.addr_customer_minimum,
#         "address_shipping": self.addr_shipping_minimum,
#         "address_invoicing": self.addr_invoicing_missing_field,
#         "line": self.content_line_valid,
#         "amount": self.content_amount_valid,
#     }
#     self.env.datamodels["sale.order"].validate(json_import)
#
# def test_validation_state_code(self):
#     addr_customer_wrong_state = deepcopy(self.addr_customer_minimum)
#     addr_customer_wrong_state["state_code"] = "redcliff"
#     json_import = {
#         "address_customer": addr_customer_wrong_state,
#         "address_shipping": self.addr_shipping_minimum,
#         "address_invoicing": self.addr_invoicing_minimum,
#         "line": self.content_line_valid,
#         "amount": self.content_amount_valid,
#     }
#     self.env.datamodels["sale.order"].validate(json_import)
#
# def test_validation_country_code(self):
#     addr_customer_wrong_country = deepcopy(self.addr_customer_minimum)
#     addr_customer_wrong_country["country_code"] = "matchstick"
#     json_import = {
#         "address_customer": addr_customer_wrong_country,
#         "address_shipping": self.addr_shipping_minimum,
#         "address_invoicing": self.addr_invoicing_minimum,
#         "line": self.content_line_valid,
#         "amount": self.content_amount_valid,
#     }
#     self.env.datamodels["sale.order"].validate(json_import)
#
# def test_validation_product_code(self):
#     content_lines_invalid_product = deepcopy(self.content_line_valid)
#     content_lines_invalid_product[0]["product_code"] = "faceoff"
#     json_import = {
#         "address_customer": self.addr_customer_minimum,
#         "address_shipping": self.addr_shipping_minimum,
#         "address_invoicing": self.addr_invoicing_minimum,
#         "line": content_lines_invalid_product,
#         "amount": self.content_amount_valid,
#     }
#     self.env.datamodels["sale.order"].validate(json_import)
#
# def _setup_data(self):
#     self.partner_thomasjean = self.env["res.partner"].create(
#         {"name": "Thomas Jean", "email": "thomasjean@gmail.com"}
#     )
#     self.addr_customer_minimum = {
#         "name": "Thomas Jean",
#         # !type:no required
#         "street": "1 rue de xyz",
#         # street2: not required
#         "zip": 69100,
#         "city": "Lyon",
#         "email": "thomasjean@gmail.com",
#         # state_code: not required
#         # "state_code": 69001,
#         "country_code": "FR",
#         # external_id: not required
#     }
#     self.addr_shipping_minimum = {
#         "name": "does not matter",
#         # !type: not required
#         "street": "2 rue de xyz",
#         "zip": 69100,
#         # street2: not required
#         "city": "Lyon",
#         # email: not required
#         # state_code: not required
#         "country_code": "FR",
#         # external_id: not required
#     }
#     self.addr_invoicing_minimum = {
#         "name": "does not matter",
#         # !type: not required
#         "street": "3 rue de xyz",
#         "zip": 69100,
#         # street2: not required
#         "city": "Lyon",
#         # email: not required
#         # state_code: not required
#         "country_code": "FR",
#         # external_id: not required
#     }
#     self.addr_customer_missing_field = {
#         "name": "Thomas Jean",
#         # !type: not required
#         "street": "1 rue de xyz",
#         # street2: not required
#         "city": "Lyon",
#         "email": "thomasjean@gmail.com",
#         # state_code: not required
#         # country_code: required, missing
#         # external_id: not required
#     }
#     self.addr_shipping_missing_field = {
#         "name": "does not matter",
#         # !type: not required
#         # street: required, missing
#         # street2: not required
#         "city": "Lyon",
#         # email: not required
#         # state_code: not required
#         "country_code": "FR",
#         # external_id: not required
#     }
#     self.addr_invoicing_missing_field = {
#         # name: required, missing
#         # !type: not required
#         "street": "3 rue de xyz",
#         # street2: not required
#         "city": "Lyon",
#         # email: not required
#         # state_code: not required
#         "country_code": "FR",
#         # external_id: not required
#     }
#     self.content_line_valid = [
#         {
#             "product_code": "FURN_0096",
#             "qty": 5,
#             "price_unit": 500.0,
#             "description": "",
#             "discount": 0.0,
#         }
#     ]
#     self.content_lines_invalid = [
#         {
#             "product_code": "DOES NOT EXIST",
#             "qty": 5,
#             "price_unit": 500.0,
#             "description": "",
#             "discount": 0.0,
#         }
#     ]
#     self.content_amount_valid = {
#         "amount_tax": 2500.0 * 5 * 0.15,
#         "amount_untaxed": 2500.0 * 5,
#         "amount_total": 2500.0 * 5 * 1.15,
#     }
#     self.content_amount_invalid = {
#         "amount_tax": 1.11,
#         "amount_untaxed": 2.22,
#         "amount_total": 8.88,
#     }
