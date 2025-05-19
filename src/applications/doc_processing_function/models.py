from enum import Enum

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class TaxCatEnum(str, Enum):
    employment_income = 'Employment Income'
    investment_income = 'Investment Income'
    no_tax_income = 'Tax‑Exempt Income'
    other_income = 'Income (Other)'
    business_expense = 'Business Expense'
    medical_expense = 'Medical Expense'
    childcare_expense = 'Childcare Expense'
    other_expense = 'Expense (Other)'


class Classification(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    tax_category: TaxCatEnum = Field(description="Tax-relevant category of a document")
