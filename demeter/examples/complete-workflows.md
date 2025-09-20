# 🌾 Demeter WAVIS: Complete Workflow Examples

Real-world scenarios demonstrating AI-driven development with SSOT integration.

---

## 📊 Example 1: E-commerce API Development

### Scenario
Building a REST API for an e-commerce platform using Python + FastAPI.

### Project Setup
```bash
# Start new project
./quick-start.sh

# Configuration selected:
# - Name: ecommerce-api
# - Tech Stack: Python + FastAPI
# - Description: E-commerce platform API
```

### SSOT Definition
```yaml
# demeter/core/ssot/framework-requirements.yaml
functional_requirements:
  FR-001:
    title: "Product Management"
    description: "Manage product catalog with CRUD operations"
    priority: "high"
    acceptance_criteria:
      - "Create products with name, price, description"
      - "List products with pagination and filtering"
      - "Update product information"
      - "Delete products (soft delete)"

  FR-002:
    title: "Shopping Cart"
    description: "Users can manage items in shopping cart"
    priority: "high"
    acceptance_criteria:
      - "Add products to cart"
      - "Remove products from cart"
      - "Update quantities"
      - "Calculate total price"

non_functional_requirements:
  NFR-001:
    title: "API Performance"
    description: "API response time requirements"
    requirements:
      - "Product list endpoint: < 200ms"
      - "Cart operations: < 100ms"
      - "Support 1000 concurrent users"

units_of_work:
  UoW-001:
    title: "Product API Endpoints"
    description: "Implement RESTful product management endpoints"
    references: ["FR-001"]
    priority: "high"
    acceptance_criteria:
      - "POST /products - Create product"
      - "GET /products - List products with pagination"
      - "GET /products/{id} - Get product details"
      - "PUT /products/{id} - Update product"
      - "DELETE /products/{id} - Soft delete product"

  UoW-002:
    title: "Shopping Cart Service"
    description: "Implement shopping cart business logic"
    references: ["FR-002"]
    dependencies: ["UoW-001"]
    priority: "high"
```

### AI-Driven Development Session

#### Step 1: Query Requirements
```
/ssot-query product management
```

**Claude Response:**
```
🔍 Query: product management
📊 Found 2 results:

  functional_requirement: FR-001
    Product Management - CRUD operations for product catalog

  unit_of_work: UoW-001
    Product API Endpoints - RESTful product management

📋 Context:
- High priority feature
- Dependencies: None
- Related: Shopping cart functionality
```

#### Step 2: Generate Product API Implementation
```
/generate-implementation UoW-001 --with-tests --with-contracts --tech-stack python-fastapi
```

**Generated Implementation:**

```python
# src/api/products.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ..database import get_db
from ..models.product import Product
from ..schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])

class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    size: int

# Contract: Create Product
# Preconditions: Valid product data, unique name
# Postconditions: Product created, ID returned
@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """Create a new product"""
    # Validate input (contract precondition)
    if not product.name or len(product.name.strip()) == 0:
        raise HTTPException(status_code=400, detail="Product name is required")

    if product.price <= 0:
        raise HTTPException(status_code=400, detail="Product price must be positive")

    # Check for duplicate name
    existing = db.query(Product).filter(Product.name == product.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Product with this name already exists")

    # Create product
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Contract postcondition: Product created with ID
    assert db_product.id is not None, "Product must have ID after creation"

    return db_product

# Contract: List Products with Pagination
# Preconditions: Valid pagination parameters
# Postconditions: Returns paginated results, total count accurate
@router.get("/", response_model=ProductListResponse)
async def list_products(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    search: Optional[str] = Query(None, description="Search in product name"),
    db: Session = Depends(get_db)
):
    """List products with pagination and search"""
    # Build query
    query = db.query(Product).filter(Product.deleted_at.is_(None))

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * size
    products = query.offset(offset).limit(size).all()

    # Contract postcondition: Verify pagination math
    assert len(products) <= size, "Returned items must not exceed page size"

    return ProductListResponse(
        items=products,
        total=total,
        page=page,
        size=size
    )

# Contract: Get Product by ID
# Preconditions: Valid product ID
# Postconditions: Returns product or 404
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID"""
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.deleted_at.is_(None)
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

# Contract: Update Product
# Preconditions: Product exists, valid update data
# Postconditions: Product updated, version incremented
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update product"""
    # Find product
    db_product = db.query(Product).filter(
        Product.id == product_id,
        Product.deleted_at.is_(None)
    ).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Validate update data
    update_data = product_update.dict(exclude_unset=True)

    if "price" in update_data and update_data["price"] <= 0:
        raise HTTPException(status_code=400, detail="Price must be positive")

    # Apply updates
    for field, value in update_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)

    return db_product

# Contract: Soft Delete Product
# Preconditions: Product exists and not already deleted
# Postconditions: Product marked as deleted
@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Soft delete product"""
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.deleted_at.is_(None)
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Soft delete
    from datetime import datetime
    product.deleted_at = datetime.utcnow()
    db.commit()

    return {"message": "Product deleted successfully"}
```

**Generated Tests:**

```python
# tests/test_products.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.main import app
from src.database import get_db
from tests.conftest import TestingSessionLocal

client = TestClient(app)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

class TestProductAPI:
    """Test Product API endpoints mapped to acceptance criteria"""

    def test_create_product_ac1(self):
        """AC: Create products with name, price, description"""
        response = client.post("/products/", json={
            "name": "Test Product",
            "price": 29.99,
            "description": "A test product"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Product"
        assert data["price"] == 29.99
        assert data["id"] is not None

    def test_create_product_validation(self):
        """Contract: Validate input data"""
        # Test empty name
        response = client.post("/products/", json={
            "name": "",
            "price": 29.99
        })
        assert response.status_code == 400

        # Test negative price
        response = client.post("/products/", json={
            "name": "Test Product",
            "price": -10
        })
        assert response.status_code == 400

    def test_list_products_ac2(self):
        """AC: List products with pagination and filtering"""
        # Create test products
        for i in range(15):
            client.post("/products/", json={
                "name": f"Product {i}",
                "price": 10.0 + i
            })

        # Test pagination
        response = client.get("/products/?page=1&size=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10
        assert data["total"] == 15
        assert data["page"] == 1

        # Test search
        response = client.get("/products/?search=Product%201")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= 1

    def test_update_product_ac3(self):
        """AC: Update product information"""
        # Create product
        response = client.post("/products/", json={
            "name": "Original Product",
            "price": 20.0
        })
        product_id = response.json()["id"]

        # Update product
        response = client.put(f"/products/{product_id}", json={
            "name": "Updated Product",
            "price": 25.0
        })

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Product"
        assert data["price"] == 25.0

    def test_delete_product_ac4(self):
        """AC: Delete products (soft delete)"""
        # Create product
        response = client.post("/products/", json={
            "name": "To Be Deleted",
            "price": 15.0
        })
        product_id = response.json()["id"]

        # Delete product
        response = client.delete(f"/products/{product_id}")
        assert response.status_code == 200

        # Verify product is not accessible
        response = client.get(f"/products/{product_id}")
        assert response.status_code == 404
```

#### Step 3: Verify Contracts
```
/verify-contracts UoW-001
```

**Verification Results:**
```
✅ Contract Verification: UoW-001

Product API Endpoints:
├── ✅ POST /products
│   ├── ✅ Preconditions: Input validation implemented
│   ├── ✅ Postconditions: Product created with ID
│   └── ✅ Performance: < 100ms average
├── ✅ GET /products
│   ├── ✅ Preconditions: Pagination parameters validated
│   ├── ✅ Postconditions: Paginated results returned
│   └── ✅ Performance: < 200ms (NFR-001)
├── ✅ GET /products/{id}
│   ├── ✅ Preconditions: Valid ID required
│   └── ✅ Postconditions: Product or 404 returned
├── ✅ PUT /products/{id}
│   ├── ✅ Preconditions: Product exists, valid data
│   └── ✅ Postconditions: Product updated
└── ✅ DELETE /products/{id}
    ├── ✅ Preconditions: Product exists
    └── ✅ Postconditions: Soft delete applied

🎉 All acceptance criteria satisfied!
```

#### Step 4: Implement Shopping Cart
```
/generate-implementation UoW-002 --with-tests --with-contracts
```

**Generated Shopping Cart Service:**

```python
# src/services/cart.py
from typing import List, Dict
from decimal import Decimal
from sqlalchemy.orm import Session

from ..models.cart import CartItem
from ..models.product import Product
from ..schemas.cart import CartItemCreate, CartResponse

class ShoppingCartService:
    """Shopping cart business logic with contract validation"""

    def __init__(self, db: Session):
        self.db = db

    # Contract: Add Product to Cart
    # Preconditions: Product exists, quantity > 0, user authenticated
    # Postconditions: Item added or quantity updated, total recalculated
    def add_to_cart(self, user_id: int, product_id: int, quantity: int) -> CartResponse:
        """Add product to cart"""
        # Validate preconditions
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        # Verify product exists
        product = self.db.query(Product).filter(
            Product.id == product_id,
            Product.deleted_at.is_(None)
        ).first()

        if not product:
            raise ValueError("Product not found")

        # Check if item already in cart
        existing_item = self.db.query(CartItem).filter(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id
        ).first()

        if existing_item:
            # Update quantity
            existing_item.quantity += quantity
        else:
            # Add new item
            new_item = CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
                price=product.price  # Lock in current price
            )
            self.db.add(new_item)

        self.db.commit()

        # Return updated cart
        return self.get_cart(user_id)

    # Contract: Calculate Cart Total
    # Preconditions: Valid user ID
    # Postconditions: Accurate total calculation, includes all valid items
    def get_cart(self, user_id: int) -> CartResponse:
        """Get cart with total calculation"""
        items = self.db.query(CartItem).filter(
            CartItem.user_id == user_id
        ).all()

        # Calculate total
        total = Decimal('0.00')
        item_count = 0

        for item in items:
            item_total = Decimal(str(item.price)) * item.quantity
            total += item_total
            item_count += item.quantity

        # Contract postcondition: Total must be non-negative
        assert total >= 0, "Cart total cannot be negative"

        return CartResponse(
            items=items,
            total=float(total),
            item_count=item_count
        )
```

---

## 🌐 Example 2: Full-Stack React Application

### Scenario
Building a task management app using TypeScript + Next.js.

### Project Setup
```bash
./quick-start.sh

# Configuration:
# - Name: task-manager
# - Tech Stack: TypeScript + Next.js
# - Description: Task management application
```

### AI-Driven Frontend Development

#### Step 1: Query UI Requirements
```
/ssot-query task management interface
```

#### Step 2: Generate React Components
```
/generate-implementation UoW-301 --with-tests --tech-stack typescript-nextjs
```

**Generated Task Component:**

```typescript
// src/components/TaskList.tsx
import React, { useState, useEffect } from 'react';
import { Task, TaskStatus } from '@/types/task';
import { TaskCard } from './TaskCard';
import { TaskForm } from './TaskForm';

interface TaskListProps {
  userId: string;
  onTaskUpdate?: (task: Task) => void;
}

export const TaskList: React.FC<TaskListProps> = ({ userId, onTaskUpdate }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Contract: Load user tasks
  // Preconditions: Valid user ID
  // Postconditions: Tasks loaded or error state set
  useEffect(() => {
    const loadTasks = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch(`/api/tasks?userId=${userId}`);

        if (!response.ok) {
          throw new Error('Failed to load tasks');
        }

        const tasksData = await response.json();
        setTasks(tasksData);

        // Contract postcondition: Tasks array is valid
        console.assert(Array.isArray(tasksData), 'Tasks must be an array');

      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      loadTasks();
    }
  }, [userId]);

  // Contract: Update task status
  // Preconditions: Valid task and status
  // Postconditions: Task updated, UI reflects change
  const handleStatusChange = async (taskId: string, status: TaskStatus) => {
    try {
      const response = await fetch(`/api/tasks/${taskId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
      });

      if (!response.ok) {
        throw new Error('Failed to update task');
      }

      const updatedTask = await response.json();

      // Update local state
      setTasks(prev => prev.map(task =>
        task.id === taskId ? updatedTask : task
      ));

      // Notify parent component
      onTaskUpdate?.(updatedTask);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Update failed');
    }
  };

  if (loading) {
    return <div className="flex justify-center p-4">Loading tasks...</div>;
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        Error: {error}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Tasks</h2>
        <span className="text-gray-600">{tasks.length} tasks</span>
      </div>

      <div className="grid gap-4">
        {tasks.map(task => (
          <TaskCard
            key={task.id}
            task={task}
            onStatusChange={handleStatusChange}
          />
        ))}
      </div>

      {tasks.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No tasks yet. Create your first task!
        </div>
      )}
    </div>
  );
};
```

**Generated Tests:**

```typescript
// src/components/__tests__/TaskList.test.tsx
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TaskList } from '../TaskList';
import { Task, TaskStatus } from '@/types/task';

// Mock fetch
global.fetch = jest.fn();

const mockTasks: Task[] = [
  {
    id: '1',
    title: 'Test Task',
    description: 'Test Description',
    status: TaskStatus.PENDING,
    userId: 'user1',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];

describe('TaskList Component', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  it('loads and displays tasks for user', async () => {
    // Arrange
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    // Act
    render(<TaskList userId="user1" />);

    // Assert - Loading state
    expect(screen.getByText('Loading tasks...')).toBeInTheDocument();

    // Assert - Tasks loaded
    await waitFor(() => {
      expect(screen.getByText('Test Task')).toBeInTheDocument();
    });

    expect(fetch).toHaveBeenCalledWith('/api/tasks?userId=user1');
  });

  it('handles task status update', async () => {
    // Test contract: Update task status
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockTasks
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ ...mockTasks[0], status: TaskStatus.COMPLETED })
      });

    const onTaskUpdate = jest.fn();
    render(<TaskList userId="user1" onTaskUpdate={onTaskUpdate} />);

    await waitFor(() => {
      expect(screen.getByText('Test Task')).toBeInTheDocument();
    });

    // Simulate status change
    const statusButton = screen.getByRole('button', { name: /complete/i });
    await userEvent.click(statusButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/tasks/1', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: TaskStatus.COMPLETED })
      });
    });

    expect(onTaskUpdate).toHaveBeenCalled();
  });

  it('displays error state when loading fails', async () => {
    // Test contract: Error state handling
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

    render(<TaskList userId="user1" />);

    await waitFor(() => {
      expect(screen.getByText(/Error: Network error/)).toBeInTheDocument();
    });
  });

  it('shows empty state when no tasks', async () => {
    // Test contract: Empty state handling
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => []
    });

    render(<TaskList userId="user1" />);

    await waitFor(() => {
      expect(screen.getByText('No tasks yet. Create your first task!')).toBeInTheDocument();
    });
  });
});
```

---

## 🔧 Example 3: Microservice with Go + Gin

### Scenario
Building a notification service microservice using Go + Gin.

### AI-Driven Backend Development

#### Step 1: Generate Go Service
```
/generate-implementation UoW-401 --with-tests --tech-stack go-gin
```

**Generated Notification Service:**

```go
// internal/handlers/notification.go
package handlers

import (
    "net/http"
    "strconv"

    "github.com/gin-gonic/gin"
    "github.com/notification-service/internal/models"
    "github.com/notification-service/internal/services"
)

type NotificationHandler struct {
    service *services.NotificationService
}

func NewNotificationHandler(service *services.NotificationService) *NotificationHandler {
    return &NotificationHandler{service: service}
}

// Contract: Send Notification
// Preconditions: Valid recipient, message not empty, valid type
// Postconditions: Notification queued, ID returned
func (h *NotificationHandler) SendNotification(c *gin.Context) {
    var req models.NotificationRequest

    // Validate input (contract precondition)
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    // Business logic validation
    if req.Recipient == "" {
        c.JSON(http.StatusBadRequest, gin.H{"error": "recipient is required"})
        return
    }

    if req.Message == "" {
        c.JSON(http.StatusBadRequest, gin.H{"error": "message is required"})
        return
    }

    // Send notification through service
    notification, err := h.service.SendNotification(c.Request.Context(), &req)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    // Contract postcondition: Notification has ID
    if notification.ID == "" {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "notification ID not generated"})
        return
    }

    c.JSON(http.StatusCreated, notification)
}

// Contract: Get Notification Status
// Preconditions: Valid notification ID
// Postconditions: Status returned or 404
func (h *NotificationHandler) GetNotificationStatus(c *gin.Context) {
    id := c.Param("id")

    if id == "" {
        c.JSON(http.StatusBadRequest, gin.H{"error": "notification ID is required"})
        return
    }

    notification, err := h.service.GetNotification(c.Request.Context(), id)
    if err != nil {
        if err == services.ErrNotificationNotFound {
            c.JSON(http.StatusNotFound, gin.H{"error": "notification not found"})
            return
        }
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusOK, notification)
}

// Contract: List User Notifications
// Preconditions: Valid user ID, optional pagination
// Postconditions: Paginated list returned
func (h *NotificationHandler) ListUserNotifications(c *gin.Context) {
    userID := c.Param("userId")

    if userID == "" {
        c.JSON(http.StatusBadRequest, gin.H{"error": "user ID is required"})
        return
    }

    // Parse pagination parameters
    page := 1
    limit := 10

    if p := c.Query("page"); p != "" {
        if parsed, err := strconv.Atoi(p); err == nil && parsed > 0 {
            page = parsed
        }
    }

    if l := c.Query("limit"); l != "" {
        if parsed, err := strconv.Atoi(l); err == nil && parsed > 0 && parsed <= 100 {
            limit = parsed
        }
    }

    notifications, total, err := h.service.ListUserNotifications(
        c.Request.Context(),
        userID,
        page,
        limit,
    )
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    response := gin.H{
        "notifications": notifications,
        "total":        total,
        "page":         page,
        "limit":        limit,
    }

    c.JSON(http.StatusOK, response)
}
```

**Generated Tests:**

```go
// internal/handlers/notification_test.go
package handlers_test

import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/gin-gonic/gin"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"

    "github.com/notification-service/internal/handlers"
    "github.com/notification-service/internal/models"
    "github.com/notification-service/internal/services/mocks"
)

func TestNotificationHandler_SendNotification(t *testing.T) {
    // Test contract: Send notification with validation

    gin.SetMode(gin.TestMode)

    t.Run("successful notification send", func(t *testing.T) {
        // Arrange
        mockService := new(mocks.NotificationService)
        handler := handlers.NewNotificationHandler(mockService)

        req := models.NotificationRequest{
            Recipient: "user@example.com",
            Message:   "Test notification",
            Type:      "email",
        }

        expectedNotification := &models.Notification{
            ID:        "notif-123",
            Recipient: req.Recipient,
            Message:   req.Message,
            Type:      req.Type,
            Status:    "queued",
        }

        mockService.On("SendNotification", mock.Anything, &req).
            Return(expectedNotification, nil)

        // Act
        w := httptest.NewRecorder()
        c, _ := gin.CreateTestContext(w)

        reqBody, _ := json.Marshal(req)
        c.Request = httptest.NewRequest("POST", "/notifications", bytes.NewBuffer(reqBody))
        c.Request.Header.Set("Content-Type", "application/json")

        handler.SendNotification(c)

        // Assert
        assert.Equal(t, http.StatusCreated, w.Code)

        var response models.Notification
        err := json.Unmarshal(w.Body.Bytes(), &response)
        assert.NoError(t, err)
        assert.Equal(t, "notif-123", response.ID)
        assert.Equal(t, "queued", response.Status)

        mockService.AssertExpectations(t)
    })

    t.Run("validation error - empty recipient", func(t *testing.T) {
        // Test contract precondition: Valid recipient required

        handler := handlers.NewNotificationHandler(nil)

        req := models.NotificationRequest{
            Recipient: "", // Invalid: empty recipient
            Message:   "Test notification",
            Type:      "email",
        }

        w := httptest.NewRecorder()
        c, _ := gin.CreateTestContext(w)

        reqBody, _ := json.Marshal(req)
        c.Request = httptest.NewRequest("POST", "/notifications", bytes.NewBuffer(reqBody))
        c.Request.Header.Set("Content-Type", "application/json")

        handler.SendNotification(c)

        assert.Equal(t, http.StatusBadRequest, w.Code)

        var response map[string]string
        json.Unmarshal(w.Body.Bytes(), &response)
        assert.Contains(t, response["error"], "recipient is required")
    })

    t.Run("validation error - empty message", func(t *testing.T) {
        // Test contract precondition: Message not empty

        handler := handlers.NewNotificationHandler(nil)

        req := models.NotificationRequest{
            Recipient: "user@example.com",
            Message:   "", // Invalid: empty message
            Type:      "email",
        }

        w := httptest.NewRecorder()
        c, _ := gin.CreateTestContext(w)

        reqBody, _ := json.Marshal(req)
        c.Request = httptest.NewRequest("POST", "/notifications", bytes.NewBuffer(reqBody))
        c.Request.Header.Set("Content-Type", "application/json")

        handler.SendNotification(c)

        assert.Equal(t, http.StatusBadRequest, w.Code)
    })
}

func TestNotificationHandler_GetNotificationStatus(t *testing.T) {
    // Test contract: Get status by valid ID

    gin.SetMode(gin.TestMode)

    t.Run("found notification", func(t *testing.T) {
        mockService := new(mocks.NotificationService)
        handler := handlers.NewNotificationHandler(mockService)

        expectedNotification := &models.Notification{
            ID:     "notif-123",
            Status: "delivered",
        }

        mockService.On("GetNotification", mock.Anything, "notif-123").
            Return(expectedNotification, nil)

        w := httptest.NewRecorder()
        c, _ := gin.CreateTestContext(w)
        c.Params = gin.Params{{Key: "id", Value: "notif-123"}}
        c.Request = httptest.NewRequest("GET", "/notifications/notif-123", nil)

        handler.GetNotificationStatus(c)

        assert.Equal(t, http.StatusOK, w.Code)

        var response models.Notification
        json.Unmarshal(w.Body.Bytes(), &response)
        assert.Equal(t, "notif-123", response.ID)
        assert.Equal(t, "delivered", response.Status)

        mockService.AssertExpectations(t)
    })

    t.Run("notification not found", func(t *testing.T) {
        // Test contract postcondition: 404 when not found

        mockService := new(mocks.NotificationService)
        handler := handlers.NewNotificationHandler(mockService)

        mockService.On("GetNotification", mock.Anything, "nonexistent").
            Return(nil, services.ErrNotificationNotFound)

        w := httptest.NewRecorder()
        c, _ := gin.CreateTestContext(w)
        c.Params = gin.Params{{Key: "id", Value: "nonexistent"}}
        c.Request = httptest.NewRequest("GET", "/notifications/nonexistent", nil)

        handler.GetNotificationStatus(c)

        assert.Equal(t, http.StatusNotFound, w.Code)

        mockService.AssertExpectations(t)
    })
}
```

---

## 📊 Example 4: Performance Optimization Workflow

### Scenario
Optimizing an existing API endpoint that's failing performance requirements.

### Performance Analysis Session

#### Step 1: Identify Performance Issue
```bash
# Run development cycle with performance focus
./demeter/ai/automate-dev-cycle.sh start-feature "API Performance Optimization"
```

#### Step 2: Query Performance Requirements
```
/ssot-query performance requirements API endpoints
```

**Response:**
```
📊 Performance Requirements Found:

NFR-001: API Response Time
- Product listing: < 200ms (95th percentile)
- Search endpoints: < 150ms (95th percentile)
- Authentication: < 100ms (95th percentile)

Current Status: ❌ FAILING
- Product listing: 850ms average
- Search: 1200ms average
```

#### Step 3: Generate Optimization Implementation
```
/generate-implementation UoW-501 --focus performance --tech-stack python-fastapi
```

**Generated Optimization:**

```python
# src/api/optimized_products.py
from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import text
from redis import Redis
import json
from typing import List, Optional

from ..database import get_db
from ..cache import get_redis
from ..models.product import Product
from ..schemas.product import ProductResponse

router = APIRouter(prefix="/products", tags=["products-optimized"])

# Contract: Optimized Product Listing
# Preconditions: Valid pagination, optional filters
# Postconditions: Response time < 200ms, cache utilization
@router.get("/", response_model=List[ProductResponse])
async def list_products_optimized(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Optimized product listing with caching and database optimization"""

    # Build cache key
    cache_key = f"products:page:{page}:size:{size}"
    if category:
        cache_key += f":category:{category}"
    if search:
        cache_key += f":search:{search}"

    # Try cache first (Contract: Utilize caching for performance)
    cached_result = redis.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    # Optimized database query
    query = db.query(Product).filter(Product.deleted_at.is_(None))

    # Use selectinload for eager loading of relationships
    query = query.options(selectinload(Product.category))

    # Apply filters with optimized conditions
    if category:
        query = query.filter(Product.category_id == category)

    if search:
        # Use full-text search if available, otherwise ILIKE
        query = query.filter(
            Product.search_vector.match(search)  # PostgreSQL full-text search
        )

    # Pagination with offset optimization for large datasets
    offset = (page - 1) * size

    # Use raw SQL for better performance on large datasets
    if offset > 10000:  # Switch to cursor-based pagination for large offsets
        # Implementation of cursor-based pagination
        query = query.filter(Product.id > get_last_id_from_previous_page(page, size))
        products = query.limit(size).all()
    else:
        products = query.offset(offset).limit(size).all()

    # Convert to response format
    result = [ProductResponse.from_orm(product) for product in products]

    # Cache the result asynchronously (Contract: Cache for subsequent requests)
    background_tasks.add_task(
        cache_products_result,
        redis,
        cache_key,
        result,
        expire=300  # 5 minutes
    )

    return result

async def cache_products_result(redis: Redis, key: str, data: List[ProductResponse], expire: int):
    """Background task to cache product results"""
    try:
        serialized = json.dumps([item.dict() for item in data])
        redis.setex(key, expire, serialized)
    except Exception as e:
        # Log error but don't fail the request
        print(f"Cache error: {e}")

# Contract: Database Query Optimization
# Preconditions: Valid query parameters
# Postconditions: Optimized query execution plan
def get_optimized_product_query(db: Session, filters: dict) -> str:
    """Generate optimized SQL query based on filters"""

    base_query = """
    SELECT p.id, p.name, p.price, p.description, c.name as category_name
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.id
    WHERE p.deleted_at IS NULL
    """

    conditions = []
    params = {}

    if filters.get('category'):
        conditions.append("p.category_id = :category_id")
        params['category_id'] = filters['category']

    if filters.get('search'):
        conditions.append("p.search_vector @@ plainto_tsquery(:search)")
        params['search'] = filters['search']

    if conditions:
        base_query += " AND " + " AND ".join(conditions)

    base_query += " ORDER BY p.created_at DESC LIMIT :limit OFFSET :offset"

    return base_query, params

# Performance monitoring decorator
def monitor_performance(func):
    """Decorator to monitor API performance"""
    import time
    import functools

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()

        duration = (end_time - start_time) * 1000  # Convert to milliseconds

        # Contract validation: Must meet performance requirement
        if duration > 200:  # 200ms threshold
            print(f"WARNING: {func.__name__} took {duration:.2f}ms (exceeds 200ms threshold)")

        # Log performance metrics
        print(f"API Performance: {func.__name__} completed in {duration:.2f}ms")

        return result

    return wrapper

# Apply performance monitoring
list_products_optimized = monitor_performance(list_products_optimized)
```

**Performance Tests:**

```python
# tests/test_performance.py
import pytest
import time
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

class TestPerformanceRequirements:
    """Test performance contracts for API endpoints"""

    def test_product_listing_performance_nfr001(self):
        """NFR-001: Product listing must respond in < 200ms"""

        # Warm up the endpoint
        client.get("/products/?page=1&size=10")

        # Measure performance
        start_time = time.time()
        response = client.get("/products/?page=1&size=10")
        end_time = time.time()

        # Assertions
        assert response.status_code == 200

        duration_ms = (end_time - start_time) * 1000
        assert duration_ms < 200, f"Product listing took {duration_ms:.2f}ms (requirement: <200ms)"

    def test_search_performance_nfr001(self):
        """NFR-001: Search endpoints must respond in < 150ms"""

        start_time = time.time()
        response = client.get("/products/?search=test")
        end_time = time.time()

        assert response.status_code == 200

        duration_ms = (end_time - start_time) * 1000
        assert duration_ms < 150, f"Search took {duration_ms:.2f}ms (requirement: <150ms)"

    @pytest.mark.parametrize("concurrent_requests", [10, 50, 100])
    def test_concurrent_load_performance(self, concurrent_requests):
        """Test performance under concurrent load"""
        import concurrent.futures
        import statistics

        def make_request():
            start = time.time()
            response = client.get("/products/?page=1&size=10")
            end = time.time()
            return (end - start) * 1000, response.status_code

        # Execute concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
            futures = [executor.submit(make_request) for _ in range(concurrent_requests)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        # Analyze results
        durations = [result[0] for result in results]
        status_codes = [result[1] for result in results]

        # All requests should succeed
        assert all(code == 200 for code in status_codes)

        # 95th percentile should be under 200ms
        p95_duration = statistics.quantiles(durations, n=20)[18]  # 95th percentile
        assert p95_duration < 200, f"95th percentile: {p95_duration:.2f}ms (requirement: <200ms)"
```

#### Step 4: Verify Performance Improvements
```
/verify-contracts UoW-501 --performance
```

**Performance Verification Results:**
```
🚀 Performance Verification: UoW-501

API Optimization Results:
├── ✅ Response Time Requirements
│   ├── ✅ Product listing: 89ms avg (requirement: <200ms)
│   ├── ✅ Search endpoints: 67ms avg (requirement: <150ms)
│   └── ✅ 95th percentile: 145ms (requirement: <200ms)
├── ✅ Caching Implementation
│   ├── ✅ Redis integration active
│   ├── ✅ Cache hit ratio: 78%
│   └── ✅ Background cache refresh
├── ✅ Database Optimization
│   ├── ✅ Query execution plan optimized
│   ├── ✅ Index utilization: 95%
│   └── ✅ Connection pooling efficient
└── ✅ Concurrent Load Handling
    ├── ✅ 100 concurrent requests: ✅
    ├── ✅ 500 concurrent requests: ✅
    └── ✅ No memory leaks detected

🎉 Performance requirements EXCEEDED!
Improvement: 89% reduction in response time
```

---

## 🎯 Key Takeaways

### 1. Consistent Workflow Pattern

Every example follows the same pattern:
1. **Query SSOT** for requirements and context
2. **Generate Implementation** with AI assistance
3. **Verify Contracts** for compliance
4. **Run Tests** to ensure quality
5. **System Verification** for overall health

### 2. Contract-Driven Quality

All implementations include:
- **Precondition validation** at input boundaries
- **Postcondition guarantees** in return values
- **Performance contracts** with measurement
- **Error handling contracts** for failure scenarios

### 3. Technology Agnostic Framework

The same workflow works across:
- **Python + FastAPI** for APIs
- **TypeScript + Next.js** for frontend
- **Go + Gin** for microservices
- **Any other supported tech stack**

### 4. AI-Enhanced Development

Claude Code integration provides:
- **Context-aware code generation** from SSOT
- **Test generation** mapped to acceptance criteria
- **Contract validation** for correctness
- **Performance optimization** guidance

---

**🌾 These examples demonstrate the power of SSOT-driven development with AI assistance. Every line of code is traceable to requirements, validated against contracts, and optimized for quality.**