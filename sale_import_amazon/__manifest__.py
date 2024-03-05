# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Connector Amazon",
    "description": """Connect Amazon SP-API with Odoo""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Akretion",
    "website": "http://akretion.com",
    "depends": [
        "sale_stock",
        # https://github.com/akretion/sale-import/
        "sale_import_base",
    ],
    "data": [
        # 'views/amazon_marketplace.xml',
        # 'views/sale_channel.xml',
        # "views/res_partner.xml",
        # "views/sale_order.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
    "installable": True,
    "external_dependencies": {"python": ["python-amazon-sp-api"]},
}
