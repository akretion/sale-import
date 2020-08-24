# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import hashlib
import hmac

import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class SaleChannelHookMixin(models.AbstractModel):
    _name = "sale.channel.hook.mixin"

    def trigger_hook(self, hook_name, *args):
        for rec in self:
            if rec.channel_id:
                rec.channel_id.execute_hook(hook_name, args)