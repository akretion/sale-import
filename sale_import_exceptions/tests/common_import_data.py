# Copyright 2020 Akretion


def setup_import_data(test):
    test.addr_customer_minimum = {
        "name": "Thomas Jean",
        # !type:no required
        "street": "1 rue de xyz",
        # street2: not required
        "zip": 69100,
        "city": "Lyon",
        "email": "thomasjean@gmail.com",
        # state_code: not required
        "state_code": 69001,
        "country_code": "FR",
        # external_id: not required
    }
    test.addr_shipping_minimum = {
        "name": "does not matter",
        # !type: not required
        "street": "2 rue de xyz",
        "zip": 69100,
        # street2: not required
        "city": "Lyon",
        # email: not required
        # state_code: not required
        "country_code": "FR",
        # external_id: not required
    }
    test.addr_invoicing_minimum = {
        "name": "does not matter",
        # !type: not required
        "street": "3 rue de xyz",
        "zip": 69100,
        # street2: not required
        "city": "Lyon",
        # email: not required
        # state_code: not required
        "country_code": "FR",
        # external_id: not required
    }
    test.addr_customer_missing_field = {
        "name": "Thomas Jean",
        # !type: not required
        "street": "1 rue de xyz",
        # street2: not required
        "city": "Lyon",
        "email": "thomasjean@gmail.com",
        # state_code: not required
        # country_code: required, missing
        # external_id: not required
    }
    test.addr_shipping_missing_field = {
        "name": "does not matter",
        # !type: not required
        # street: required, missing
        # street2: not required
        "city": "Lyon",
        # email: not required
        # state_code: not required
        "country_code": "FR",
        # external_id: not required
    }
    test.addr_invoicing_missing_field = {
        # name: required, missing
        # !type: not required
        "street": "3 rue de xyz",
        # street2: not required
        "city": "Lyon",
        # email: not required
        # state_code: not required
        "country_code": "FR",
        # external_id: not required
    }
    test.content_line_valid = [
        {
            "product_code": "FURN_0096",
            "qty": 5,
            "price_unit": 500.0,
            "description": "",
            "discount": 0.0,
        }
    ]
    test.content_lines_invalid = [
        {
            "product_code": "DOES NOT EXIST",
            "qty": 5,
            "price_unit": 500.0,
            "description": "",
            "discount": 0.0,
        }
    ]
    test.content_amount_valid = {
        "amount_tax": 2500.0 * 5 * 0.15,
        "amount_untaxed": 2500.0 * 5,
        "amount_total": 2500.0 * 5 * 1.15,
    }
    test.content_amount_invalid = {
        "amount_tax": 1.11,
        "amount_untaxed": 2.22,
        "amount_total": 8.88,
    }
