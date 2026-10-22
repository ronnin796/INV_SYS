# 📦 Smart Inventory Management & Demand Forecasting System (INV_SYS)

A full-featured inventory management system built with **Django**, **Django REST Framework**, and **Celery**, featuring automated time-series demand forecasting using **Auto-ARIMA (`pmdarima`)**.

---

## 🚀 Key Features

- **📦 Real-Time Inventory & Stock Tracking:** Monitor stock levels, reorder points, and low-stock warnings across products.
- **🏢 Multi-Warehouse Management:** Track and transfer inventory across multiple warehouse locations.
- **📈 AI/ML Demand Forecasting:** Forecast future sales and product demand using statistical time-series models with Auto-ARIMA.
- **💰 Sales & Purchase Workflows:** Manage customer sales, billing, and supplier purchase orders.
- **👥 Supplier & Customer Management:** Maintain centralized records, transaction histories, and supplier information.
- **📊 Analytics Dashboard:** View key performance indicators, sales charts, inventory valuation, and demand forecasts.
- **⚡ Asynchronous Task Processing:** Run scheduled forecasting jobs and background tasks using Celery and Redis.
- **🔐 Secure Authentication:** Support user authentication, role-based permissions, session authentication, and JSON Web Tokens (SimpleJWT).

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Backend | Python 3.10+, Django 5.x, Django REST Framework |
| Forecasting | `pmdarima`, Auto-ARIMA |
| Additional ML/NLP Tools | `nltk`, `kagglehub` |
| Task Queue & Scheduling | Celery, Redis, Celery Beat |
| Database | PostgreSQL (`psycopg2-binary`) / SQLite |
| Authentication | Django Authentication, SimpleJWT |
| Frontend | Django Templates, Crispy Forms, Bootstrap 4 |
| Static Files | Whitenoise |

---

## 📂 Project Architecture

```text
INV_SYS/
├── requirements.txt
├── LICENSE
└── inv/
    ├── manage.py
    ├── db.sqlite3
    ├── inv/
    │   └── Project settings and ASGI/WSGI configuration
    └── api/
        ├── inventory/      # Stock tracking and alerts
        ├── forecast/       # ARIMA-based demand forecasting
        ├── product/        # Product catalogs and SKUs
        ├── category/       # Product categories
        ├── subcategory/    # Product subcategories
        ├── sales/          # Sales orders and invoices
        ├── purchase/       # Supplier purchase orders
        ├── customer/       # Customer management
        ├── suppliers/      # Supplier management
        ├── warehouse/      # Warehouse locations and transfers
        ├── dashboard/      # Analytics and reporting
        └── user/           # Authentication and permissions
```

---

## 👥 Project Team & Contributors

This project was developed collaboratively by:

- **Nischal Chaudhary** — [@ronnin796](https://github.com/ronnin796)
- **Roja Shrestha** — [@rojashrestha](https://github.com/rojashrestha)
- **Saloni Rauniyar** — [@salonirau](https://github.com/salonirau)

---

## 🎓 Academic Context & Overview

This project was developed as our **5th Semester Engineering / Course Project**. The primary goal was to bridge the gap between traditional enterprise inventory management and modern data-driven forecasting by integrating **Full-Stack Web Development (Django/PostgreSQL)** with **Statistical Machine Learning (Time-Series Auto-ARIMA)** and **Asynchronous Task Scheduling (Celery/Redis)**.

- **Course/Semester:** 5th Semester Project
- **Domain:** Enterprise Systems, Supply Chain Management, and Predictive Analytics

---

## ⚙️ Installation & Local Setup

### 1. Prerequisites

Make sure you have the following installed:

- Python 3.10 or higher
- Git
- Redis server (required for Celery background tasks)

### 2. Clone the Repository

```bash
git clone https://github.com/ronnin796/INV_SYS.git
cd INV_SYS
```

### 3. Create and Activate a Virtual Environment

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
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the appropriate project configuration directory (`inv/`, alongside `manage.py`, if that is where your Django settings load it).

Example configuration:

```env
DEBUG=True
SECRET_KEY=your-django-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
```

**Important:** Update the environment variables according to your Django settings. Do not use the example secret key in production.

### 6. Run Database Migrations

Navigate to the directory containing `manage.py`:

```bash
cd inv
python manage.py migrate
```

If your project contains model changes that have not yet been migrated, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser

Create an administrator account to access the Django admin portal:

```bash
python manage.py createsuperuser
```

---

## 🏃 Running the Application

Run each service in a separate terminal. Activate the virtual environment in each terminal before starting the service.

### 1. Start the Django Development Server

From the directory containing `manage.py`:

```bash
python manage.py runserver
```

Access the application at:

- **Application:** http://127.0.0.1:8000/
- **Django Admin:** http://127.0.0.1:8000/admin/

### 2. Start the Celery Worker

In a separate terminal:

```bash
celery -A inv worker --loglevel=info
```

### 3. Start Celery Beat

In another separate terminal:

```bash
celery -A inv beat --loglevel=info
```

**Note:** Make sure Redis is running before starting Celery. The commands assume `inv` is the correct Django project package and that the Celery application is configured accordingly.

---

## 📈 Demand Forecasting Module

The forecasting module uses **Auto-ARIMA (`pmdarima`)** to model historical sales data and forecast future product demand.

### Key Capabilities

- Aggregates historical sales transactions by product SKU.
- Identifies trends and potential seasonal patterns in product demand.
- Generates forecasts to support inventory planning.
- Helps inform reorder decisions and reduce the risk of stockouts or overstocking.

Forecast quality depends on the availability, quality, and amount of historical sales data. Forecasts should be evaluated against actual sales before being used for operational decisions.

---

## 📄 License

This project is licensed under the **MIT License**. See the [`LICENSE`](LICENSE) file for details.

