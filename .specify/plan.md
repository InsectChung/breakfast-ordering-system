#### 步驟 10.2：完整技術計畫範例 - plan.md

```markdown
# 技術計畫：早餐店網路訂餐管理系統

## 文件資訊
- **版本**: 1.0
- **創建日期**: 2025-12-14
- **最後更新**: 2025-12-14
- **狀態**: 審核中
- **依據規格**: spec.md v1.0
- **依據憲法**: constitution.md v1.0

---

## 目錄
1. [整體架構](#architecture)
2. [資料庫設計](#database)
3. [API 端點定義](#api-endpoints)
4. [認證與授權](#authentication)
5. [支付整合](#payment)
6. [前端架構](#frontend)
7. [後端架構](#backend)
8. [測試策略](#testing)
9. [部署架構](#deployment)
10. [依賴清單](#dependencies)

---

<a name="architecture"></a>
## 1. 整體架構

### 1.1 系統架構圖

```
┌─────────────────────────────────────────────────┐
│   前端層 (Next.js)                              │
│   ┌──────────────┐  ┌──────────────┐            │
│   │ 客戶端 Pages │  │ 管理員 Pages │            │
│   └──────────────┘  └──────────────┘            │
│          ↓                   ↓                  │
│   ┌─────────────────────────────┐               │
│   │ Redux Store (狀態管理)      │               │
│   └─────────────────────────────┘               │
└─────────────────────────────────────────────────┘
                  ↓ HTTP/REST
┌─────────────────────────────────────────────────┐
│   API 閘道層 (Flask)                            │
│   ┌──────────────┐  ┌──────────────┐            │
│   │ JWT 認證中介 │  │ CORS 處理    │            │
│   └──────────────┘  └──────────────┘            │
└─────────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│   業務邏輯層 (Flask Services)                   │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│   │訂單服務  │ │菜單服務  │ │支付服務  │        │
│   └──────────┘ └──────────┘ └──────────┘        │
│   ┌──────────┐ ┌──────────┐                    │
│   │認證服務  │ │通知服務  │                    │
│   └──────────┘ └──────────┘                    │
└─────────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│   資料存取層 (SQLAlchemy ORM)                   │
└─────────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│   資料庫層 (SQLite)                             │
│   ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐          │
│   │User  │ │Menu  │ │Order │ │Order │          │
│   │      │ │Item  │ │      │ │Item  │          │
│   └──────┘ └──────┘ └──────┘ └──────┘          │
└─────────────────────────────────────────────────┘
```

### 1.2 技術棧總覽

| 層級 | 技術 | 版本 | 理由 |
|------|------|------|------|
| 前端 | Next.js | 14+ | 支援 SSR/SSG，SEO 友善，移動優先 |
| 狀態管理 | Redux Toolkit | 最新 | 可預測的狀態管理，DevTools 支援 |
| HTTP 客戶端 | Axios | 最新 | 支援攔截器，易於設定認證 Header |
| UI 組件 | Tailwind CSS | 3.x | 快速開發響應式 UI |
| 後端 | Flask | 3.0+ | 輕量級，靈活，適合 MVP |
| API 框架 | Flask-RESTful | 最新 | 快速建立 RESTful API |
| ORM | Flask-SQLAlchemy | 最新 | 與 Flask 深度整合 |
| 資料庫 (Dev) | SQLite | 3.x | 零配置，快速開發 |
| 資料庫 (Prod) | PostgreSQL | 15+ | 生產環境穩定、效能佳 |
| 認證 | JWT | - | 無狀態、適合 REST API |
| 測試 | pytest, behave | 最新 | TDD/BDD 支援 |

---

<a name="database"></a>
## 2. 資料庫設計

### 2.1 概念性 ERD (實體關係圖)

```
┌─────────────┐       ┌──────────────┐       ┌──────────────┐
│    User     │       │   MenuItem   │       │    Order     │
├─────────────┤       ├──────────────┤       ├──────────────┤
│ user_id (PK)│       │ item_id (PK) │       │ order_id (PK)│
│ email       │       │ name         │       │ user_id (FK) │
│ password    │       │ description  │       │ order_number │
│ name        │       │ price        │       │ total_amount │
│ phone       │       │ image_url    │       │ status       │
│ role        │       │ stock_level  │       │ payment_     │
│ address     │       │ category     │       │   method     │
│ created_at  │       │ is_available │       │ delivery_    │
└─────────────┘       │ created_at   │       │   address    │
                      └──────────────┘       │ estimated_   │
                                             │   delivery   │
                                             │ created_at   │
                                             │ updated_at   │
                                             └──────────────┘
                                                    │
                                                    │ 1:N
                                                    ↓
                                             ┌──────────────┐
                                             │  OrderItem   │
                                             ├──────────────┤
                                             │ item_id (PK) │
                                             │ order_id(FK) │
                                             │ menu_item_id │
                                             │   (FK)       │
                                             │ quantity     │
                                             │ unit_price   │
                                             │ subtotal     │
                                             │ custom_notes │
                                             └──────────────┘
```

### 2.2 詳細資料表定義

#### Table: `users`
**說明**: 儲存顧客和管理員帳戶資訊

| 欄位名稱 | 資料類型 | 約束 | 說明 |
|---------|---------|------|------|
| `user_id` | UUID | PK, NOT NULL | 主鍵 |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | 登入帳號 |
| `password_hash` | VARCHAR(255) | NOT NULL | bcrypt 雜湊密碼 (cost=12) |
| `name` | VARCHAR(100) | NOT NULL | 使用者姓名 |
| `phone` | VARCHAR(20) | NOT NULL | 聯絡電話 |
| `role` | ENUM | NOT NULL | `customer` 或 `admin` |
| `address` | TEXT | NULL | 預設配送地址 |
| `created_at` | TIMESTAMP | DEFAULT NOW() | 註冊時間 |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | 最後更新時間 |

**索引**:
- `idx_users_email` ON `email` (登入查詢優化)

**安全性**:
- 密碼必須使用 bcrypt (cost ≥ 12)
- Email 必須經過驗證（發送驗證郵件）

---

#### Table: `menu_items`
**說明**: 儲存餐點菜單資訊

| 欄位名稱 | 資料類型 | 約束 | 說明 |
|---------|---------|------|------|
| `item_id` | UUID | PK, NOT NULL | 主鍵 |
| `name` | VARCHAR(100) | NOT NULL | 餐點名稱 |
| `description` | TEXT | NULL | 餐點描述 |
| `price` | DECIMAL(10, 2) | NOT NULL | 價格（單位：元） |
| `image_url` | VARCHAR(500) | NOT NULL | 圖片 URL（高品質） |
| `stock_level` | INTEGER | NOT NULL, DEFAULT 0 | 當前庫存數量 |
| `category` | VARCHAR(50) | NOT NULL | 類別（主食/飲料/配菜） |
| `is_available` | BOOLEAN | DEFAULT TRUE | 是否供應中 |
| `created_at` | TIMESTAMP | DEFAULT NOW() | 建立時間 |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | 最後更新時間 |

**索引**:
- `idx_menu_category` ON `category` (分類查詢優化)
- `idx_menu_available` ON `is_available` (可用性篩選)

**業務規則**:
- 圖片必須符合憲法要求（≥ 800x600, < 200KB）
- 當 `stock_level = 0` 時，前端應自動標示「已售完」

---

#### Table: `orders`
**說明**: 儲存訂單主表

| 欄位名稱 | 資料類型 | 約束 | 說明 |
|---------|---------|------|------|
| `order_id` | UUID | PK, NOT NULL | 主鍵 |
| `user_id` | UUID | FK, NOT NULL | 關聯到 `users.user_id` |
| `order_number` | VARCHAR(50) | UNIQUE, NOT NULL | 人類可讀訂單編號 (ORD-YYYYMMDD-XXX) |
| `total_amount` | DECIMAL(10, 2) | NOT NULL | 訂單總金額 |
| `status` | ENUM | NOT NULL | `pending`, `in_progress`, `ready_for_delivery`, `delivered`, `cancelled` |
| `payment_method` | VARCHAR(50) | NOT NULL | 支付方式 |
| `payment_status` | ENUM | NOT NULL | `pending`, `completed`, `failed`, `refunded` |
| `delivery_address` | TEXT | NOT NULL | 配送地址 |
| `estimated_delivery` | TIMESTAMP | NOT NULL | 預計送達時間 |
| `created_at` | TIMESTAMP | DEFAULT NOW() | 訂單建立時間 |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | 最後更新時間 |

**索引**:
- `idx_orders_user` ON `user_id` (用戶訂單查詢)
- `idx_orders_status` ON `status` (狀態篩選)
- `idx_orders_created` ON `created_at` (時間排序)

**狀態機**:
```
pending → in_progress → ready_for_delivery → delivered
   ↓
cancelled (僅在 pending 或 in_progress 時允許)
```

---

#### Table: `order_items`
**說明**: 儲存訂單明細（多對多關聯表）

| 欄位名稱 | 資料類型 | 約束 | 說明 |
|---------|---------|------|------|
| `item_id` | UUID | PK, NOT NULL | 主鍵 |
| `order_id` | UUID | FK, NOT NULL | 關聯到 `orders.order_id` |
| `menu_item_id` | UUID | FK, NOT NULL | 關聯到 `menu_items.item_id` |
| `quantity` | INTEGER | NOT NULL, CHECK > 0 | 購買數量 |
| `unit_price` | DECIMAL(10, 2) | NOT NULL | 購買時的單價（快照） |
| `subtotal` | DECIMAL(10, 2) | NOT NULL | 小計 (quantity * unit_price) |
| `custom_notes` | TEXT | NULL | 客製化備註 |

**索引**:
- `idx_order_items_order` ON `order_id` (訂單明細查詢)

**業務規則**:
- `unit_price` 必須快照當時的價格（防止事後菜單價格變動影響歷史訂單）
- `subtotal` 應由後端自動計算，不接受前端傳入

---

### 2.3 SQLAlchemy 模型定義範例

**app/models/user.py**

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.Enum('customer', 'admin', name='user_roles'), nullable=False, default='customer')
    address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關係
    orders = db.relationship('Order', backref='customer', lazy=True)
    
    def set_password(self, password):
        """使用 bcrypt (cost=12) 雜湊密碼"""
        self.password_hash = generate_password_hash(password, method='bcrypt')
    
    def check_password(self, password):
        """驗證密碼"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """序列化為 JSON（不包含密碼）"""
        return {
            'user_id': str(self.user_id),
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'role': self.role,
            'address': self.address,
            'created_at': self.created_at.isoformat()
        }
```

---

<a name="api-endpoints"></a>
## 3. API 端點定義

### 3.1 API 設計原則

- **REST 風格**: 使用標準 HTTP 方法（GET, POST, PUT, DELETE）
- **版本控制**: 所有 API 以 `/api/v1/` 為前綴
- **統一響應格式**: 所有響應使用標準 JSON 格式
- **錯誤處理**: 遵循憲法定義的錯誤格式
- **認證**: 使用 JWT Bearer Token（除公開端點外）

### 3.2 統一響應格式

**成功響應**:
```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功" (可選)
}
```

**錯誤響應**:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "人類可讀的錯誤訊息",
    "details": { ... },
    "timestamp": "2025-12-14T10:30:00Z"
  }
}
```

---

### 3.3 認證相關 API

#### `POST /api/v1/auth/register`
**說明**: 註冊新用戶

**認證**: 無需認證

**請求體**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "張三",
  "phone": "0912-345-678",
  "address": "台北市信義區信義路五段 1 號"
}
```

**成功響應** (201 Created):
```json
{
  "success": true,
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "張三",
    "role": "customer"
  },
  "message": "註冊成功，請檢查郵件進行驗證"
}
```

**錯誤響應** (400 Bad Request):
```json
{
  "success": false,
  "error": {
    "code": "EMAIL_ALREADY_EXISTS",
    "message": "此 Email 已被註冊",
    "timestamp": "2025-12-14T10:30:00Z"
  }
}
```

---

#### `POST /api/v1/auth/login`
**說明**: 用戶登入

**認證**: 無需認證

**請求體**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**成功響應** (200 OK):
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "name": "張三",
      "role": "customer"
    }
  }
}
```

**Token 有效期**:
- `access_token`: 1 小時
- `refresh_token`: 7 天

---

### 3.4 菜單相關 API

#### `GET /api/v1/menu`
**說明**: 獲取所有可用的菜單項目

**認證**: 無需認證（公開端點）

**查詢參數**:
- `category` (可選): 篩選類別（`main`, `drink`, `side`）
- `available` (可選): 僅顯示供應中的項目（`true`/`false`，默認 `true`）

**請求範例**:
```
GET /api/v1/menu?category=main&available=true
```

**成功響應** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "item_id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "經典蛋餅",
      "description": "現煎蛋餅，酥脆外皮",
      "price": 35.00,
      "image_url": "https://cdn.example.com/images/egg-pancake.webp",
      "stock_level": 50,
      "category": "main",
      "is_available": true
    },
    {
      "item_id": "123e4567-e89b-12d3-a456-426614174001",
      "name": "冰美式咖啡",
      "description": "精選阿拉比卡豆",
      "price": 45.00,
      "image_url": "https://cdn.example.com/images/iced-americano.webp",
      "stock_level": 30,
      "category": "drink",
      "is_available": true
    }
  ]
}
```

**效能要求**: P95 延遲 < 3000ms

---

### 3.5 訂單相關 API

#### `POST /api/v1/orders`
**說明**: 創建新訂單

**認證**: 需要 JWT Token（`customer` 或 `admin` 角色）

**Header**:
```
Authorization: Bearer <access_token>
```

**請求體**:
```json
{
  "items": [
    {
      "menu_item_id": "123e4567-e89b-12d3-a456-426614174000",
      "quantity": 2,
      "custom_notes": "不要蔥"
    },
    {
      "menu_item_id": "123e4567-e89b-12d3-a456-426614174001",
      "quantity": 1
    }
  ],
  "delivery_address": "台北市信義區信義路五段 1 號",
  "estimated_delivery": "2025-12-14T08:30:00Z",
  "payment_method": "credit_card"
}
```

**成功響應** (201 Created):
```json
{
  "success": true,
  "data": {
    "order_id": "789e4567-e89b-12d3-a456-426614174000",
    "order_number": "ORD-20251214-001",
    "total_amount": 125.00,
    "status": "pending",
    "payment_status": "pending",
    "delivery_address": "台北市信義區信義路五段 1 號",
    "estimated_delivery": "2025-12-14T08:30:00Z",
    "items": [
      {
        "item_id": "xxx",
        "name": "經典蛋餅",
        "quantity": 2,
        "unit_price": 35.00,
        "subtotal": 70.00
      },
      {
        "item_id": "yyy",
        "name": "冰美式咖啡",
        "quantity": 1,
        "unit_price": 45.00,
        "subtotal": 45.00
      }
    ],
    "created_at": "2025-12-14T07:45:00Z"
  },
  "message": "訂單創建成功，請完成支付"
}
```

**錯誤響應** (400 Bad Request):
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "經典蛋餅庫存不足，剩餘 1 份",
    "details": {
      "item_id": "123e4567-e89b-12d3-a456-426614174000",
      "requested": 2,
      "available": 1
    },
    "timestamp": "2025-12-14T07:45:30Z"
  }
}
```

**效能要求**: P95 延遲 < 1500ms（關鍵 API）

---

#### `GET /api/v1/orders/:order_id`
**說明**: 查詢訂單詳情

**認證**: 需要 JWT Token

**權限**: 
- `customer`: 僅能查詢自己的訂單
- `admin`: 可查詢所有訂單

**成功響應** (200 OK):
```json
{
  "success": true,
  "data": {
    "order_id": "789e4567-e89b-12d3-a456-426614174000",
    "order_number": "ORD-20251214-001",
    "customer": {
      "name": "張三",
      "phone": "0912-345-678"
    },
    "total_amount": 125.00,
    "status": "in_progress",
    "payment_status": "completed",
    "payment_method": "credit_card",
    "delivery_address": "台北市信義區信義路五段 1 號",
    "estimated_delivery": "2025-12-14T08:30:00Z",
    "items": [...],
    "created_at": "2025-12-14T07:45:00Z",
    "updated_at": "2025-12-14T07:50:00Z"
  }
}
```

**錯誤響應** (403 Forbidden):
```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "您沒有權限查看此訂單",
    "timestamp": "2025-12-14T08:00:00Z"
  }
}
```

---

#### `PUT /api/v1/orders/:order_id/status`
**說明**: 更新訂單狀態（僅管理員）

**認證**: 需要 JWT Token（僅 `admin` 角色）

**請求體**:
```json
{
  "status": "ready_for_delivery"
}
```

**成功響應** (200 OK):
```json
{
  "success": true,
  "data": {
    "order_id": "789e4567-e89b-12d3-a456-426614174000",
    "status": "ready_for_delivery",
    "updated_at": "2025-12-14T08:20:00Z"
  },
  "message": "訂單狀態已更新"
}
```

**效能要求**: P95 延遲 < 1500ms（關鍵 API）

---

### 3.6 管理員 API

#### `GET /api/v1/admin/orders`
**說明**: 獲取訂單列表（僅管理員）

**認證**: 需要 JWT Token（僅 `admin` 角色）

**查詢參數**:
- `status` (可選): 篩選狀態（`pending`, `in_progress`, 等）
- `page` (可選): 頁碼（默認 1）
- `per_page` (可選): 每頁數量（默認 20，最大 100）

**成功響應** (200 OK):
```json
{
  "success": true,
  "data": {
    "orders": [
      {
        "order_id": "...",
        "order_number": "ORD-20251214-001",
        "customer_name": "張三",
        "total_amount": 125.00,
        "status": "pending",
        "created_at": "2025-12-14T07:45:00Z"
      }
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 20,
      "total_items": 45,
      "total_pages": 3
    }
  }
}
```

---

<a name="authentication"></a>
## 4. 認證與授權策略

### 4.1 JWT Token 結構

**Access Token Payload**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "role": "customer",
  "exp": 1702548900,
  "iat": 1702545300
}
```

**Refresh Token Payload**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "refresh",
  "exp": 1703153100,
  "iat": 1702545300
}
```

### 4.2 認證流程

```
1. 用戶登入 → 後端驗證密碼 → 返回 access_token + refresh_token
2. 前端儲存 Token 到 localStorage 或 HttpOnly Cookie
3. 每次 API 請求攜帶: Authorization: Bearer <access_token>
4. 後端驗證 Token → 允許/拒絕請求
5. Access Token 過期 → 使用 Refresh Token 獲取新的 Access Token
```

### 4.3 權限控制

| 端點 | 允許角色 | 說明 |
|------|---------|------|
| `GET /api/v1/menu` | 公開 | 無需認證 |
| `POST /api/v1/orders` | `customer`, `admin` | 已認證用戶 |
| `GET /api/v1/orders/:id` | `customer`(自己), `admin` | 角色 + 所有權檢查 |
| `PUT /api/v1/orders/:id/status` | `admin` | 僅管理員 |
| `GET /api/v1/admin/*` | `admin` | 僅管理員 |

---

<a name="payment"></a>
## 5. 支付整合策略

### 5.1 支付流程

```
1. 顧客提交訂單 → 訂單狀態: pending, 支付狀態: pending
2. 前端導向支付閘道（或使用 SDK）
3. 支付閘道處理交易 → 回傳結果
4. 後端接收 Webhook 或輪詢結果 → 更新支付狀態
5. 支付成功 → 訂單狀態: in_progress, 支付狀態: completed
6. 支付失敗 → 訂單狀態: 保持 pending, 支付狀態: failed
```

### 5.2 Mock 支付閘道（開發環境）

**目的**: MVP 階段使用 Mock 服務模擬支付行為

**實作**:
```python
# app/services/payment_mock.py

class MockPaymentGateway:
    """模擬支付閘道，用於開發和測試"""
    
    @staticmethod
    def process_payment(order_id, amount, payment_method):
        """模擬支付處理
        
        Args:
            order_id: 訂單 ID
            amount: 金額（元）
            payment_method: 支付方式
            
        Returns:
            {
                'success': bool,
                'transaction_id': str,
                'message': str
            }
        """
        import random
        import time
        
        # 模擬網路延遲
        time.sleep(random.uniform(0.5, 1.5))
        
        # 90% 成功率
        if random.random() < 0.9:
            return {
                'success': True,
                'transaction_id': f'TXN-{order_id}-{int(time.time())}',
                'message': '支付成功'
            }
        else:
            return {
                'success': False,
                'transaction_id': None,
                'message': '支付失敗：餘額不足'
            }
```

### 5.3 生產環境整合（未來）

**建議的第三方支付服務**:
- **Stripe**: 國際市場，支援信用卡、Apple Pay
- **綠界科技 (ECPay)**: 台灣市場，支援超商付款、ATM
- **藍新金流 (NewebPay)**: 台灣市場，多元支付方式

**安全性要求**:
- 所有敏感資料傳輸必須加密（HTTPS/TLS 1.3）
- 不儲存完整信用卡號碼（遵循 PCI DSS）
- 使用 Tokenization 技術

---

<a name="frontend"></a>
## 6. 前端架構設計

### 6.1 目錄結構

```
breakfast-ordering-frontend/
├── app/
│   ├── (customer)/           # 客戶端路由群組
│   │   ├── menu/
│   │   │   └── page.tsx
│   │   ├── cart/
│   │   │   └── page.tsx
│   │   ├── checkout/
│   │   │   └── page.tsx
│   │   └── orders/
│   │       └── [id]/
│   │           └── page.tsx
│   ├── (admin)/              # 管理員路由群組
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   └── orders/
│   │       └── page.tsx
│   ├── api/                  # API Routes (可選)
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/                   # 通用 UI 組件
│   ├── customer/             # 客戶端組件
│   │   ├── MenuCard.tsx
│   │   ├── CartItem.tsx
│   │   └── OrderTracker.tsx
│   └── admin/                # 管理員組件
│       └── OrderListItem.tsx
├── lib/
│   ├── api/                  # API 客戶端
│   │   ├── axios-instance.ts
│   │   ├── menu.ts
│   │   ├── orders.ts
│   │   └── auth.ts
│   └── utils/                # 工具函數
├── store/                    # Redux Store
│   ├── slices/
│   │   ├── cartSlice.ts
│   │   ├── authSlice.ts
│   │   └── orderSlice.ts
│   └── store.ts
├── types/                    # TypeScript 類型定義
├── public/
└── package.json
```

### 6.2 狀態管理（Redux Toolkit）

**Cart Slice 範例**:
```typescript
// store/slices/cartSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CartItem {
  menu_item_id: string;
  name: string;
  quantity: number;
  unit_price: number;
  subtotal: number;
  image_url: string;
}

interface CartState {
  items: CartItem[];
  total_amount: number;
}

const initialState: CartState = {
  items: [],
  total_amount: 0
};

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    addItem: (state, action: PayloadAction<CartItem>) => {
      const existingItem = state.items.find(
        item => item.menu_item_id === action.payload.menu_item_id
      );
      
      if (existingItem) {
        existingItem.quantity += action.payload.quantity;
        existingItem.subtotal = existingItem.quantity * existingItem.unit_price;
      } else {
        state.items.push(action.payload);
      }
      
      state.total_amount = state.items.reduce((sum, item) => sum + item.subtotal, 0);
    },
    
    removeItem: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter(item => item.menu_item_id !== action.payload);
      state.total_amount = state.items.reduce((sum, item) => sum + item.subtotal, 0);
    },
    
    clearCart: (state) => {
      state.items = [];
      state.total_amount = 0;
    }
  }
});

export const { addItem, removeItem, clearCart } = cartSlice.actions;
export default cartSlice.reducer;
```

---

<a name="backend"></a>
## 7. 後端架構設計

### 7.1 目錄結構

```
breakfast-ordering-backend/
├── app/
│   ├── __init__.py           # Flask App 工廠
│   ├── models/               # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── menu_item.py
│   │   ├── order.py
│   │   └── order_item.py
│   ├── routes/               # API 路由
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── menu.py
│   │   ├── orders.py
│   │   └── admin.py
│   ├── services/             # 業務邏輯層
│   │   ├── __init__.py
│   │   ├── order_service.py
│   │   ├── menu_service.py
│   │   └── payment_mock.py
│   ├── middleware/           # 中介軟體
│   │   ├── __init__.py
│   │   ├── auth.py           # JWT 驗證
│   │   └── error_handler.py
│   └── utils/                # 工具函數
│       ├── __init__.py
│       └── validators.py
├── tests/                    # 測試
│   ├── unit/
│   ├── integration/
│   └── features/             # BDD 測試（Gherkin）
├── migrations/               # 資料庫遷移
├── config.py                 # 配置文件
├── run.py                    # 應用程式入口
├── requirements.txt
└── pytest.ini
```

### 7.2 Flask 應用程式工廠

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config

db = SQLAlchemy()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化擴展
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})  # 生產環境需限制
    
    # 註冊藍圖
    from app.routes import auth, menu, orders, admin
    app.register_blueprint(auth.bp, url_prefix='/api/v1/auth')
    app.register_blueprint(menu.bp, url_prefix='/api/v1/menu')
    app.register_blueprint(orders.bp, url_prefix='/api/v1/orders')
    app.register_blueprint(admin.bp, url_prefix='/api/v1/admin')
    
    # 註冊錯誤處理
    from app.middleware.error_handler import register_error_handlers
    register_error_handlers(app)
    
    return app
```

---

<a name="testing"></a>
## 8. 測試策略

### 8.1 測試金字塔

```
        ┌─────────────┐
        │  E2E 測試   │  ← 少量（關鍵流程）
        └─────────────┘
      ┌───────────────────┐
      │   整合測試        │  ← 中等數量（API 端點）
      └───────────────────┘
  ┌─────────────────────────┐
  │     單元測試            │  ← 大量（業務邏輯、模型）
  └─────────────────────────┘
```

### 8.2 測試類型與工具

| 測試類型 | 工具 | 涵蓋範圍 | 目標覆蓋率 |
|---------|------|---------|-----------|
| **單元測試** | pytest | 模型、服務、工具函數 | ≥ 90% |
| **整合測試** | pytest + Flask test client | API 端點、資料庫互動 | ≥ 80% |
| **BDD 測試** | behave (Gherkin) | 端到端用戶流程 | 所有關鍵場景 |
| **效能測試** | Locust / Apache Bench | 關鍵 API 延遲 | < 1500ms (P95) |
| **安全測試** | bandit, safety | 漏洞掃描 | 無高風險漏洞 |

### 8.3 BDD 測試範例

**tests/features/order_creation.feature**

```gherkin
Feature: 訂單創建
  
  Background:
    Given 系統中存在以下菜單項目：
      | item_id                              | name     | price | stock |
      | 123e4567-e89b-12d3-a456-426614174000 | 經典蛋餅 | 35    | 50    |
    And 我已登入為 "customer" 角色

  Scenario: 成功創建訂單
    When 我發送 POST 請求到 "/api/v1/orders" 包含：
      """
      {
        "items": [
          {
            "menu_item_id": "123e4567-e89b-12d3-a456-426614174000",
            "quantity": 2
          }
        ],
        "delivery_address": "台北市信義區信義路五段 1 號",
        "estimated_delivery": "2025-12-14T08:30:00Z",
        "payment_method": "credit_card"
      }
      """
    Then 響應狀態碼應為 201
    And 響應體應包含 "order_id"
    And 訂單狀態應為 "pending"
```

**tests/features/steps/order_steps.py**

```python
from behave import given, when, then
import json

@given('系統中存在以下菜單項目：')
def step_impl(context):
    # 在測試資料庫中創建菜單項目
    pass

@when('我發送 POST 請求到 "{endpoint}" 包含：')
def step_impl(context, endpoint):
    context.response = context.client.post(
        endpoint,
        data=context.text,
        content_type='application/json',
        headers={'Authorization': f'Bearer {context.access_token}'}
    )

@then('響應狀態碼應為 {status_code:d}')
def step_impl(context, status_code):
    assert context.response.status_code == status_code

@then('響應體應包含 "{field}"')
def step_impl(context, field):
    data = json.loads(context.response.data)
    assert field in data['data']
```

---

<a name="deployment"></a>
## 9. 部署架構

### 9.1 開發環境

```
本地開發:
- 前端: npm run dev (localhost:3000)
- 後端: flask run (localhost:5000)
- 資料庫: SQLite (本地文件)
```

### 9.2 生產環境（建議）

```
┌────────────────────────────────────────┐
│   Load Balancer / CDN (Cloudflare)    │
└────────────────────────────────────────┘
          ↓                     ↓
┌─────────────────┐   ┌─────────────────┐
│ Next.js (Vercel)│   │ Flask (AWS ECS) │
│ 前端靜態資源     │   │ 後端 API        │
└─────────────────┘   └─────────────────┘
                              ↓
                    ┌─────────────────┐
                    │ PostgreSQL (RDS)│
                    │ 生產資料庫      │
                    └─────────────────┘
```

**部署平台建議**:
- **前端**: Vercel（Next.js 原生支援）或 AWS Amplify
- **後端**: AWS ECS/Fargate, Google Cloud Run, 或 Heroku
- **資料庫**: AWS RDS (PostgreSQL), Google Cloud SQL
- **圖片儲存**: AWS S3 + CloudFront

---

<a name="dependencies"></a>
## 10. 依賴清單

### 10.1 後端依賴 (requirements.txt)

```txt
# Flask 核心
Flask==3.0.0
Flask-RESTful==0.3.10
Flask-SQLAlchemy==3.1.1
Flask-CORS==4.0.0
Flask-JWT-Extended==4.5.3

# 資料庫
SQLAlchemy==2.0.23
psycopg2-binary==2.9.9  # PostgreSQL 驅動
alembic==1.13.0         # 資料庫遷移

# 安全性
bcrypt==4.1.2
PyJWT==2.8.0

# 測試
pytest==7.4.3
pytest-cov==4.1.0
behave==1.2.6
factory-boy==3.3.0      # 測試資料生成

# 工具
python-dotenv==1.0.0
marshmallow==3.20.1     # 資料序列化
```
