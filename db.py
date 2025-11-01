import sqlite3

def get_connection():
    return sqlite3.connect("challenge.db")

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de restaurantes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurant (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        city TEXT NOT NULL
    );
    """)

    # Tabela de produtos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    );
    """)

        # Tabela de vendas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sale (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        total REAL NOT NULL,
        sale_date TEXT NOT NULL,
        FOREIGN KEY (restaurant_id) REFERENCES restaurant(id),
        FOREIGN KEY (product_id) REFERENCES product(id)
    );
    """)


    conn.commit()
    conn.close()
    print("✅ Banco de dados e tabelas criados com sucesso!")

if __name__ == "__main__":
    create_tables()
