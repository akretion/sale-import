#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from typing import Optional

from odoo.addons.sale_import_base.models.schemas import SaleOrder


class ExtendedSaleOrder(SaleOrder, extends=SaleOrder):
    is_fulfilled_by_amazon: Optional[bool] = False
    amazon_marketplace_id: Optional[int] = False
    state: Optional[str] = None
