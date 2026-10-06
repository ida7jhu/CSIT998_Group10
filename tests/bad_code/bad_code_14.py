import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()


def many_tables_nested_queries():
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    results = []

    for customer in customers:
        cursor.execute(f"SELECT * FROM orders WHERE customer_id = {customer['customer_id']}")
        orders = cursor.fetchall()

        for order in orders:
            cursor.execute(f"SELECT * FROM order_items WHERE order_id = {order['order_id']}")
            items = cursor.fetchall()

            for item in items:
                cursor.execute(f"SELECT * FROM products WHERE product_id = {item['product_id']}")
                products = cursor.fetchall()

                for product in products:
                    cursor.execute(f"SELECT * FROM categories WHERE category_id = {product['category_id']}")
                    categories = cursor.fetchall()

                    for category in categories:
                        results.append({
                            "customer_name": customer["name"],
                            "order_date": order["date"],
                            "item_quantity": item["quantity"],
                            "product_name": product["name"],
                            "category_name": category["name"]
                        })
    return results


def many_tables_python_in_memory_join():
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.execute("SELECT * FROM order_items")
    items = cursor.fetchall()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    results = []
    for c in customers:
        for o in orders:
            if o["customer_id"] == c["customer_id"]:
                for i in items:
                    if i["order_id"] == o["order_id"]:
                        for p in products:
                            if p["product_id"] == i["product_id"]:
                                for cat in categories:
                                    if cat["category_id"] == p["category_id"]:
                                        results.append((c, o, i, p, cat))
    return results


def many_tables_implicit_sql_join():
    cursor.execute("""
                   SELECT c.name, o.date, i.quantity, p.name, cat.name
                   FROM customers c,
                        orders o,
                        order_items i,
                        products p,
                        categories cat
                   WHERE c.customer_id = o.customer_id
                     AND o.order_id = i.order_id
                     AND i.product_id = p.product_id
                     AND p.category_id = cat.category_id
                   """)

    return cursor.fetchall()