from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _si_validate_datamodel(self, datamodel_instance):
        super()._si_validate_datamodel(datamodel_instance)
        self._si_validate_delivery_carrier(datamodel_instance)

    def _si_validate_delivery_carrier(self, datamodel_instance):
        pass  # todo

    def _si_process_m2os(self, so_vals):
        super()._si_process_m2os(so_vals)
        self._si_process_delivery_carrier(so_vals)

    def _si_process_delivery_carrier(self, so_vals):  # todo
        # delivery_carrier = self.env["delivery.carrier"].search(
        #     [("name", "=", so_vals.get("delivery_carrier") and so_vals["delivery_carrier"].get("name"))]
        # )
        # if delivery_carrier:
        #     so_vals["carrier_id"] = delivery_carrier.id
        # del so_vals["delivery_carrier"]
        pass
