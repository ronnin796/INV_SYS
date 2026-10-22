# 📦 Smart Inventory Management & Demand Forecasting System (INV_SYS)

A full-featured, enterprise-grade **Inventory Management System** built with **Django**, **Django REST Framework**, and **Celery**, powered by automated **Time-Series Demand Forecasting** (`pmdarima` / ARIMA).

---

## 🚀 Key Features

* **📦 Real-time Inventory & Stock Tracking**: Monitor stock levels, reorder points, and automated low-stock warnings across products.
* **🏢 Multi-Warehouse Management**: Track and transfer inventory across different warehouse locations.
* **📈 AI/ML Demand Forecasting**: Periodic sales and stock demand forecasting using statistical time-series models (**Auto-ARIMA** via `pmdarima`).
* **💰 Sales & Purchase Workflows**: Complete order lifecycle management for customer sales, billing, and supplier purchase orders.
* **👥 Supplier & Customer Management**: Centralized directories with transaction history and supplier reliability metrics.
* **📊 Analytics Dashboard**: Interactive KPIs, sales charts, inventory valuation, and forecast predictions.
* **⚡ Asynchronous Task Processing**: Scheduled forecasting jobs and background processing powered by **Celery** and **Redis** (`celerybeat`).
* **🔐 Secure API & Auth**: Role-based access control, session authentication, and JSON Web Tokens (**SimpleJWT**).

---

## 🛠️ Tech Stack

* **Backend Framework**: Python 3.10+, Django 5.x, Django REST Framework
* **Machine Learning / Forecasting**: `pmdarima`, `nltk`, `kagglehub`
* **Task Queue & Scheduler**: Celery, Redis, Celery Beat
* **Database**: PostgreSQL (`psycopg2-binary`) / SQLite
* **Authentication**: Django Auth, Django-REST-Framework-SimpleJWT
* **Frontend / UI Components**: Django Templates, Crispy Forms, Bootstrap 4, Whitenoise

---

## 📂 Project Architecture

```text
INV_SYS/
├── requirements.txt            # Project dependencies
├── LICENSE                     # License file
└── inv/                        # Django Project Root
    ├── manage.py               # Django CLI management script
    ├── db.sqlite3              # Local development database
    ├── inv/                    # Project settings & ASGI/WSGI configuration
    └── api/                    # Core Business Logic & Modules
        ├── inventory/          # Stock level tracking & alerts
        ├── forecast/           # ARIMA time-series demand forecasting
        ├── product/            # Product catalogs & SKUs
        ├── category/           # Product categories
        ├── subcategory/        # Product subcategories
        ├── sales/              # Customer sales orders & invoices
        ├── purchase/           # Supplier purchase orders
        ├── customer/           # Customer management
        ├── suppliers/          # Vendor/Supplier management
        ├── warehouse/          # Warehouse locations & transfers
        ├── dashboard/          # Analytics & reporting views
        └── user/               # User authentication & permissions

## ⚙️ Installation & Local Setup

### 1. Prerequisites

- Python 3.10 or higher
- Redis server (for Celery background tasks)

### 2. Clone the Repository

```bash
git clone https://github.com/ronnin796/INV_SYS.git

cd INV_SYS
```

### 3. Create and Activate Virtual Environment

**Windows (PowerShell)**

```powershell
python -m venv .venv

.\.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

### 5. Environment Configuration

Create a `.env` file in the `inv/` directory (or set environment variables):

```env
DEBUG=True

SECRET_KEY=your-django-secret-key-here

DATABASE_URL=sqlite:///db.sqlite3

REDIS_URL=redis://localhost:6379/0
```

### 6. Run Database Migrations

```bash
cd inv

python manage.py makemigrations

python manage.py migrate
```

### 7. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

---

## 🏃 Running the Application

### 1. Start the Django Development Server

From the `inv/` directory, run:

```bash
python manage.py runserver
```

Visit the application at:

- **Application:** http://127.0.0.1:8000/
- **Admin Portal:** http://127.0.0.1:8000/admin/

### 2. Start Celery Worker

Open a separate terminal, activate the virtual environment, and run:

```bash
cd inv

celery -A inv worker --loglevel=info
```

### 3. Start Celery Beat Scheduler

Open another separate terminal, activate the virtual environment, and run:

```bash
cd inv

celery -A inv beat --loglevel=info
```

---

## 📈 Demand Forecasting Module

The forecasting pipeline utilizes Auto-ARIMA (`pmdarima`) to fit historical sales data and forecast future product demand.

Key features include:

- Aggregates historical sales transactions per product SKU.
- Identifies seasonal trends and demand fluctuations.
- Automatically computes reorder levels to help prevent stockouts and overstocking.

---

## 📄 License

This project is licensed under the terms of the MIT License. See the `LICENSE` file for details.
