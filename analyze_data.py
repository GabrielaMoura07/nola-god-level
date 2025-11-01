import pandas as pd
from db import get_connection

def analyze_sales():
    conn = get_connection()

    query = """
    SELECT 
        r.name AS restaurant,
        p.name AS product,
        SUM(s.quantity) AS total_sold,
        SUM(s.total) AS revenue
    FROM sale s
    JOIN restaurant r ON s.restaurant_id = r.id
    JOIN product p ON s.product_id = p.id
    GROUP BY r.name, p.name
    ORDER BY revenue DESC
    """
    
    df = pd.read_sql_query(query, conn)
    print("===== 🧾 RELATÓRIO DE VENDAS =====")
    print(df)
    print("\n💰 Receita total:", df['revenue'].sum())
    conn.close()

if __name__ == "__main__":
    analyze_sales()
