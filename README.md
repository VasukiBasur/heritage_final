# Heritage Textile & Handloom Supply Chain Tracker

## Overview
The **Heritage Textile & Handloom Supply Chain Tracker** is a full-stack, data-driven web application designed to digitize and manage traditional artisanal workflows. It tracks master weavers, traditional designs, inventory of raw materials, and active production logs across 10 enterprise supply chain modules. 

Powered by a robust MySQL backend utilizing advanced database features (Triggers, Stored Procedures, Views, Foreign Key Cascades) and a Python/Flask middleware layer, the platform securely calculates artisanal payouts, audits supply chains, and provides dynamic data analytics via a premium, responsive frontend.

---

## Pre-Configured Role Credentials

All accounts are pre-seeded and ready to use:

| Role | Email | Password | Landing Page |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@example.com` | `1234` | `/admin/dashboard` |
| **Weaver / Artisan** | `artisan@example.com` | `1234` | `/weaver_dashboard` |
| **Supplier** | `supplier@example.com` | `1234` | `/supplier/dashboard` |
| **Customer / Buyer** | `customer@example.com` | `1234` | `/shop/home` |
| **Delivery Partner** | `delivery@example.com` | `1234` | `/delivery/dashboard` |

---

## How to Run the Server Locally

1. **Activate Virtual Environment**:
   ```powershell
   .\.venv\Scripts\activate
   ```

2. **(Optional) Re-seed Database**:
   Ensure MySQL service is running, then run:
   ```powershell
   python setup_master_db.py
   ```

3. **Start the Application**:
   ```powershell
   python app.py
   ```

4. **Access in Browser**:
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.


   # 🧵 Heritage Handloom Management System

🔗 **Live Demo:** https://heritage-final-1.onrender.com
