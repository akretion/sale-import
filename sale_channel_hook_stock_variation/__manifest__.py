# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Channel Hook Stock Variation",
    "summary": """ On stock variation, trigger notification to external webservice """,
    "version": "14.0.1.0.0",
    "website": "https://github.com/OCA/sale-channel",
    "author": "Akretion,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": False,
    "depends": ["sale_channel_hook", "sale_channel_product", "stock"],
    "data": ["views/product_template.xml", "views/sale_channel.xml"],
    "demo": [],
}
