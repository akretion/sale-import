#  Copyright (c) Akretion 2020
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from typing import Optional

from extendable_pydantic import ExtendableModelMeta
from pydantic import BaseModel  # pylint: disable=missing-manifest-dependency

from odoo.addons.sale_import_base.models.schemas import SaleOrder


class DeliveryCarrier(BaseModel, metaclass=ExtendableModelMeta):
    code: str
    price_unit: float
    discount: Optional[float] = 0
    description: Optional[str] = None


class ExtendedSaleOrder(SaleOrder, extends=SaleOrder):
    delivery_carrier: Optional[DeliveryCarrier]
