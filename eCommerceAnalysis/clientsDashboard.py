import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
from clientsQueries import *

def show_clients_dashboard(engine):
    show_avg_purchase_by_state(engine)
    show_avg_purchase_by_city(engine)
    show_top_10_customers_by_sales_volume(engine)
    show_total_products_by_customer(engine)
    show_avg_reviews_by_state(engine)
    show_avg_reviews_by_city(engine)

# Consulta 6: valor médio de compras efetuadas por clientes de todas as cidades.
def show_avg_purchase_by_city(engine):
    st.markdown("<h2 style='text-align: center; font-size: 24px;'>Valor Médio das Compras Efetuadas por Clientes de Cada Cidade</h2>", unsafe_allow_html=True)
    data = get_avg_purchase_all_cities(engine)
    df = pd.DataFrame(data, columns=["City", "Avg Purchase"])
    selected_city = st.selectbox("Selecione a cidade", df["City"].unique())
    city_data = df[df["City"] == selected_city]
    avg_purchase = city_data["Avg Purchase"].values[0]
    st.markdown(f"O valor médio das compras realizadas na cidade de {selected_city} é: **R$ {avg_purchase:.2f}**")

# Consulta 7: valor médio de compras efetuadas por clientes de todos os estados.
def show_avg_purchase_by_state(engine):
    st.markdown("<h2 style='text-align: center; font-size: 24px;'>Valor Médio das Compras Efetuadas por Clientes de Cada Estado</h2>", unsafe_allow_html=True)
    data = get_avg_purchase_by_state(engine)
    df = pd.DataFrame(data, columns=["State", "Avg Purchase"])
    st.bar_chart(df.set_index("State")["Avg Purchase"])

# Consulta 37: top 10 clientes com maior volume de compras.
def show_top_10_customers_by_sales_volume(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Top 10 Clientes com Maior Volume de Compras</h2>", unsafe_allow_html=True)
    data = get_top_10_customers_by_sales_volume(engine)
    df = pd.DataFrame(data, columns=["Customer ID", "Customer City", "Total Purchases"])
    df = df.sort_values(by='Total Purchases', ascending=False)
    st.bar_chart(df.set_index("Customer ID")["Total Purchases"])

# Consulta 18: total de produtos comprados por cliente.
def show_total_products_by_customer(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Total de Produtos Comprados por Cliente</h2>", unsafe_allow_html=True)
    data = get_total_products_by_customer(engine)
    df = pd.DataFrame(data, columns=["Customer ID", "Total Products"])
    
    customer_id = st.text_input("Digite o ID do cliente")
    
    if customer_id:
        customer_data = df[df["Customer ID"] == customer_id]
        
        if not customer_data.empty:
            total_products = customer_data["Total Products"].values[0]
            st.markdown(f"O total de produtos comprados por esse cliente é: **{total_products}**")
        else:
            st.markdown(f"Cliente com ID {customer_id} não encontrado.")

# Consulta 51: média de avaliações dos clientes por estado.
def show_avg_reviews_by_state(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Média de Avaliações dos Clientes por Estado</h2>", unsafe_allow_html=True)
    data = get_avg_reviews_by_state(engine)
    df = pd.DataFrame(data, columns=["State", "Average Reviews"])
    df["Average Reviews"] = df["Average Reviews"].astype(float)  
    df = df.sort_values(by="Average Reviews", ascending=False) 
    st.bar_chart(df.set_index("State")["Average Reviews"])

# Consulta 47: média de avaliações por cidade.
def show_avg_reviews_by_city(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Média de Avaliações dos Clientes por Cidade</h2>", unsafe_allow_html=True)
    data = get_avg_reviews_by_city(engine)
    df = pd.DataFrame(data, columns=["City", "Average Reviews"])
    selected_city = st.selectbox("Selecione a cidade", df["City"].unique())
    
    city_data = df[df["City"] == selected_city]
    avg_reviews = city_data["Average Reviews"].values[0]
    st.markdown(f"A média de avaliações dos clientes na cidade de {selected_city} é: **{avg_reviews:.2f}**")

