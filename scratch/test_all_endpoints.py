import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import app
import jwt
from datetime import datetime, timedelta

def run_tests():
    print("=" * 60)
    print("HERITAGE HANDLOOM - END-TO-END VALIDATION SUITE")
    print("=" * 60)

    client = app.app.test_client()
    passed = 0
    failed = 0

    def test_endpoint(desc, method, url, role=None, user_id=1, username="TestUser", expected_status=200):
        nonlocal passed, failed
        headers = {}
        if role:
            payload = {
                'user_id': user_id,
                'role': role,
                'username': username,
                'exp': datetime.utcnow() + timedelta(hours=2)
            }
            token = jwt.encode(payload, app.JWT_SECRET, algorithm='HS256')
            client.set_cookie('jwt_token', token)
        else:
            client.delete_cookie('jwt_token')

        if method == 'GET':
            res = client.get(url, follow_redirects=False)
        else:
            res = client.post(url, follow_redirects=False)

        if res.status_code == expected_status:
            print(f"  [PASS] {desc} ({url}) -> Status {res.status_code}")
            passed += 1
            return True
        else:
            print(f"  [FAIL] {desc} ({url}) -> Expected {expected_status}, Got {res.status_code}")
            if res.status_code >= 500:
                print("      Error preview:", res.data.decode('utf-8', errors='ignore')[:300])
            failed += 1
            return False

    print("\n--- 1. Testing Authentication & Public Pages ---")
    test_endpoint("Root Redirect", 'GET', '/', expected_status=302)
    test_endpoint("Login Page", 'GET', '/login', expected_status=200)
    test_endpoint("Signup Page", 'GET', '/signup', expected_status=200)

    # Test actual Login POST request with Admin
    print("\n--- 2. Testing Role Login Form Submissions ---")
    roles_credentials = [
        ('Admin', 'admin@example.com', '1234', '/admin/dashboard'),
        ('Weaver', 'artisan@example.com', '1234', '/weaver_dashboard'),
        ('Supplier', 'supplier@example.com', '1234', '/supplier/dashboard'),
        ('Customer', 'customer@example.com', '1234', '/shop/home'),
        ('Delivery Partner', 'delivery@example.com', '1234', '/delivery/dashboard')
    ]

    for role_name, email, pwd, expected_redirect in roles_credentials:
        client.delete_cookie('jwt_token')
        res = client.post('/login', data={'email': email, 'password': pwd, 'role': role_name}, follow_redirects=False)
        if res.status_code == 302 and expected_redirect in res.headers.get('Location', ''):
            print(f"  [PASS] Login as {role_name} ({email}) -> Redirect to {expected_redirect}")
            passed += 1
        else:
            print(f"  [FAIL] Login as {role_name} ({email}) -> Got status {res.status_code}, Location: {res.headers.get('Location')}")
            failed += 1

    print("\n--- 3. Testing Admin Core Dashboards & Modules ---")
    admin_routes = [
        ("Admin Main Dashboard", "/admin/dashboard"),
        ("Artisans Master View", "/artisans"),
        ("Traditional Designs View", "/designs"),
        ("Raw Materials View", "/materials"),
        ("Weaver Management Module (Module 1)", "/weaver_module"),
        ("Raw Materials Module (Module 2)", "/raw_material_module"),
        ("Supplier Module (Module 3)", "/supplier_module"),
        ("Production Tracking Module (Module 4)", "/production_module"),
        ("Product Catalog Module (Module 5)", "/product_catalog_module"),
        ("Order Management Module (Module 6)", "/order_module"),
        ("Customer Management Module (Module 7)", "/customer_module"),
        ("Warehouse Inventory Module (Module 8)", "/inventory_module"),
        ("Payment & Billing Module (Module 9)", "/billing_module"),
        ("Logistics & Transport Module (Module 10)", "/logistics_module"),
        ("Demand Prediction (AI Module 12)", "/demand_prediction")
    ]
    for desc, route in admin_routes:
        test_endpoint(desc, 'GET', route, role='Admin', username='Super Admin')

    print("\n--- 4. Testing Weaver / Artisan Workspace ---")
    weaver_routes = [
        ("Weaver Dashboard", "/weaver_dashboard"),
        ("Weaver Products", "/artisan/products"),
        ("Weaver Production Tracker", "/artisan/production"),
        ("Weaver Orders", "/artisan/orders"),
        ("Weaver Inventory", "/artisan/inventory"),
        ("Weaver Earnings", "/artisan/earnings"),
        ("Weaver Shipments", "/artisan/shipments"),
        ("Weaver Sales Analytics", "/artisan/analytics/sales"),
        ("Weaver Performance", "/artisan/analytics/performance"),
        ("Weaver Reviews", "/artisan/reviews"),
        ("Weaver QR Verification", "/artisan/qr_verification"),
        ("Weaver Notifications", "/artisan/notifications"),
        ("Weaver Profile", "/artisan/profile")
    ]
    for desc, route in weaver_routes:
        test_endpoint(desc, 'GET', route, role='Weaver', user_id=2, username='Sunitha Weaver')

    print("\n--- 5. Testing Supplier Workspace ---")
    supplier_routes = [
        ("Supplier Dashboard", "/supplier/dashboard"),
        ("Supplier Pickup", "/supplier/pickup"),
        ("Supplier Active Shipments", "/supplier/active"),
        ("Supplier Schedule", "/supplier/schedule"),
        ("Supplier Earnings", "/supplier/earnings"),
        ("Supplier Tracking", "/supplier/tracking"),
        ("Supplier Analytics", "/supplier/analytics"),
        ("Supplier Settings", "/supplier/settings")
    ]
    for desc, route in supplier_routes:
        test_endpoint(desc, 'GET', route, role='Supplier', user_id=3, username='Karnataka Silk Hub')

    print("\n--- 6. Testing Customer / Buyer Marketplace ---")
    customer_routes = [
        ("Customer Dashboard", "/shop/home"),
        ("Customer Products Catalog", "/shop/products"),
        ("Customer Orders", "/shop/orders"),
        ("Customer Payment Portal", "/shop/payment"),
        ("Customer Tracking", "/shop/tracking"),
        ("Customer Wishlist", "/shop/wishlist"),
        ("Customer Reviews", "/shop/reviews"),
        ("Customer Profile", "/shop/profile")
    ]
    for desc, route in customer_routes:
        test_endpoint(desc, 'GET', route, role='Customer', user_id=4, username='Pooja Hegde')

    print("\n--- 7. Testing Delivery Partner Portal ---")
    test_endpoint("Delivery Partner Dashboard", 'GET', '/delivery/dashboard', role='Delivery Partner', user_id=5, username='Raju Express')

    print("\n--- 8. Testing REST APIs ---")
    api_endpoints = [
        ("API Products", "/api/products"),
        ("API Orders", "/api/orders"),
        ("API Suppliers", "/api/suppliers"),
        ("API Inventory", "/api/inventory"),
        ("API Payments", "/api/payments"),
        ("API Shipments", "/api/shipments"),
        ("API Dashboard Stats", "/api/dashboard/stats")
    ]
    for desc, route in api_endpoints:
        test_endpoint(desc, 'GET', route, role='Admin')

    print("\n" + "=" * 60)
    print(f"TEST SUMMARY: {passed} PASSED, {failed} FAILED (TOTAL {passed + failed})")
    print("=" * 60)

if __name__ == '__main__':
    run_tests()
