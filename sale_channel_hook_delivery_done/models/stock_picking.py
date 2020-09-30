#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "sale.channel.hook.mixin"]

    sale_channel_id = fields.Many2one("sale.channel", related="sale_id.sale_channel_id")

    def _prepare_hook_tracking(self, package):
        return {"number": package.name}

    def _hook_should_trigger_notif(self):
        must_trigger = (
            self.picking_type_id in self.sale_channel_id.hook_picking_type_ids
        ) and self.sale_channel_id.hook_active_delivery_done
        return must_trigger

    @api.multi
    def action_done(self):
        res = super(StockPicking, self).action_done()
        for pick in self:
            if pick._hook_should_trigger_notif():
                pick.trigger_channel_hook("delivery_done", pick)
        return res

    def get_hook_content_delivery_done(self, *args):
        sale = self.sale_id
        content = {
            "sale_name": sale.name,
            "picking": self.name,
            "carrier": sale.carrier_id.name,
            "tracking": [
                self._prepare_hook_tracking(package) for package in self.package_ids
            ],
        }
        return content
