#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

{
    "name": "Sale Import Delivery Carrier",
    "summary": "Adds delivery carrier functionality to Sale Imports",
    "version": "14.0.1.0.0",
    "category": "Generic Modules/Sale",
    "author": "Akretion, Odoo Community Association (OCA)",
    "website": "https://github.com/akretion/sale-import",
    "depends": ["sale_import_base", "delivery"],
    "license": "AGPL-3",
    "data": [],
    "installable": True,
    "external_dependencies": {"python": ["marshmallow_objects"]},
}
