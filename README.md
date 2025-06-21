# Medicine Management System

A comprehensive FastAPI-based medicine management system featuring custom APIs for CRUD operations and an interactive web interface for managing medicine inventory.

## Features

### Backend API Features
- **FastAPI Server** with automatic API documentation
- **Complete CRUD Operations** for medicines and categories
- **Advanced Filtering & Search** capabilities
- **Data Validation** using Pydantic models
- **Error Handling** with detailed error messages
- **RESTful API Design** with proper HTTP methods and status codes
- **In-memory Database** for quick setup and testing

### Frontend Features
- **Responsive Web Interface** built with Bootstrap 5
- **Real-time Statistics** showing total, expired, and low-stock medicines
- **Advanced Search & Filtering** with multiple criteria
- **Interactive Forms** for adding and editing medicines
- **Category Management** system
- **Visual Indicators** for expired and low-stock medicines

### API Endpoints

#### Medicine Endpoints
- `GET /api/medicines` - Get all medicines with filtering and pagination
- `POST /api/medicines` - Create a new medicine
- `GET /api/medicines/{medicine_id}` - Get a specific medicine
- `PUT /api/medicines/{medicine_id}` - Update a medicine
- `DELETE /api/medicines/{medicine_id}` - Delete a medicine

#### Category Endpoints
- `GET /api/categories` - Get all categories
- `POST /api/categories` - Create a new category
- `GET /api/categories/{category_id}` - Get a specific category
- `DELETE /api/categories/{category_id}` - Delete a category

#### Utility Endpoints
- `GET /api/health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern, fast web framework
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server
- **In-memory Storage** - Simple data persistence

### Frontend
- **HTML5, CSS3, JavaScript**
- **Bootstrap 5** - UI framework
- **Font Awesome** - Icons
- **Vanilla JavaScript** - No frontend framework dependencies

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- VS Code (recommended)

### Step-by-Step Installation in VS Code

#### 1. Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd medicine-management-system

# Or download and extract the project files
```

#### 2. Open in VS Code
```bash
# Open the project in VS Code
code .

# Or open VS Code and use File > Open Folder to select the project directory
```

#### 3. Create a Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
# Install all required packages
pip install fastapi uvicorn pydantic jinja2 python-multipart

# Or if you have a requirements.txt file:
pip install -r requirements.txt
```

#### 5. Run the Application
```bash
# Start the development server
python main.py

# The server will start on http://localhost:5000
# You can also run with uvicorn directly:
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

#### 6. Access the Application
- **Web Interface**: Open http://localhost:5000 in your browser
- **API Documentation**: Visit http://localhost:5000/docs for interactive API docs
- **Alternative API Docs**: Visit http://localhost:5000/redoc for ReDoc documentation

## Quick Start Guide

### Adding Your First Medicine
1. Open the web interface at http://localhost:5000
2. Click "Add Medicine" button
3. Fill in the required fields:
   - Name (e.g., "Aspirin")
   - Category (select from dropdown)
   - Dosage (e.g., "500mg")
   - Manufacturer (e.g., "Bayer")
   - Expiry Date (future date)
   - Stock Quantity (e.g., 50)
   - Price (optional)
   - Description (optional)
4. Click "Save Medicine"

### Adding Categories
1. Click "Add Category" button
2. Enter category name (e.g., "heart-medication")
3. Add optional description
4. Click "Save Category"

### Using Search and Filters
- **Search**: Type medicine name or manufacturer in the search box
- **Category Filter**: Select a specific category from dropdown
- **Expiry Filter**: Choose to show all, valid, or expired medicines
- **Clear Filters**: Click "Clear" to reset all filters

## API Usage Examples

### Get All Medicines
```bash
curl -X GET "http://localhost:5000/api/medicines"
```

### Create a New Medicine
```bash
curl -X POST "http://localhost:5000/api/medicines" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ibuprofen",
    "category": "painkillers",
    "dosage": "400mg",
    "manufacturer": "Generic Labs",
    "expiry_date": "2025-12-31",
    "stock_quantity": 75,
    "price": 8.99,
    "description": "Anti-inflammatory pain reliever"
  }'
```

### Search Medicines 
```bash
# Search by name or manufacturer
curl -X GET "http://localhost:5000/api/medicines?search=aspirin"

# Filter by category
curl -X GET "http://localhost:5000/api/medicines?category=painkillers"

# Get expired medicines
curl -X GET "http://localhost:5000/api/medicines?expired=true"
```

### Get All Categories
```bash
curl -X GET "http://localhost:5000/api/categories"
```

### Create a New Category
```bash
curl -X POST "http://localhost:5000/api/categories" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "diabetes-medication",
    "description": "Medications for diabetes management"
  }'
```

## Project Structure
```
medicine-management-system/
├── main.py              # FastAPI application and API endpoints
├── models.py            # Pydantic data models
├── database.py          # Database operations (in-memory storage)
├── README.md            # This file
├── templates/
│   └── index.html       # Web interface template
├── static/
│   ├── style.css        # CSS styling
│   └── script.js        # Frontend JavaScript
└── requirements.txt     # Python dependencies
```

## Features Overview

### Medicine Management
- Add new medicines with complete information
- Update existing medicine details
- Delete medicines from inventory
- Search by name or manufacturer
- Filter by category or expiry status
- Track stock quantities and prices

### Category Management
- Create custom medicine categories
- Organize medicines by type
- Prevent deletion of categories in use
- Automatic category validation

### Dashboard Features
- Real-time statistics display
- Expired medicine alerts
- Low stock warnings
- Visual status indicators

## Troubleshooting

### Common Issues

#### Server Won't Start
```bash
# Check if port 5000 is already in use
netstat -an | grep 5000

# Use a different port
uvicorn main:app --port 8000
```

#### Module Not Found Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### API Returns 500 Errors
- Check server logs in the terminal
- Verify all required fields are provided in requests
- Ensure date formats are YYYY-MM-DD

### Development Tips

#### Debugging
- Server logs appear in the terminal running `python main.py`
- Use browser developer tools to inspect frontend errors
- Check the `/docs` endpoint for API documentation

#### Data Persistence
- Current implementation uses in-memory storage
- Data is lost when server restarts
- For production, consider implementing MongoDB integration

#### Customization
- Modify `static/style.css` for UI changes
- Update `static/script.js` for frontend behavior
- Edit `models.py` to add new fields or validation

## API Documentation

The application provides interactive API documentation at:
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

These interfaces allow you to:
- Test API endpoints directly
- View request/response schemas
- Understand parameter requirements
- Generate code examples

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
