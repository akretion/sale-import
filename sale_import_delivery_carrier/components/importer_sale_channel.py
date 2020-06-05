from odoo.addons.component.core import Component


class ImporterSaleChannel(Component):
    _inherit = "importer.sale.channel"

    def _si_finalize(self, sale_order, raw_import_data):
        super()._si_finalize(sale_order, raw_import_data)
        self._si_create_delivery_line(sale_order, raw_import_data)

    def _si_create_delivery_line(self, sale_order, data):
        if not data.get("delivery_carrier"):
            return
        delivery_carrier = self.env["delivery.carrier"].search(
            [("name", "=", data["delivery_carrier"]["name"])]
        )
        if delivery_carrier:
            sale_order.carrier_id = delivery_carrier
            price = data["delivery_carrier"]["price_unit"]
            discount = data["delivery_carrier"]["discount"]
            carrier_line = sale_order._create_delivery_line(delivery_carrier, price)
            carrier_line.discount = discount
            # DISCUSSION: création de la ligne. _create_delivery_line
            # applique les taxes, quid des taxes pour nous notre ligne de delivery ?
        del data["delivery_carrier"]
