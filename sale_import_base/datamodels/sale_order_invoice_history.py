# Copyright 2020 Akretion
from odoo.addons.datamodel import fields
from odoo.addons.datamodel.datamodels.base import BaseDatamodel


class SaleOrderInvoiceHistoryDatamodel(BaseDatamodel):
    _name = "sale.order.invoice.history"

    date = fields.Date()
    number = fields.Str()
