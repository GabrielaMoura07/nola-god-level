import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# === CONFIGURAÇÕES DO APP ===
st.set_page_config(page_title="God Level Restaurant Analytics", layout="wide")

# === FUNÇÃO DE CARREGAMENTO ===
@st.cache_data
def load_data():
    conn = sqlite3.connect("restaurant_data.db")
    query = """
        SELECT s.id, r.name AS restaurant, r.city, r.channel, 
               p.name AS product, s.quantity, s.total, s.sale_date
        FROM sale s
        JOIN restaurant r ON s.restaurant_id = r.id
        JOIN product p ON s.product_id = p.id
    """
    df = pd.read_sql_query(query, conn)
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    return df

# === CARREGAR DADOS ===
st.title("📊 God Level - Restaurante Dashboard")
data = load_data()

# === SIDEBAR ===
st.sidebar.header("Filtros")
city_filter = st.sidebar.multiselect("Cidade", data["city"].unique())
channel_filter = st.sidebar.multiselect("Canal", data["channel"].unique())
product_filter = st.sidebar.multiselect("Produto", data["product"].unique())

filtered_data = data.copy()
if city_filter:
    filtered_data = filtered_data[filtered_data["city"].isin(city_filter)]
if channel_filter:
    filtered_data = filtered_data[filtered_data["channel"].isin(channel_filter)]
if product_filter:
    filtered_data = filtered_data[filtered_data["product"].isin(product_filter)]

# === MÉTRICAS ===
st.subheader("📈 Visão Geral")
col1, col2, col3 = st.columns(3)
col1.metric("Vendas Totais (R$)", f"{filtered_data['total'].sum():,.2f}")
col2.metric("Quantidade Vendida", f"{filtered_data['quantity'].sum():,}")
col3.metric("Ticket Médio (R$)", f"{filtered_data['total'].sum()/max(1, filtered_data['quantity'].sum()):,.2f}")

# === GRÁFICOS ===
st.subheader("📊 Tendência de Vendas ao Longo do Tempo")
sales_over_time = filtered_data.groupby("sale_date")["total"].sum().reset_index()
fig1 = px.line(sales_over_time, x="sale_date", y="total", title="Receita Diária", markers=True)
st.plotly_chart(fig1, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("🍽️ Vendas por Restaurante")
    sales_by_restaurant = filtered_data.groupby("restaurant")["total"].sum().reset_index()
    fig2 = px.bar(sales_by_restaurant, x="restaurant", y="total", color="restaurant", title="Receita por Restaurante")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("📦 Produtos Mais Vendidos")
    top_products = filtered_data.groupby("product")["quantity"].sum().reset_index().sort_values("quantity", ascending=False)
    fig3 = px.bar(top_products.head(10), x="product", y="quantity", color="product", title="Top 10 Produtos")
    st.plotly_chart(fig3, use_container_width=True)

# === COMPARAÇÃO DE PERÍODOS ===
st.subheader("📅 Comparação entre Períodos")
col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Data inicial", value=data["sale_date"].min().date())
with col2:
    end = st.date_input("Data final", value=data["sale_date"].max().date())

mask = (data["sale_date"].dt.date >= start) & (data["sale_date"].dt.date <= end)
period_data = data[mask]
st.write(f"Período selecionado: **{start} → {end}**")

sales_period = period_data.groupby("sale_date")["total"].sum().reset_index()
fig4 = px.area(sales_period, x="sale_date", y="total", title="Evolução das Vendas no Período", color_discrete_sequence=["#00CC96"])
st.plotly_chart(fig4, use_container_width=True)
