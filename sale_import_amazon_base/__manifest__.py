# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Amazon Connector Base",
    "summary": """Base module to Connect Amazon SP-API with Odoo""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Akretion",
    "website": "https://github.com/akretion/sale-import",
    "depends": [
        "stock",
        # https://github.com/OCA/server-env
        "server_environment",
        # https://github.com/OCA/sale-channel
        "sale_import_base",
    ],
    "data": [
        "views/amazon_marketplace.xml",
        "views/sale_channel.xml",
        "views/sale_order.xml",
        "data/amazon_marketplace.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
    "installable": True,
}
