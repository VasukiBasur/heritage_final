# Public Deployment Guide: Heritage Textile & Handloom ERP

This guide provides step-by-step instructions to deploy the **Heritage Textile & Handloom Supply Chain Tracker** as a live public website with a managed cloud MySQL database.

---

## Architecture Overview

```
[ Public Users / Mobile Phones ]
               │
               ▼ (HTTPS)
   [ Render / Railway Web App ]
       │ Python 3.14 + Flask + Gunicorn WSGI
       │ Reverse ProxyFix (SSL Termination)
       │
       ▼ (Encrypted MySQL 8.0 Protocol)
 [ Managed Cloud MySQL Database ]
   (TiDB Cloud / Aiven / Railway)
   18 Tables, 2 Triggers, Stored Procedure, View
```

---

## Option 1: Render (Web Service) + TiDB Cloud (Recommended)

This is the cleanest, 100% free hosting combination.

### Part A: Set up Free Hosted MySQL on TiDB Cloud
1. Go to [tidbcloud.com](https://tidbcloud.com) and sign up for a free account.
2. Click **Create Cluster** and select **Serverless** (Free 5GB tier).
3. Set your cluster name to `heritage-handloom` and click **Create**.
4. In the **Connect** dialog:
   - Generate your database password and copy it.
   - Note the **Host**, **Port** (`4000`), **User**, and **Database name** (`test` or create `heritage_handloom`).
5. Enable SSL: TiDB Serverless requires SSL by default.

### Part B: Initialize & Seed Remote Database
Before deploying the web app, initialize all tables and seed data into your cloud database from your local terminal:

1. In your local `.env` file, temporarily set the cloud database credentials:
   ```env
   DB_HOST=gateway01.ap-southeast-1.prod.aws.tidbcloud.com
   DB_PORT=4000
   DB_USER=your_username.root
   DB_PASSWORD=your_password
   DB_NAME=heritage_handloom
   DB_SSL=true
   ```
2. Run the master setup script:
   ```powershell
   python setup_master_db.py
   ```
   *This automatically creates all 18 tables, triggers, stored procedures, provenance views, and populates the 5 role accounts and sample data.*

### Part C: Deploy Flask App to Render
1. Push your project code to a GitHub repository:
   ```bash
   git add .
   git commit -m "Configure production deployment settings"
   git push origin main
   ```
2. Go to [render.com](https://render.com) and click **New +** -> **Web Service**.
3. Select your GitHub repository.
4. Configure the Web Service:
   - **Name**: `heritage-handloom` (or your chosen name)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --workers 2 --threads 4 --timeout 120`
5. In **Environment Variables**, add:
   | Key | Value |
   | :--- | :--- |
   | `DB_HOST` | *(Your cloud DB host)* |
   | `DB_PORT` | `4000` *(or your cloud port)* |
   | `DB_USER` | *(Your cloud DB user)* |
   | `DB_PASSWORD` | *(Your cloud DB password)* |
   | `DB_NAME` | `heritage_handloom` |
   | `DB_SSL` | `true` |
   | `SECRET_KEY` | *(A random 32+ character string, e.g. `heritage_handloom_prod_key_2026_super_secure!`)* |
   | `FLASK_ENV` | `production` |
6. Click **Deploy Web Service**.
7. In ~2 minutes, your website will be live at `https://heritage-handloom.onrender.com`!

---

## Option 2: 1-Click Unified Deployment on Railway.app

Railway can host both the Python app and the MySQL database in one place.

1. Go to [railway.app](https://railway.app) and click **Start a New Project**.
2. Select **Provision MySQL**.
   - Railway will provision a private/public MySQL instance.
   - In the MySQL service settings, click **Variables** and copy `MYSQLHOST`, `MYSQLPORT`, `MYSQLUSER`, `MYSQLPASSWORD`, `MYSQLDATABASE`.
3. In the same project, click **New** -> **GitHub Repo** -> select this repository.
4. Railway will automatically detect the [Procfile](file:///c:/heritage_final/Procfile) and build using `gunicorn`.
5. Under your Web Service **Variables**, reference the MySQL variables:
   - `DB_HOST` = `${{MySQL.MYSQLHOST}}`
   - `DB_PORT` = `${{MySQL.MYSQLPORT}}`
   - `DB_USER` = `${{MySQL.MYSQLUSER}}`
   - `DB_PASSWORD` = `${{MySQL.MYSQLPASSWORD}}`
   - `DB_NAME` = `${{MySQL.MYSQLDATABASE}}`
   - `SECRET_KEY` = `heritage_handloom_super_secret_key_32bytes_sha256!`
6. In **Settings**, click **Generate Domain** to get a public URL (e.g. `https://heritage-handloom.up.railway.app`).
7. Run `python setup_master_db.py` once pointing to the Railway public database to seed it.

---

## Option 3: PythonAnywhere (All-In-One Dashboard)

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com).
2. Go to the **Databases** tab and click **Initialize MySQL**. Note your database hostname and password.
3. Open a **Bash Console** and clone your repository:
   ```bash
   git clone <your-repo-url>
   cd heritage_final
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   pip install -r requirements.txt
   ```
4. Update your `.env` with the PythonAnywhere database credentials and run:
   ```bash
   python setup_master_db.py
   ```
5. Go to the **Web** tab:
   - Click **Add a new web app** -> **Manual configuration** -> **Python 3.10**.
   - Set **Source code** to `/home/yourusername/heritage_final`.
   - Set **Virtualenv** to `/home/yourusername/.virtualenvs/myenv`.
   - Edit the **WSGI configuration file** to:
     ```python
     import sys
     import os
     from dotenv import load_dotenv

     project_home = '/home/yourusername/heritage_final'
     if project_home not in sys.path:
         sys.path.insert(0, project_home)

     load_dotenv(os.path.join(project_home, '.env'))

     from app import app as application
     ```
6. Click **Reload yourusername.pythonanywhere.com** and your app is live!

---

## Pre-Seeded Production User Accounts

Once deployed, you and your users can log in directly using the 5 pre-configured accounts:

| Role | Email | Password | Dashboard URL |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@example.com` | `1234` | `/admin/dashboard` |
| **Weaver / Artisan** | `artisan@example.com` | `1234` | `/weaver_dashboard` |
| **Supplier** | `supplier@example.com` | `1234` | `/supplier/dashboard` |
| **Customer / Buyer** | `customer@example.com` | `1234` | `/shop/home` |
| **Delivery Partner** | `delivery@example.com` | `1234` | `/delivery/dashboard` |

---

## Verification & Health Check

After deployment, test the live public URL:
1. Open `https://<your-public-domain>/login` in your browser.
2. Log in with `admin@example.com` / `1234`.
3. Verify that the Admin Dashboard loads with live charts, statistics, and tables.
4. Try scanning any on-screen QR code from a mobile phone camera: it will open the live public tracking page directly!
