from odoo.addons.datamodel import fields
from odoo.addons.sale_import_base.datamodels.sale_order_address import (
    SaleOrderAddressDatamodel,
)


class AmazonSaleOrderAddressDatamodel(SaleOrderAddressDatamodel):
    _inherit = "sale.order.address"
    external_id = fields.Str()
