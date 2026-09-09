"""
HERITAGE HANDLOOM - DATABASE CONNECTION LOGIC

This file documents the specific SQL logic and application flows required 
to connect the 5 pillars of the platform: 
Customers, Products, Artisans, Suppliers, and Delivery Partners.

1. ORDERS CONNECT CUSTOMERS & PRODUCTS
-------------------------------------------------
When a Customer (user_id) checks out a Cart containing Product (product_id):
SQL:
    INSERT INTO orders (customer_id, total_amount, status) VALUES (%s, %s, 'Processing');
    -- Get last_insert_id() -> order_id
    INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (%s, %s, %s, %s);

2. PRODUCTS CONNECT ARTISANS
-------------------------------------------------
Every Product has a distinct Artisan origin.
SQL:
    SELECT p.product_name, p.price, a.name AS artisan_name, a.village 
    FROM product_catalog p
    JOIN artisans a ON p.artisan_id = a.artisan_id
    WHERE p.product_id = %s;

3. SUPPLIERS CONNECT RAW MATERIALS
-------------------------------------------------
Suppliers provide inventory to the ecosystem.
SQL:
    SELECT r.material_name, r.quantity_in_stock, s.company_name
    FROM raw_materials r
    JOIN suppliers s ON r.supplier_id = s.supplier_id;

4. INVENTORY UPDATES AUTOMATICALLY (Application Logic Trigger)
-------------------------------------------------
When an Order is confirmed, inventory must decrease automatically.
SQL:
    UPDATE product_catalog 
    SET stock_quantity = stock_quantity - %s 
    WHERE product_id = %s AND stock_quantity >= %s;

When a Supplier delivery is confirmed:
SQL:
    UPDATE raw_materials 
    SET quantity_in_stock = quantity_in_stock + %s 
    WHERE material_id = %s;

5. PAYMENTS CONNECT ORDERS
-------------------------------------------------
Billing ties directly to the unique order.
SQL:
    INSERT INTO billing_payments (order_id, amount, payment_method, transaction_status)
    VALUES (%s, %s, 'UPI', 'Completed');

6. SHIPMENT UPDATES CONNECT DELIVERY PARTNERS
-------------------------------------------------
When an order is ready for dispatch, it's assigned to a Delivery Partner (user_id with role 'Delivery Partner').
SQL:
    INSERT INTO logistics (order_id, delivery_partner_id, current_status, route_gps)
    VALUES (%s, %s, 'In Transit', '{"lat": 12.97, "lng": 77.59}');

When the partner marks it Delivered:
SQL:
    UPDATE logistics SET current_status = 'Delivered' WHERE shipment_id = %s;
    UPDATE orders SET status = 'Delivered' WHERE order_id = (SELECT order_id FROM logistics WHERE shipment_id = %s);
"""

print("Database connection logic documented.")
