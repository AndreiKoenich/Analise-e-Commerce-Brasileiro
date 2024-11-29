import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine, text
from ordersDashboard import show_orders_dashboard

def load_data_from_db(engine, table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    return df

def show_info(engine):
    st.sidebar.header("Filtros de Análise")
    categoria_selecionada = st.sidebar.selectbox(
        "Selecione uma categoria de consultas:", 
        ["Categoria...", "Pedidos", "Clientes", "Vendedores", "Produtos"],
        index=0  # O primeiro item (índice 0) será o item padrão
    )

    if st.sidebar.button("Pesquisar"):
        st.session_state.pesquisou = True
        if categoria_selecionada == "Pedidos":
            show_orders_dashboard(engine)
        elif categoria_selecionada == "Clientes":
            show_orders_dashboard(engine)
        elif categoria_selecionada == "Vendedores":
            show_orders_dashboard(engine)
        elif categoria_selecionada == "Produtos":
            show_orders_dashboard(engine)

    tabelas = []
    if categoria_selecionada == "Pedidos":
        tabelas = ["olist_order_items_dataset", "olist_order_payments_dataset", "olist_order_reviews_dataset", "olist_orders_dataset"]
    elif categoria_selecionada == "Clientes":
        tabelas = ["olist_customers_dataset", "olist_geolocation_dataset"]
    elif categoria_selecionada == "Vendedores":
        tabelas = ["olist_sellers_dataset"]
    elif categoria_selecionada == "Produtos":
        tabelas = ["olist_products_dataset", "product_category_name_translation"]

    if categoria_selecionada != "Categoria...":
        st.sidebar.header("Tabelas Relacionadas:")
        for table in tabelas:
            if st.sidebar.button(table):
                display_table(engine, table)
    else:
        st.session_state.pesquisou = False

def display_table(engine, table_name):
    st.session_state.pesquisou = True
    st.markdown(f"<h3 style='text-align: center;'>Tabela {table_name}</h3>", unsafe_allow_html=True)
    df = load_data_from_db(engine, table_name)
    st.write(df)