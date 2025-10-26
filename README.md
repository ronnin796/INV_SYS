# 🏭 Multi-Warehouse Inventory Forecast & Alert System

A smart and scalable **Inventory Management System** built with **Django**, designed to manage multiple warehouses, predict stock shortages, and automate restocking alerts — all powered by data forecasting and background automation.

This system integrates **(ARIMA)** for demand forecasting, **Celery + Redis** for asynchronous alerting, and a clean **TailwindCSS + Alpine.js** dashboard .
---

## 🚀 Key Features

### 🏢 Multi-Warehouse Management
- Manage multiple **warehouses** independently  
- Track **stock levels** of each product across warehouses  
- Centralized dashboard for viewing all warehouse inventories  
- Real-time synchronization between warehouses

### 🧾 Product, Category & Supplier Management
- Manage **products**, **categories**, and **suppliers**  
- Each product linked to a specific warehouse  
- Update quantities on restock or sale  
- Automatic calculation of total available stock  

### 📉 Intelligent Forecasting
- Predicts future demand using  **ARIMA**  
- Helps identify upcoming **stock shortages** per warehouse  
- Trend visualization with **Chart.js** graphs  
- Separate `forecast` module for clean, maintainable logic  

### 🔔 Automated Stock Alerts
- **Celery + Redis** handle background alert tasks  
- Low-stock alerts automatically sent via email  
- Configurable thresholds for different product types  
- Ensures timely restocking without manual checks  
 

---

## 🧰 Tech Stack

| Layer | Technologies |
|-------|---------------|
| **Backend** | Django, Django ORM |
| **Frontend** | Tailwind CSS, Alpine.js, Chart.js |
| **Machine Learning** | Statsmodels (ARIMA) |
| **Task Queue** | Celery + Redis |
| **Database** | SQLite / PostgreSQL |
| **Version Control** | Git + GitHub |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ronnin796/INV_SYS.git
cd inv
```

### 2️⃣ Create and Activate virtual envoronment

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt

```
### 4️⃣ Apply Migrations
```
python manage.py makemigrations
python manage.py migrate

```
### 5️⃣ Start Redis & Celery (optional)

### 6️⃣ Run the Django Server
```
python manage.py runserver

```
🪄 License

This project is licensed under the MIT License — you are free to use, modify, and distribute.


