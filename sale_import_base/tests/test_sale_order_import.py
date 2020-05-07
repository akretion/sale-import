# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from copy import deepcopy

from odoo.exceptions import ValidationError

from .common_sale_order_import import SaleImportCase


class TestSaleOrderImport(SaleImportCase):
    def setUp(self):
        super().setUp()

    def test_invalid_json(self):
        """ An invalid input will stop the job """
        json_import = deepcopy(self.sale_order_example_vals)
        del json_import["address_customer"]["street"]
        del json_import["address_invoicing"]["zip"]
        del json_import["address_shipping"]["country_code"]
        json_import["lines"][0] = self.line_invalid
        with self.assertRaises(ValidationError):
            self.env["sale.order"].process_json_import(json_import)

    def test_create_partner(self):
        """ If we can't match a partner on 1. external id
        or 2. email (optional), create a new one. """
        json_import = deepcopy(self.sale_order_example_vals)
        json_import["address_customer"] = {
            "name": "Nicolas Cage",
            "street": "1",
            "street2": "bis",
            "zip": "22121",
            "city": "New Orleans",
            "email": "nicolas.cage@aol.com",
            "country_code": "US",
            "external_id": "AMZN_NICCAGE",
        }
        json_import["address_invoicing"] = {
            "name": "Nicolas Cage",
            "street": "2",
            "street2": "bis",
            "zip": "22121",
            "city": "Somerset",
            "country_code": "GB",
        }
        json_import["address_shipping"] = {
            "name": "Nicolas Cage",
            "street": "3",
            "street2": "bis",
            "zip": "22121",
            "city": "Oberpfaltz",
            "country_code": "DE",
        }
        self.env["sale.order"].process_json_import(json_import)
        customer = self.env["res.partner"].search([], order="id desc")[2]
        shipping = self.env["res.partner"].search([], order="id desc")[1]
        invoicing = self.env["res.partner"].search([], order="id desc")[0]
        self.assertEqual(customer.street, "1")
        self.assertEqual(invoicing.street, "2")
        self.assertEqual(shipping.street, "3")
        self.assertEqual(invoicing.parent_id, customer)
        self.assertEqual(shipping.parent_id, customer)

    def test_import_existing_partner_match_external_id(self):
        """ During import, if a partner is matched, his
         address is updated """
        json_import = deepcopy(self.sale_order_example_vals)
        del json_import["address_customer"]["email"]
        new_sale_order = self.env["sale.order"].process_json_import(json_import)
        self.assertEqual(new_sale_order.partner_id, self.partner_thomasjean)

    def test_import_existing_partner_match_email(self):
        """ If sale channel allows it and there is no match
        on external_id, we can match partner on email """
        json_import = deepcopy(self.sale_order_example_vals)
        del json_import["address_customer"]["external_id"]
        new_sale_order = self.env["sale.order"].process_json_import(json_import)
        self.assertEqual(new_sale_order.partner_id, self.partner_thomasjean)

    def test_import_existing_partner_match_email_not_allowed(self):
        """ DISCUSSION on en revient à créér un nouveau partner
        1. pas match sur external_id -> 2. pas match sur email -> create. Mais
        on risque d'avoir des conflits avec des partner dont l'email existe déjà"""
        json_import = deepcopy(self.sale_order_example_vals)
        del json_import["address_customer"]["external_id"]
        new_sale_order = self.env["sale.order"].process_json_import(json_import)
        for field in ("name", "street", "email", "city"):
            self.assertEqual(
                getattr(new_sale_order.partner_id, field),
                self.addr_customer_example[field],
            )

    def test_product_missing(self):
        """ Test product code validation effectively blocks the job """
        json_import = deepcopy(self.sale_order_example_vals)
        for line in json_import["lines"]:
            line["product_code"] = "doesn't exist"
        with self.assertRaises(ValidationError):
            self.env["sale.order"].process_json_import(json_import)

    def test_product_search(self):
        """ Check we get the right product match on product code"""
        json_import = deepcopy(self.sale_order_example_vals)
        new_sale_order = self.env["sale.order"].process_json_import(json_import)
        self.assertEqual(new_sale_order.order_line[0].product_id, self.product_order)
        self.assertEqual(new_sale_order.order_line[1].product_id, self.product_deliver)

    def test_wrong_total_amount(self):
        """ Test the sale.exception works as intended """
        json_import = deepcopy(self.sale_order_example_vals)
        json_import["amount"]["amount_total"] += 500.0
        new_sale_order = self.env["sale.order"].process_json_import(json_import)
        with self.assertRaises(ValidationError):
            new_sale_order._check_exception()

    def test_wrong_total_amount_tax(self):
        """ Test the sale.exception works as intended """
        json_import = deepcopy(self.sale_order_example_vals)
        json_import["amount"]["amount_tax"] += 500.0
        new_sale_order = self.env["sale.order"].process_json_import(json_import)
        with self.assertRaises(ValidationError):
            new_sale_order._check_exception()

    def test_order_country_with_tax(self):
        """ Test fiscal position is applied correctly
        in case the destination country has tax """
        json_import = deepcopy(self.sale_order_example_vals)
        json_import["address_shipping"]["country_code"] = "CH"
        new_sale_order = self.env["sale.order"].process_json_import(json_import)
        self.assertEqual(new_sale_order.order_line[0].tax_id, self.tax_swiss)

    def test_order_country_without_tax(self):
        """ Test fiscal position is applied correctly
        in case the destination country has no tax """
        json_import = deepcopy(self.sale_order_example_vals)
        json_import["address_shipping"]["country_code"] = "DE"
        new_sale_order = self.env["sale.order"].process_json_import(json_import)
        self.assertEqual(new_sale_order.order_line[0].tax_id, self.env["account.tax"])

    ### DISCUSSION Tests rajoutés
    def test_import_existing_partner_update_addresses(self):
        """ During import, if a partner is matched, his
         address is updated """
        json_import = deepcopy(self.sale_order_example_vals)
        self.env["sale.order"].process_json_import(json_import)
        json_import["address_customer"]["street"] = "new val customer"
        json_import["address_invoicing"]["street"] = "new val invoicing"
        new_sale_order = self.env["sale.order"].process_json_import(json_import)
        self.assertEqual(new_sale_order.partner_id.street, "new val customer")
        self.assertEqual(new_sale_order.partner_invoice_id.street, "new val invoicing")
        self.assertEqual(new_sale_order.partner_shipping_id.street, "2 rue de shipping")

    def test_order_line_description(self):
        """ Test that a description is taken into account, or
        default description is generated if none is provided """
        json_import = deepcopy(self.sale_order_example_vals)
        new_sale_order = self.env["sale.order"].process_json_import(json_import)
        self.assertEqual(
            new_sale_order.order_line[0].name, json_import["lines"][0]["description"]
        )
        expected_desc = (
            "[" + self.product_deliver.default_code + "] " + self.product_deliver.name
        )
        self.assertEqual(new_sale_order.order_line[1].name, expected_desc)

    def test_partner_binding(self):
        """ Test that a binding is created whenever a customer
        is matched or created """
        json_import = deepcopy(self.sale_order_example_vals)
        new_sale_order = self.env["sale.order"].process_json_import(json_import)
        binding = self.env["res.partner.binding"].search([])[-1]
        self.assertEqual(binding.sale_channel_id, self.sale_channel_ebay)
        self.assertEqual(binding.partner_id, self.partner_thomasjean)
        self.assertEqual(
            binding.external_id, json_import["address_customer"]["external_id"]
        )

    def test_currency_code(self):
        """ DISCUSSION """
        pass

    def test_payment_xyz(self):
        """ DISCUSSION"""
        pass
