# Copyright 2020 Akretion
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _si_validate_datamodel(self, datamodel_instance):
        super()._si_validate_datamodel(datamodel_instance)
        self._si_validate_payment(datamodel_instance)

    def _si_validate_payment(self, datamodel_instance):
        pass  # todo

    def _si_finalize(self, new_sale_order, raw_import_data):
        super()._si_finalize(new_sale_order, raw_import_data)
        self._si_create_payment(raw_import_data)

    def _si_create_payment(self, raw_import_data):
        pass  # todo
