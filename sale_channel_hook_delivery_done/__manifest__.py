#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
{
    "name": "Sale Channel Delivery Done",
    "summary": "Adds a hook for when a Sale Order is marked as delivered",
    "version": "14.0.1.0.0",
    "category": "Generic Modules/Sale",
    "author": "Akretion, Odoo Community Association (OCA)",
    "website": "https://github.com/akretion/sale-import",
    "depends": ["sale_channel_hook", "delivery"],
    "license": "AGPL-3",
    "data": ["views/sale_channel.xml"],
    "installable": True,
}
