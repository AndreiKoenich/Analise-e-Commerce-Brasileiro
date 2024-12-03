import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine, text
from showHomepage import show_homepage
from ordersDashboard import show_orders_dashboard
from clientsDashboard import show_clients_dashboard
from sellersDashboard import show_sellers_dashboard
from productsDashboard import show_products_dashboard

def load_data_from_db(engine, table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    return df

def showSidebar(engine):
    st.sidebar.header("Filtros de Análise")
    categoria_selecionada = st.sidebar.selectbox(
        "Selecione uma categoria de consultas:", 
        ["Categoria...", "Pedidos", "Clientes", "Vendedores", "Produtos"],
        index=0
    )

    if 'pesquisou' not in st.session_state:
        st.session_state.pesquisou = False
    if 'exibindo_tabela' not in st.session_state:
        st.session_state.exibindo_tabela = False
    if 'tabela_selecionada' not in st.session_state:
        st.session_state.tabela_selecionada = None

    if st.sidebar.button("Pesquisar"):
        st.session_state.pesquisou = True
        st.session_state.exibindo_tabela = False  
        st.session_state.tabela_selecionada = None

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
                st.session_state.pesquisou = False 
                st.session_state.exibindo_tabela = True
                st.session_state.tabela_selecionada = table

    if st.session_state.exibindo_tabela and st.session_state.tabela_selecionada:
        display_table(engine, st.session_state.tabela_selecionada)
    elif st.session_state.pesquisou and categoria_selecionada == "Pedidos":
        show_orders_dashboard(engine)
    elif st.session_state.pesquisou and categoria_selecionada == "Clientes":
        show_clients_dashboard(engine)
    elif st.session_state.pesquisou and categoria_selecionada == "Vendedores":
        show_sellers_dashboard(engine)
    elif st.session_state.pesquisou and categoria_selecionada == "Produtos":
        show_products_dashboard(engine)
    elif st.session_state.pesquisou and categoria_selecionada == "Categoria...":
        show_homepage()

def display_table(engine, table_name):
    st.markdown(f"<h3 style='text-align: center;'>Tabela {table_name}</h3>", unsafe_allow_html=True)
    df = load_data_from_db(engine, table_name)
    st.write(df)