# desafio.py
import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

# ===========================
# 1. Conectar ao banco SQLite
# ===========================
# Pode usar ":memory:" para banco em memória, ou "challenge.db" para arquivo
conn = sqlite3.connect("challenge.db")
cursor = conn.cursor()

# ===========================
# 2. Criar tabelas
# ===========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS restaurant (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS payment_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sale (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER,
    payment_type_id INTEGER,
    amount REAL,
    sale_date TEXT,
    FOREIGN KEY(restaurant_id) REFERENCES restaurant(id),
    FOREIGN KEY(payment_type_id) REFERENCES payment_type(id)
)
""")
conn.commit()

# ===========================
# 3. Inserir dados iniciais
# ===========================
# Tipos de pagamento
payment_types = ["Cash", "Credit Card", "Debit Card", "Voucher"]
cursor.executemany("INSERT INTO payment_type (name) VALUES (?)", [(p,) for p in payment_types])

# Restaurantes
restaurants = [("Nola Central", "New Orleans"), ("Cafe du Monde", "New Orleans")]
cursor.executemany("INSERT INTO restaurant (name, city) VALUES (?, ?)", restaurants)

conn.commit()

# ===========================
# 4. Gerar dados de vendas
# ===========================
fake = Faker()

def generate_sales(months=6, sales_per_restaurant=50):
    today = datetime.today()
    for r_id in range(1, len(restaurants)+1):
        for _ in range(sales_per_restaurant):
            days_ago = random.randint(0, months*30)
            sale_date = today - timedelta(days=days_ago)
            amount = round(random.uniform(5, 200), 2)
            payment_type_id = random.randint(1, len(payment_types))
            cursor.execute("""
                INSERT INTO sale (restaurant_id, payment_type_id, amount, sale_date)
                VALUES (?, ?, ?, ?)
            """, (r_id, payment_type_id, amount, sale_date.strftime("%Y-%m-%d")))
    conn.commit()

generate_sales()

# ===========================
# 5. Consultas de exemplo
# ===========================
print("=== Total de vendas por restaurante ===")
cursor.execute("""
SELECT r.name, SUM(s.amount) as total_sales
FROM sale s
JOIN restaurant r ON s.restaurant_id = r.id
GROUP BY r.name
""")
for row in cursor.fetchall():
    print(row)

print("\n=== Vendas por tipo de pagamento ===")
cursor.execute("""
SELECT p.name, SUM(s.amount) as total_sales
FROM sale s
JOIN payment_type p ON s.payment_type_id = p.id
GROUP BY p.name
""")
for row in cursor.fetchall():
    print(row)

# Fechar conexão
conn.close()
