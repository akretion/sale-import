from odoo import _, http
from odoo.exceptions import ValidationError


class SaleImportBaseController(http.Controller):
    @http.route(
        "/sale_order/post", type="json", auth="api_key", methods=["POST"]
    )  # TODO test
    def main(self, **kw):
        sale_order_data = kw.get("sale_orders")
        api_key = "todo"
        sale_channel = self.env["sale.channel"].search([("api_key", "=", api_key)])
        if not sale_channel:
            raise ValidationError(_("API key does not map to any sale channel"))
        job_ids = self.env["sale.order"].batch_process_json_imports(
            sale_order_data, sale_channel=sale_channel
        )
        return job_ids
