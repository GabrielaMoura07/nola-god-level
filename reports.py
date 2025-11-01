# reports.py
from db import get_connection

conn = get_connection()
cursor = conn.cursor()

# Vendas por restaurante por mês
print("=== Vendas por restaurante por mês ===")
cursor.execute("""
SELECT r.name,
       strftime('%Y-%m', s.sale_date) as month,
       SUM(s.amount) as total_sales
FROM sale s
JOIN restaurant r ON s.restaurant_id = r.id
GROUP BY r.name, month
ORDER BY r.name, month
""")
for row in cursor.fetchall():
    print(row)

# Ticket médio por restaurante
print("\n=== Ticket médio por restaurante ===")
cursor.execute("""
SELECT r.name, AVG(s.amount) as avg_ticket
FROM sale s
JOIN restaurant r ON s.restaurant_id = r.id
GROUP BY r.name
""")
for row in cursor.fetchall():
    print(row)

# Top tipos de pagamento
print("\n=== Top tipos de pagamento ===")
cursor.execute("""
SELECT p.name, SUM(s.amount) as total_sales
FROM sale s
JOIN payment_type p ON s.payment_type_id = p.id
GROUP BY p.name
ORDER BY total_sales DESC
""")
for row in cursor.fetchall():
    print(row)

# Faturamento total
print("\n=== Faturamento total ===")
cursor.execute("SELECT SUM(amount) FROM sale")
total = cursor.fetchone()[0]
print(f"Faturamento total: {total:.2f}")

conn.close()
