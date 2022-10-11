#  Copyright (c) Akretion 2020
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models


class SaleChannelHookMixin(models.AbstractModel):
    _name = "sale.channel.hook.mixin"
    _description = "Mixin for models triggering sale channel hooks"

    def trigger_channel_hook(self, hook_name, *args):
        for rec in self:
            if rec.sale_channel_id:
                hook_content_getter = getattr(rec, "get_hook_content_" + hook_name)
                content = hook_content_getter(args)
                if content is not None:
                    rec.sale_channel_id.with_delay().send_hook_api_request(content)
