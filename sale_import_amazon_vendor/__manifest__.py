# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Amazon Connector for Vendors",
    "summary": """Connect Amazon SP-API with Odoo for Vendors""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Akretion",
    "website": "https://github.com/akretion/sale-import",
    "depends": ["sale_import_amazon_base"],
    "data": [
        "views/sale_channel.xml",
        "views/sale_order.xml",
        "data/amazon_cron.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
    "installable": True,
    "external_dependencies": {"python": ["python-amazon-sp-api"]},
}
