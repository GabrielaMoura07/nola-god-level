import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker("pt_BR")

# === CONFIGURAÇÕES ===
DB_NAME = "restaurant_data.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.executescript("""
    DROP TABLE IF EXISTS sale;
    DROP TABLE IF EXISTS product;
    DROP TABLE IF EXISTS restaurant;

    CREATE TABLE restaurant (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        city TEXT NOT NULL,
        channel TEXT NOT NULL
    );

    CREATE TABLE product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    );

    CREATE TABLE sale (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        total REAL NOT NULL,
        sale_date TEXT NOT NULL,
        FOREIGN KEY (restaurant_id) REFERENCES restaurant (id),
        FOREIGN KEY (product_id) REFERENCES product (id)
    );
    """)

    conn.commit()
    conn.close()
    print("✅ Banco de dados e tabelas criados com sucesso!")

def populate_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Restaurantes
    restaurants = [(fake.company(), fake.city(), random.choice(["iFood", "Rappi", "Presencial", "WhatsApp"])) for _ in range(10)]
    cursor.executemany("INSERT INTO restaurant (name, city, channel) VALUES (?, ?, ?)", restaurants)

    # Produtos
    products = [
        ("Hambúrguer Clássico", 25.0),
        ("Pizza Margerita", 45.0),
        ("Suco Natural", 8.0),
        ("Refrigerante Lata", 6.0),
        ("Combo Executivo", 35.0),
        ("Salada Caesar", 22.0)
    ]
    cursor.executemany("INSERT INTO product (name, price) VALUES (?, ?)", products)

    # Vendas
    start_date = datetime.now() - timedelta(days=180)
    sales = []
    for _ in range(3000):  # 3 mil vendas simuladas
        restaurant_id = random.randint(1, len(restaurants))
        product_id = random.randint(1, len(products))
        quantity = random.randint(1, 5)
        price = products[product_id - 1][1]
        total = round(price * quantity, 2)
        sale_date = (start_date + timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d")

        sales.append((restaurant_id, product_id, quantity, total, sale_date))

    cursor.executemany(
        "INSERT INTO sale (restaurant_id, product_id, quantity, total, sale_date) VALUES (?, ?, ?, ?, ?)",
        sales
    )

    conn.commit()
    conn.close()
    print("✅ Dados populados com sucesso!")

def main():
    create_tables()
    populate_data()
    print("🎉 Banco pronto para uso no Streamlit!")

if __name__ == "__main__":
    main()
