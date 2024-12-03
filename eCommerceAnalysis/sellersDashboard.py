import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
from sellersQueries import *

def show_sellers_dashboard(engine):
    show_total_sellers_by_state(engine)
    show_top_10_cities_by_sellers(engine)
    show_sellers_count_by_city(engine)
    show_avg_seller_reviews_by_state(engine)
    show_items_sold_by_seller(engine)
    show_total_sales_by_seller(engine)
    show_sellers_count_by_category(engine)

# Consulta 52: quantidade total de vendedores por estado.
def show_total_sellers_by_state(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Quantidade Total de Vendedores por Estado</h2>", unsafe_allow_html=True)
    data = get_total_sellers_by_state(engine)
    df = pd.DataFrame(data, columns=["State", "Seller Count"])
    st.bar_chart(df.set_index("State")["Seller Count"])

# Consulta 21: média de avaliação dos vendedores por estado.
def show_avg_seller_reviews_by_state(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Média de Avaliação dos Vendedores por Estado</h2>", unsafe_allow_html=True)
    data = get_avg_seller_reviews_by_state(engine)
    df = pd.DataFrame(data, columns=["State", "Average Review Score"])
    df["Average Review Score"] = df["Average Review Score"].astype(float)
    st.bar_chart(df.set_index("State")["Average Review Score"])
    
# Consulta 31: número de itens vendidos por vendedor.
def show_items_sold_by_seller(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Quantidade de Produtos Vendidos por Vendedor</h2>", unsafe_allow_html=True)
    data = get_items_sold_by_seller(engine)
    df = pd.DataFrame(data, columns=["Seller ID", "Total Items"])
    
    seller_id = st.text_input("Digite o ID do vendedor")
    
    if seller_id:
        seller_data = df[df["Seller ID"] == seller_id]
        
        if not seller_data.empty:
            total_items = seller_data["Total Items"].values[0]
            st.markdown(f"O número total de itens vendidos por este vendedor é: **{total_items}**")
        else:
            st.markdown(f"Vendedor com ID {seller_id} não encontrado.")

# Consulta 16: valor total em vendas por vendedor.
def show_total_sales_by_seller(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Valor Total Obtido em Vendas por Vendedor</h2>", unsafe_allow_html=True)
    data = get_sales_by_seller(engine)
    df = pd.DataFrame(data, columns=["Seller ID", "Total Sales"])
    
    seller_id = st.text_input("Digite o ID do vendedor", key="total_sales_seller_input")
    
    if seller_id:
        seller_data = df[df["Seller ID"] == seller_id]
        
        if not seller_data.empty:
            total_sales = seller_data["Total Sales"].values[0]
            st.markdown(f"O total de vendas realizadas por esse vendedor é: **R${total_sales:,.2f}**")
        else:
            st.markdown(f"Vendedor com ID {seller_id} não encontrado.")

# Consulta 58: quantidade total de vendedores por cidade.
def show_sellers_count_by_city(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Quantidade Total de Vendedores por Cidade</h2>", unsafe_allow_html=True)
    data = get_sellers_count_by_city(engine)
    df = pd.DataFrame(data, columns=["City", "Seller Count"])
    selected_city = st.selectbox("Selecione a cidade", df["City"].unique())
    city_data = df[df["City"] == selected_city]
    seller_count = city_data["Seller Count"].values[0]
    st.markdown(f"A quantidade de vendedores na cidade de {selected_city} é: {seller_count}")

# Consulta 59: top 10 cidades com maior quantidade de vendedores.
def show_top_10_cities_by_sellers(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>As 10 Cidades com Maior Quantidade de Vendedores</h2>", unsafe_allow_html=True)
    data = get_top_10_cities_by_sellers(engine)
    df = pd.DataFrame(data, columns=["City", "Seller Count"])
    df = df.sort_values(by='Seller Count', ascending=False)
    st.bar_chart(df.set_index("City")["Seller Count"])

# Consulta 60: quantidade de vendedores por categoria de produto.
def show_sellers_count_by_category(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Quantidade de Vendedores por Categoria de Produto</h2>", unsafe_allow_html=True)
    
    data = get_sellers_count_by_category(engine)
    categories = [row[0] for row in data]
    
    category = st.selectbox("Selecione a categoria de produto", categories)
    
    if category:
        category_data = [row for row in data if row[0] == category]
        if category_data:
            seller_count = category_data[0][1]
            st.write(f"A quantidade de vendedores para a categoria '{category}' é: {seller_count}")
        else:
            st.write(f"Nenhuma informação encontrada para a categoria '{category}'.")