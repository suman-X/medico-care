import os
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import uuid
from models import Medicine, MedicineCreate, MedicineUpdate, Category, CategoryCreate

# In-memory database storage
medicines_db: Dict[str, Dict[str, Any]] = {}
categories_db: Dict[str, Dict[str, Any]] = {}

async def get_database():
    """Initialize and return database connection (in-memory)"""
    # Initialize with some sample categories
    if not categories_db:
        sample_categories = [
            {"name": "antibiotics", "description": "Antibiotic medications"},
            {"name": "antipyretics", "description": "reduce fever"},
            {"name": "painkillers", "description": "Pain relief medications"},
            {"name": "vitamins", "description": "Vitamin supplements"},
            {"name": "antacids", "description": "Stomach acid relief"},
        ]
        
        for cat_data in sample_categories:
            cat_id = str(uuid.uuid4())
            cat_data["_id"] = cat_id
            cat_data["created_at"] = datetime.now()
            cat_data["updated_at"] = datetime.now()
            categories_db[cat_id] = cat_data
    
    return True

async def create_indexes():
    """Create database indexes for better query performance (no-op for in-memory)"""
    pass

async def close_database():
    """Close database connection (no-op for in-memory)"""
    pass

# Medicine CRUD operations

async def create_medicine(medicine: MedicineCreate) -> Medicine:
    """Create a new medicine in the database"""
    await get_database()
    
    medicine_id = str(uuid.uuid4())
    medicine_dict = medicine.model_dump()
    medicine_dict["_id"] = medicine_id
    medicine_dict["created_at"] = datetime.now()
    medicine_dict["updated_at"] = datetime.now()
    
    medicines_db[medicine_id] = medicine_dict
    
    return Medicine(**medicine_dict)

async def get_medicines(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    search: Optional[str] = None,
    expired: Optional[bool] = None
) -> List[Medicine]:
    """Retrieve medicines with optional filtering"""
    await get_database()
    
    # Filter medicines based on criteria
    filtered_medicines = []
    
    for medicine_data in medicines_db.values():
        # Category filter
        if category and medicine_data.get("category", "").lower() != category.lower():
            continue
            
        # Search filter
        if search:
            search_lower = search.lower()
            name_match = search_lower in medicine_data.get("name", "").lower()
            manufacturer_match = search_lower in medicine_data.get("manufacturer", "").lower()
            if not (name_match or manufacturer_match):
                continue
        
        # Expired filter
        if expired is not None:
            expiry_date = medicine_data.get("expiry_date")
            if expiry_date:
                if isinstance(expiry_date, str):
                    expiry_date = date.fromisoformat(expiry_date)
                is_expired = expiry_date <= date.today()
                if expired != is_expired:
                    continue
        
        filtered_medicines.append(medicine_data)
    
    # Sort by name
    filtered_medicines.sort(key=lambda x: x.get("name", ""))
    
    # Apply pagination
    paginated = filtered_medicines[skip:skip + limit]
    
    return [Medicine(**med) for med in paginated]

async def get_medicine_by_id(medicine_id: str) -> Optional[Medicine]:
    """Retrieve a specific medicine by ID"""
    await get_database()
    
    medicine_data = medicines_db.get(medicine_id)
    if medicine_data:
        return Medicine(**medicine_data)
    return None

async def update_medicine(medicine_id: str, medicine_update: MedicineUpdate) -> Optional[Medicine]:
    """Update an existing medicine"""
    await get_database()
    
    if medicine_id not in medicines_db:
        return None
    
    # Prepare update data
    update_data = medicine_update.model_dump(exclude_unset=True)
    
    if not update_data:
        # No fields to update
        return await get_medicine_by_id(medicine_id)
    
    # Update the existing medicine data
    current_data = medicines_db[medicine_id].copy()
    current_data.update(update_data)
    current_data["updated_at"] = datetime.now()
    
    medicines_db[medicine_id] = current_data
    
    return Medicine(**current_data)

async def delete_medicine(medicine_id: str) -> bool:
    """Delete a medicine by ID"""
    await get_database()
    
    if medicine_id in medicines_db:
        del medicines_db[medicine_id]
        return True
    return False

# Category CRUD operations

async def create_category(category: CategoryCreate) -> Category:
    """Create a new category in the database"""
    await get_database()
    
    # Check if category already exists
    for existing_cat in categories_db.values():
        if existing_cat["name"].lower() == category.name.lower():
            raise ValueError(f"Category '{category.name}' already exists")
    
    category_id = str(uuid.uuid4())
    category_dict = category.model_dump()
    category_dict["_id"] = category_id
    category_dict["created_at"] = datetime.now()
    category_dict["updated_at"] = datetime.now()
    
    categories_db[category_id] = category_dict
    
    return Category(**category_dict)

async def get_categories() -> List[Category]:
    """Retrieve all categories"""
    await get_database()
    
    # Sort categories by name
    sorted_categories = sorted(categories_db.values(), key=lambda x: x.get("name", ""))
    
    return [Category(**cat) for cat in sorted_categories]

async def get_category_by_id(category_id: str) -> Optional[Category]:
    """Retrieve a specific category by ID"""
    await get_database()
    
    category_data = categories_db.get(category_id)
    if category_data:
        return Category(**category_data)
    return None

async def delete_category(category_id: str) -> bool:
    """Delete a category by ID"""
    await get_database()
    
    if category_id not in categories_db:
        return False
    
    # Get category name to check for medicines using it
    category = categories_db[category_id]
    category_name = category["name"]
    
    # Check if any medicines use this category
    medicines_using_category = [
        med for med in medicines_db.values() 
        if med.get("category", "").lower() == category_name.lower()
    ]
    
    if medicines_using_category:
        raise ValueError(f"Cannot delete category '{category_name}' because it is used by {len(medicines_using_category)} medicine(s)")
    
    del categories_db[category_id]
    return True
