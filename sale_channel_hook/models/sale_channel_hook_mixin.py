# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleChannelHookMixin(models.AbstractModel):
    _name = "sale.channel.hook.mixin"

    def trigger_channel_hook(self, hook_name, *args):
        for rec in self:
            if rec.channel_id:
                hook_content_getter = rec.getattr("_get_hook_content_" + hook_name)
                content = hook_content_getter(args)
                rec.channel_id.send_hook_api_request(hook_name, content)
