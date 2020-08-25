#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import _, api, fields, models


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "sale.channel.hook.mixin"]

    sale_channel_id = fields.Many2one("sale.channel", related="sale_id.sale_channel_id")

    @api.multi
    def action_done(self):
        res = super(StockPicking, self).action_done()
        for pick in self:
            pick.trigger_channel_hook("delivery_done", pick)
        return res

    def get_hook_content_delivery_done(self):
        sale = self.sale_id
        pickings_done = all([picking.state == "done" for picking in sale.picking_ids])
        content = None
        if pickings_done:
            content = {"message": _("Delivery complete %s" % sale.name)}
        return content
