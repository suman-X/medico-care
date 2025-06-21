from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import date, datetime

# Medicine Models
class MedicineBase(BaseModel):
    """Base medicine model with common fields"""
    name: str = Field(..., min_length=1, max_length=200, description="Medicine name")
    category: str = Field(..., min_length=1, max_length=100, description="Medicine category")
    dosage: str = Field(..., min_length=1, max_length=100, description="Dosage information (e.g., '500mg', '2 tablets')")
    manufacturer: str = Field(..., min_length=1, max_length=200, description="Manufacturer name")
    expiry_date: date = Field(..., description="Expiry date")
    stock_quantity: int = Field(..., ge=0, description="Available stock quantity")
    price: Optional[float] = Field(None, ge=0, description="Price per unit")
    description: Optional[str] = Field(None, max_length=500, description="Additional description")

    @field_validator('name', 'manufacturer')
    def validate_text_fields(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or contain only whitespace')
        return v.strip().title()

    @field_validator('category')
    def validate_category(cls, v):
        if not v or not v.strip():
            raise ValueError('Category cannot be empty')
        return v.strip().lower()

    @field_validator('dosage')
    def validate_dosage(cls, v):
        if not v or not v.strip():
            raise ValueError('Dosage cannot be empty')
        return v.strip()

    @field_validator('expiry_date')
    def validate_expiry_date(cls, v):
        if v <= date.today():
            raise ValueError('Expiry date must be in the future')
        return v

class MedicineCreate(MedicineBase):
    """Model for creating a new medicine"""
    pass

class MedicineUpdate(BaseModel):
    """Model for updating an existing medicine"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    dosage: Optional[str] = Field(None, min_length=1, max_length=100)
    manufacturer: Optional[str] = Field(None, min_length=1, max_length=200)
    expiry_date: Optional[date] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=500)

    @field_validator('name', 'manufacturer')
    def validate_text_fields(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Field cannot be empty or contain only whitespace')
            return v.strip().title()
        return v

    @field_validator('category')
    def validate_category(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Category cannot be empty')
            return v.strip().lower()
        return v

    @field_validator('dosage')
    def validate_dosage(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Dosage cannot be empty')
            return v.strip()
        return v

class Medicine(MedicineBase):
    """Complete medicine model with ID and timestamps"""
    id: Optional[str] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

# Category Models
class CategoryBase(BaseModel):
    """Base category model"""
    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    description: Optional[str] = Field(None, max_length=300, description="Category description")

    @field_validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Category name cannot be empty')
        return v.strip().lower()

class CategoryCreate(CategoryBase):
    """Model for creating a new category"""
    pass

class Category(CategoryBase):
    """Complete category model with ID and timestamps"""
    id: Optional[str] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
