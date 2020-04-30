# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Import Base",
    "summary": "Base for importing Sale Orders through a JSON file format",
    "version": "12.0.1.0.0",
    "category": "Generic Modules/Sale",
    "author": "Akretion",
    "website": "https://github.com/akretion/sale-import",
    "depends": [
        "queue_job",
        "sale_partner_version",
        "product_code_unique",
        "datamodel",
        "sale_channel_partner_binding",
    ],
    "license": "AGPL-3",
    "data": [],
    "installable": True,
    "external_dependencies": {"python": ["marshmallow_objects"]},
}
