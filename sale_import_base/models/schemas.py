#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from datetime import date
from typing import Dict, List, Optional

from extendable_pydantic import ExtendableModelMeta
from pydantic import BaseModel  # pylint: disable=missing-manifest-dependency


class DeliveryCarrier(BaseModel):
    delivery_type: str
    id_relais: Optional[str] = None
    price_unit: float


class SaleCustomerConfig(BaseModel):
    prefilled_values: Dict
    product_reference: str


class Address(BaseModel, metaclass=ExtendableModelMeta):
    name: str
    street: str
    street2: Optional[str] = None
    zip: str
    city: str
    email: Optional[str] = None
    state_code: Optional[str] = None
    country_code: str
    phone: Optional[str] = None
    mobile: Optional[str] = None
    company_name: Optional[str] = None  # obligatoire si pro
    siret: Optional[str] = None
    delivery_instruction: Optional[str] = None
    # usefull for invoicing addrss / white label
    external_id: Optional[str] = None


class Customer(Address):
    external_id: str
    is_pro: Optional[bool] = False
    pro_reseller: Optional[bool] = False
    vat: Optional[str] = None


class SaleOrderLine(BaseModel, metaclass=ExtendableModelMeta):
    # product code is calculated afterward in odoo
    product_code: Optional[str] = None
    qty: float
    price_unit: float
    description: Optional[str] = None
    discount: Optional[float] = None
    customer_configuration: Optional[SaleCustomerConfig] = None
    product_type: str
    meta_data: Optional[Dict] = None
    product_external_ref: Optional[str] = None


class Amount(BaseModel, metaclass=ExtendableModelMeta):
    amount_tax: Optional[float] = None
    amount_untaxed: Optional[float] = None
    amount_total: Optional[float] = None


class Invoice(BaseModel, metaclass=ExtendableModelMeta):
    date: date
    number: str


class Payment(BaseModel, metaclass=ExtendableModelMeta):
    mode: str
    amount: float
    reference: str
    currency_code: str
    provider_reference: Optional[str] = None


class SaleOrder(BaseModel):
    name: str
    address_customer: Customer
    address_shipping: Address
    address_invoicing: Address
    lines: List[SaleOrderLine]
    amount: Optional[Amount] = None
    invoice: Optional[Invoice] = None
    payment: Optional[Payment] = None
    pricelist_id: Optional[int] = None
    date_order: Optional[date] = None
    payment_method: str
    meta_data: Optional[Dict] = None
    delivery_carrier: DeliveryCarrier
