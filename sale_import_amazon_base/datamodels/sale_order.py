#  Copyright (c) Akretion 2025
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.addons.datamodel import fields
from odoo.addons.sale_import_base.datamodels.sale_order import SaleOrderDatamodel


class AmazonSaleOrderDatamodel(SaleOrderDatamodel):
    _inherit = "sale.order"

    amazon_marketplace_id = fields.Int()
