#  Copyright (c) Akretion 2020
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

{
    "name": "Sale Import Delivery Carrier",
    "summary": "Adds delivery carrier functionality to Sale Imports",
    "version": "14.0.1.0.0",
    "category": "Generic Modules/Sale",
    "author": "Akretion, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-channel",
    "depends": ["sale_import_base", "delivery_carrier_info"],
    "license": "AGPL-3",
    "data": [],
    "installable": False,
    "external_dependencies": {"python": ["marshmallow_objects"]},
}
