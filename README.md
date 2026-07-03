# Garment Store Billing & Inventory Management System

A simple, user-friendly, and feature-rich web application designed for retail garment stores to manage inventory, handle sales transactions, generate QR codes, print invoices, and analyze sales/profit reports.

This project is built using Python, Django, SQLite, and vanilla web frontend languages (HTML, CSS, JavaScript) without any heavy external frameworks, strictly following clean and beginner-friendly programming practices.

---

## 🌟 Key Features & Phase Breakdown

### Phase 1: Custom Session Authentication
- **Shop Profiles**: Register store details (Name, Owner, Contact Number, Email, Address, and Logo image).
- **Session-based Security**: Protects dashboards, inventory management, and billing endpoints via session-stored credentials.
- **Shop Security Controls**: Includes "Forgot Password" profile verification and "Change Password" panels.

### Phase 2: Categories, Subcategories & Products
- **Categories & Subcategories**: Custom CRUD interfaces to classify clothing lines (e.g., Category: Menswear, Subcategory: Shirts).
- **Product Management**: Add, view, edit, search, and delete products. Includes product images and rack location tracking.
- **Automatic Product ID**: Formulates unique serial IDs sequentially like `SAR-000001`.
- **Automatic QR Codes**: Dynamically creates unique QR codes embedding product details upon product registration and saves them inside `media/qrcodes/`.

### Phase 3: Sales Billing & Invoicing
- **Sales Billing Terminal**: Live console to search products by Product ID and add them to a session-based active cart.
- **Stock Guard**: Validates cart additions and checkout against active inventory levels, preventing overselling.
- **Custom checkout**: Collects customer details and tracks payment modes (Cash, UPI, Card).
- **Invoice Generation**: Auto-creates sequential invoices like `INV-000001` containing breakdown details.
- **PDF & Receipt Printing**: Dedicated print-friendly template styled for receipt prints, directly initiating the browser print workflow (`window.print()`).
- **Turnover & Profit Margin**: Subtracts product purchase prices from selling prices to aggregate invoice profits.

### Phase 4: Reports & Analytics Dashboard
- **Key Performance Cards**: Real-time counter of total registered products, current stock volume in units, today's gross sales, and today's net profit.
- **Alert Tables**: Lists best-selling clothing items and triggers low stock warnings (qty &le; 5).
- **Daily & Monthly Registers**: Filterable ledgers displaying turnover, profit calculations, and list of invoices for selected days/months.
- **Weekly Summaries**: Compiles and displays progress bars comparing sales vs profit margins over the last 4 weeks.
- **Profit Range Analysis**: Analyzes Turnover, Cost of Goods Sold (COGS), and net store profits over custom start/end date ranges.

---

## 📁 Project Architecture & Directory Map

```text
InventioryA/
│
├── GarmentInventory/        # Main project configuration
│   ├── settings.py          # App registry, DB configs, static/media paths
│   ├── urls.py              # Main URL routing table (centralized route registry)
│   └── wsgi.py / asgi.py
│
├── inventory/               # Inventory & Auth App
│   ├── models.py            # Shop, Category, Subcategory, Product models
│   ├── views.py             # Auth & Inventory Function-Based Views (FBVs)
│   └── admin.py
│
├── sales/                   # Sales & Billing App
│   ├── models.py            # Invoice, InvoiceItem models
│   └── views.py             # Billing cart & Checkout FBVs
│
├── reports/                 # Reports Analytics App
│   └── views.py             # Sales logs & analytics calculations FBV
│
├── templates/               # HTML templates folder (Self-contained, no inheritance)
│   ├── login.html / signup.html / forgot_password.html / change_password.html
│   ├── dashboard.html / categories.html / subcategories.html / products.html
│   ├── billing.html / invoice_detail.html / invoice_print.html / sales_history.html
│   └── reports_dashboard.html
│
├── static/                  # Static assets
│   └── css/                 # Custom Vanilla stylesheets (One CSS per template)
│       └── *.css
│
├── media/                   # Uploaded media assets
│   ├── logos/               # Store logos
│   ├── products/            # Product image uploads
│   └── qrcodes/             # Auto-generated product QR codes
│
├── db.sqlite3               # SQLite Database
├── requirements.txt         # Project package dependencies list
└── README.md                # Documentation guide
```

---

## ⚙️ Coding Style Guidelines (Developer Notes)

- **Pure FBVs**: Views are written using simple Python function definitions (`def`), avoiding Class-Based Views.
- **No Django Forms**: HTML forms are written manually inside templates, and request parameters are captured using `request.POST.get()` or `request.GET.get()`.
- **Vanilla Frontend**: Custom styled pages utilizing pure CSS grids/flexboxes, backdrop blur filters, and transitions (no Tailwind, Bootstrap, or jQuery).
- **Self-contained HTML**: Each template page contains its complete layout structure (no `{% extends %}` or `{% include %}` filters used), ensuring simple file readability.

---

## 🚀 How to Run the Project Locally

### Step 1: Install Dependencies
Create a virtual environment (optional but recommended) and install dependencies listed in `requirements.txt`:
```bash
# Activate virtual environment (Windows syntax)
.\env\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Database Preparation
Run Django migration commands to initialize database tables for inventory, sales, and shops:
```bash
# Generate database schema scripts
python manage.py makemigrations

# Apply migrations onto the db.sqlite3 database
python manage.py migrate
```


Launch the development web server:
```bash
python manage.py runserver
```
Now, open your web browser and navigate to `http://127.0.0.1:8000/`.

*Note: Since the system uses custom session-based security, first sign up a Shop account (`/signup/`), then log in to access the store administration dashboard.*
##Live Link:sujalbadal.pythonanywhere.com


