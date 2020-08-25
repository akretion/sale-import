#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, _, api


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "sale.channel.hook.mixin"]

    @api.multi
    def action_done(self):
        res = super(StockPicking, self).action_done()
        for pick in self:
            pick.trigger_channel_hook("delivery_done", pick)
        return res

    def get_hook_content_delivery_done(self, picking):
        sale = picking.sale_id
        pickings_done = all([picking.state == "done" for picking in sale.picking_ids.mapped("state")])
        if pickings_done:
            message = _("Delivery complete %s" % sale.name)
            content = {"message": message}
        return content
