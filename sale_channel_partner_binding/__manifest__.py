# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Channel Binding",
    "summary": "Bind sale channels to contacts",
    "version": "12.0.1.0.0",
    "category": "Generic Modules/Sale",
    "author": "Akretion",
    "website": "https://github.com/akretion/sale-import",
    "depends": ["sale_channel"],
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/sale_channel.xml",
        "views/res_partner.xml",
        "views/partner_binding.xml",
    ],
    "demo": ["demo/demo.xml"],
}
