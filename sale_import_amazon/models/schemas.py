#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from typing import List, Optional

from extendable_pydantic import ExtendableModelMeta
from odoo.addons.sale_import_base.models.schemas import SaleOrder


class SaleOrder(SaleOrder):
    # FIXME: not working (field not added to the SaleOrder schema)
    is_fulfilled_by_amazon: Optional[bool] = False
    state: Optional[str] = None
