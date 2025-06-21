// Medicine Management System Frontend JavaScript

class MedicineManager {
    constructor() {
        this.medicines = [];
        this.categories = [];
        this.currentPage = 1;
        this.itemsPerPage = 10;
        this.filters = {
            search: '',
            category: '',
            expired: null
        };
        
        this.init();
    }

    async init() {
        await this.loadCategories();
        await this.loadMedicines();
        this.setupEventListeners();
        this.updateStats();
    }

    setupEventListeners() {
        // Search and filter events
        document.getElementById('searchInput').addEventListener('input', 
            this.debounce((e) => this.handleSearch(e.target.value), 300));
        
        document.getElementById('categoryFilter').addEventListener('change', 
            (e) => this.handleCategoryFilter(e.target.value));
        
        document.getElementById('expiredFilter').addEventListener('change', 
            (e) => this.handleExpiredFilter(e.target.value));
        
        document.getElementById('clearFilters').addEventListener('click', 
            () => this.clearFilters());

        // Form submissions
        document.getElementById('medicineForm').addEventListener('submit', 
            (e) => this.handleMedicineSubmit(e));
        
        document.getElementById('categoryForm').addEventListener('submit', 
            (e) => this.handleCategorySubmit(e));

        // Modal events
        document.getElementById('addMedicineBtn').addEventListener('click', 
            () => this.openMedicineModal());
        
        document.getElementById('addCategoryBtn').addEventListener('click', 
            () => this.openCategoryModal());
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    async loadMedicines() {
        try {
            this.showLoading('medicinesLoading');
            
            const params = new URLSearchParams({
                skip: ((this.currentPage - 1) * this.itemsPerPage).toString(),
                limit: this.itemsPerPage.toString(),
                ...(this.filters.search && { search: this.filters.search }),
                ...(this.filters.category && { category: this.filters.category }),
                ...(this.filters.expired !== null && { expired: this.filters.expired.toString() })
            });

            const response = await fetch(`/api/medicines?${params}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.medicines = await response.json();
            this.renderMedicines();
            this.updateStats();
            
        } catch (error) {
            console.error('Error loading medicines:', error);
            this.showAlert('Error loading medicines. Please try again.', 'danger');
        } finally {
            this.hideLoading('medicinesLoading');
        }
    }

    async loadCategories() {
        try {
            const response = await fetch('/api/categories');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.categories = await response.json();
            this.renderCategoryOptions();
            
        } catch (error) {
            console.error('Error loading categories:', error);
            this.showAlert('Error loading categories. Please try again.', 'danger');
        }
    }

    renderMedicines() {
        const tbody = document.getElementById('medicinesTableBody');
        
        if (this.medicines.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="8" class="text-center py-4">
                        <div class="empty-state">
                            <i class="fas fa-pills"></i>
                            <h4>No medicines found</h4>
                            <p>Try adjusting your search filters or add a new medicine.</p>
                        </div>
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = this.medicines.map(medicine => {
            const expiryDate = new Date(medicine.expiry_date);
            const today = new Date();
            const isExpired = expiryDate <= today;
            const isLowStock = medicine.stock_quantity <= 10;
            
            const rowClass = isExpired ? 'expired-medicine' : (isLowStock ? 'low-stock' : '');
            
            return `
                <tr class="${rowClass}">
                    <td class="fw-semibold">${this.escapeHtml(medicine.name)}</td>
                    <td>
                        <span class="badge badge-secondary">${this.escapeHtml(medicine.category)}</span>
                    </td>
                    <td>${this.escapeHtml(medicine.dosage)}</td>
                    <td>${this.escapeHtml(medicine.manufacturer)}</td>
                    <td>
                        <span class="badge ${isExpired ? 'badge-danger' : 'badge-success'}">
                            ${this.formatDate(medicine.expiry_date)}
                        </span>
                    </td>
                    <td>
                        <span class="badge ${isLowStock ? 'badge-warning' : 'badge-success'}">
                            ${medicine.stock_quantity}
                        </span>
                    </td>
                    <td>${medicine.price ? '$' + parseFloat(medicine.price).toFixed(2) : 'N/A'}</td>
                    <td class="medicine-actions">
                        <button class="btn btn-sm btn-warning" onclick="medicineManager.editMedicine('${medicine.id}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="medicineManager.deleteMedicine('${medicine.id}', '${this.escapeHtml(medicine.name)}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    }

    renderCategoryOptions() {
        const select = document.getElementById('categoryFilter');
        const medicineSelect = document.getElementById('medicineCategory');
        
        const options = this.categories.map(category => 
            `<option value="${category.name}">${this.capitalizeFirst(category.name)}</option>`
        ).join('');
        
        select.innerHTML = '<option value="">All Categories</option>' + options;
        medicineSelect.innerHTML = '<option value="">Select Category</option>' + options;
    }

    updateStats() {
        const totalMedicines = this.medicines.length;
        const expiredMedicines = this.medicines.filter(m => new Date(m.expiry_date) <= new Date()).length;
        const lowStockMedicines = this.medicines.filter(m => m.stock_quantity <= 10).length;
        
        document.getElementById('totalMedicines').textContent = totalMedicines;
        document.getElementById('expiredMedicines').textContent = expiredMedicines;
        document.getElementById('lowStockMedicines').textContent = lowStockMedicines;
    }

    handleSearch(query) {
        this.filters.search = query;
        this.currentPage = 1;
        this.loadMedicines();
    }

    handleCategoryFilter(category) {
        this.filters.category = category;
        this.currentPage = 1;
        this.loadMedicines();
    }

    handleExpiredFilter(value) {
        this.filters.expired = value === '' ? null : value === 'true';
        this.currentPage = 1;
        this.loadMedicines();
    }

    clearFilters() {
        this.filters = { search: '', category: '', expired: null };
        this.currentPage = 1;
        
        document.getElementById('searchInput').value = '';
        document.getElementById('categoryFilter').value = '';
        document.getElementById('expiredFilter').value = '';
        
        this.loadMedicines();
    }

    openMedicineModal(medicine = null) {
        const modal = new bootstrap.Modal(document.getElementById('medicineModal'));
        const form = document.getElementById('medicineForm');
        const title = document.getElementById('medicineModalLabel');
        
        if (medicine) {
            title.textContent = 'Edit Medicine';
            this.populateMedicineForm(medicine);
            form.setAttribute('data-medicine-id', medicine.id);
        } else {
            title.textContent = 'Add New Medicine';
            form.reset();
            form.removeAttribute('data-medicine-id');
        }
        
        modal.show();
    }

    openCategoryModal() {
        const modal = new bootstrap.Modal(document.getElementById('categoryModal'));
        document.getElementById('categoryForm').reset();
        modal.show();
    }

    populateMedicineForm(medicine) {
        document.getElementById('medicineName').value = medicine.name;
        document.getElementById('medicineCategory').value = medicine.category;
        document.getElementById('medicineDosage').value = medicine.dosage;
        document.getElementById('medicineManufacturer').value = medicine.manufacturer;
        document.getElementById('medicineExpiryDate').value = medicine.expiry_date;
        document.getElementById('medicineStockQuantity').value = medicine.stock_quantity;
        document.getElementById('medicinePrice').value = medicine.price || '';
        document.getElementById('medicineDescription').value = medicine.description || '';
    }

    async handleMedicineSubmit(e) {
        e.preventDefault();
        
        const form = e.target;
        const medicineId = form.getAttribute('data-medicine-id');
        const formData = new FormData(form);
        
        const medicineData = {
            name: formData.get('name'),
            category: formData.get('category'),
            dosage: formData.get('dosage'),
            manufacturer: formData.get('manufacturer'),
            expiry_date: formData.get('expiry_date'),
            stock_quantity: parseInt(formData.get('stock_quantity')),
            price: formData.get('price') ? parseFloat(formData.get('price')) : null,
            description: formData.get('description') || null
        };

        try {
            const url = medicineId ? `/api/medicines/${medicineId}` : '/api/medicines';
            const method = medicineId ? 'PUT' : 'POST';
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(medicineData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to save medicine');
            }

            const modal = bootstrap.Modal.getInstance(document.getElementById('medicineModal'));
            modal.hide();
            
            this.showAlert(
                medicineId ? 'Medicine updated successfully!' : 'Medicine added successfully!',
                'success'
            );
            
            await this.loadMedicines();
            
        } catch (error) {
            console.error('Error saving medicine:', error);
            this.showAlert(`Error: ${error.message}`, 'danger');
        }
    }

    async handleCategorySubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const categoryData = {
            name: formData.get('name'),
            description: formData.get('description') || null
        };

        try {
            const response = await fetch('/api/categories', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(categoryData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to create category');
            }

            const modal = bootstrap.Modal.getInstance(document.getElementById('categoryModal'));
            modal.hide();
            
            this.showAlert('Category added successfully!', 'success');
            
            await this.loadCategories();
            
        } catch (error) {
            console.error('Error saving category:', error);
            this.showAlert(`Error: ${error.message}`, 'danger');
        }
    }

    async editMedicine(medicineId) {
        try {
            const response = await fetch(`/api/medicines/${medicineId}`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch medicine details');
            }
            
            const medicine = await response.json();
            this.openMedicineModal(medicine);
            
        } catch (error) {
            console.error('Error fetching medicine:', error);
            this.showAlert('Error loading medicine details. Please try again.', 'danger');
        }
    }

    async deleteMedicine(medicineId, medicineName) {
        if (!confirm(`Are you sure you want to delete "${medicineName}"? This action cannot be undone.`)) {
            return;
        }

        try {
            const response = await fetch(`/api/medicines/${medicineId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Failed to delete medicine');
            }

            this.showAlert('Medicine deleted successfully!', 'success');
            await this.loadMedicines();
            
        } catch (error) {
            console.error('Error deleting medicine:', error);
            this.showAlert('Error deleting medicine. Please try again.', 'danger');
        }
    }

    showAlert(message, type) {
        const alertContainer = document.getElementById('alertContainer');
        const alertId = 'alert-' + Date.now();
        
        const alertHTML = `
            <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${this.escapeHtml(message)}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        alertContainer.insertAdjacentHTML('beforeend', alertHTML);
        
        // Auto-remove alert after 5 seconds
        setTimeout(() => {
            const alertElement = document.getElementById(alertId);
            if (alertElement) {
                const alert = bootstrap.Alert.getOrCreateInstance(alertElement);
                alert.close();
            }
        }, 5000);
    }

    showLoading(elementId) {
        document.getElementById(elementId).classList.add('show');
    }

    hideLoading(elementId) {
        document.getElementById(elementId).classList.remove('show');
    }

    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }

    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString();
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.medicineManager = new MedicineManager();
});
