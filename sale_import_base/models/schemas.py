#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from datetime import date
from typing import List, Dict, Optional

from pydantic import BaseModel  # pylint: disable=missing-manifest-dependency

class DeliveryCarrier(BaseModel):
    delivery_type: str
    id_relais: Optional[str]
    price_unit: float


class SaleCustomerConfig(BaseModel):
    prefilled_values: Dict
    product_reference: str


class Address(BaseModel):
    name: str
    street: str
    street2: Optional[str] = None
    zip: str
    city: str
    email: Optional[str]
    state_code: Optional[str]
    country_code: str
    phone: Optional[str]
    mobile: Optional[str]
    company_name: Optional[str]  # obligatoire si pro
    siret: Optional[str]
    delivery_instruction: Optional[str]
    # usefull for invoicing addrss / white label
    external_id: Optional[str]


class Customer(Address):
    external_id: str
    is_pro: Optional[bool]
    pro_reseller: Optional[bool]
    vat: Optional[str]


class SaleOrderLine(BaseModel):
    product_code: Optional[str]
    qty: float
    price_unit: float
    description: Optional[str]
    discount: Optional[float]
    discount: Optional[float]
    customer_configuration: Optional[SaleCustomerConfig]
    product_type: str
    # product code is calculated afterward in odoo
    meta_data: Optional[Dict]
    product_external_ref: Optional[str]


class Amount(BaseModel):
    amount_tax: Optional[float] = None
    amount_untaxed: Optional[float] = None
    amount_total: Optional[float] = None


class Invoice(BaseModel):
    date: date
    number: str


class Payment(BaseModel):
    mode: str
    amount: float
    reference: str
    currency_code: str
    provider_reference: Optional[str]


class SaleOrder(BaseModel):
    name: str
    address_customer: Customer
    address_shipping: Address
    address_invoicing: Address
    lines: List[SaleOrderLine]
    amount: Optional[Amount]
    invoice: Optional[Invoice]
    payment: Optional[Payment]
    pricelist_id: Optional[int]
    date_order: Optional[date]
    payment_method: str
    meta_data: Optional[Dict]
    delivery_carrier: DeliveryCarrier
