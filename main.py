from fastapi import FastAPI, HTTPException, status, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from typing import List, Optional
from datetime import datetime, date
import uvicorn
from models import Medicine, MedicineCreate, MedicineUpdate, Category, CategoryCreate
from database import (
    get_database,
    create_medicine,
    get_medicines,
    get_medicine_by_id,
    update_medicine,
    delete_medicine,
    create_category,
    get_categories,
    get_category_by_id,
    delete_category
)

# Initialize FastAPI app
app = FastAPI(
    title="Medicine Management System API",
    description="A comprehensive API for managing medicine inventory with CRUD operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize database connection on startup
@app.on_event("startup")
async def startup_event():
    await get_database()

# Root endpoint - serves the frontend
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main frontend interface"""
    return templates.TemplateResponse("index.html", {"request": request})

# Medicine CRUD Endpoints

@app.post("/api/medicines", response_model=Medicine, status_code=status.HTTP_201_CREATED)
async def create_new_medicine(medicine: MedicineCreate):
    """
    Create a new medicine entry
    
    - **name**: Medicine name (required)
    - **category**: Medicine category (required)
    - **dosage**: Dosage information (required)
    - **manufacturer**: Manufacturer name (required)
    - **expiry_date**: Expiry date in YYYY-MM-DD format (required)
    - **stock_quantity**: Current stock quantity (required)
    - **price**: Price per unit (optional)
    - **description**: Additional description (optional)
    """
    try:
        # Validate expiry date is not in the past
        if medicine.expiry_date <= date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Expiry date must be in the future"
            )
        
        new_medicine = await create_medicine(medicine)
        return new_medicine
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create medicine: {str(e)}"
        )

@app.get("/api/medicines", response_model=List[Medicine])
async def get_all_medicines(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in medicine name or manufacturer"),
    expired: Optional[bool] = Query(None, description="Filter by expiry status")
):
    """
    Retrieve all medicines with optional filtering and pagination
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 1000)
    - **category**: Filter medicines by category
    - **search**: Search medicines by name or manufacturer
    - **expired**: Filter by expiry status (true for expired, false for valid)
    """
    try:
        medicines = await get_medicines(skip=skip, limit=limit, category=category, search=search, expired=expired)
        return medicines
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve medicines: {str(e)}"
        )

@app.get("/api/medicines/{medicine_id}", response_model=Medicine)
async def get_medicine(medicine_id: str):
    """
    Retrieve a specific medicine by ID
    
    - **medicine_id**: The unique identifier of the medicine
    """
    try:
        medicine = await get_medicine_by_id(medicine_id)
        if not medicine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medicine with ID {medicine_id} not found"
            )
        return medicine
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve medicine: {str(e)}"
        )

@app.put("/api/medicines/{medicine_id}", response_model=Medicine)
async def update_existing_medicine(medicine_id: str, medicine_update: MedicineUpdate):
    """
    Update an existing medicine
    
    - **medicine_id**: The unique identifier of the medicine to update
    - Only provided fields will be updated
    """
    try:
        # Validate expiry date if provided
        if medicine_update.expiry_date and medicine_update.expiry_date <= date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Expiry date must be in the future"
            )
        
        updated_medicine = await update_medicine(medicine_id, medicine_update)
        if not updated_medicine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medicine with ID {medicine_id} not found"
            )
        return updated_medicine
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update medicine: {str(e)}"
        )

@app.delete("/api/medicines/{medicine_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_medicine(medicine_id: str):
    """
    Delete a medicine by ID
    
    - **medicine_id**: The unique identifier of the medicine to delete
    """
    try:
        deleted = await delete_medicine(medicine_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medicine with ID {medicine_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete medicine: {str(e)}"
        )

# Category CRUD Endpoints

@app.post("/api/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_new_category(category: CategoryCreate):
    """
    Create a new medicine category
    
    - **name**: Category name (required, unique)
    - **description**: Category description (optional)
    """
    try:
        new_category = await create_category(category)
        return new_category
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create category: {str(e)}"
        )

@app.get("/api/categories", response_model=List[Category])
async def get_all_categories():
    """
    Retrieve all medicine categories
    """
    try:
        categories = await get_categories()
        return categories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve categories: {str(e)}"
        )

@app.get("/api/categories/{category_id}", response_model=Category)
async def get_category(category_id: str):
    """
    Retrieve a specific category by ID
    
    - **category_id**: The unique identifier of the category
    """
    try:
        category = await get_category_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category_id} not found"
            )
        return category
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve category: {str(e)}"
        )

@app.delete("/api/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_category(category_id: str):
    """
    Delete a category by ID
    
    - **category_id**: The unique identifier of the category to delete
    """
    try:
        deleted = await delete_category(category_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete category: {str(e)}"
        )

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint to verify API is running"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Medicine Management System API"
    }

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_level="info"
    )
