import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine, text
from ordersDashboard import show_orders_dashboard

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

    # Inicialize estados no session_state
    if 'pesquisou' not in st.session_state:
        st.session_state.pesquisou = False
    if 'exibindo_tabela' not in st.session_state:
        st.session_state.exibindo_tabela = False
    if 'tabela_selecionada' not in st.session_state:
        st.session_state.tabela_selecionada = None

    # Lógica de botão de pesquisa
    if st.sidebar.button("Pesquisar"):
        st.session_state.pesquisou = True
        st.session_state.exibindo_tabela = False  # Desative exibição de tabelas
        st.session_state.tabela_selecionada = None

    # Atualizar o estado se uma tabela for selecionada
    tabelas = []
    if categoria_selecionada == "Pedidos":
        tabelas = ["olist_order_items_dataset", "olist_order_payments_dataset", "olist_order_reviews_dataset", "olist_orders_dataset"]
    elif categoria_selecionada == "Clientes":
        tabelas = ["olist_customers_dataset", "olist_geolocation_dataset"]
    elif categoria_selecionada == "Vendedores":
        tabelas = ["olist_sellers_dataset"]
    elif categoria_selecionada == "Produtos":
        tabelas = ["olist_products_dataset", "product_category_name_translation"]

    # Exibir tabelas relacionadas
    if categoria_selecionada != "Categoria...":
        st.sidebar.header("Tabelas Relacionadas:")
        for table in tabelas:
            if st.sidebar.button(table):
                # Atualize os estados imediatamente ao clicar
                st.session_state.pesquisou = False  # Gráficos não devem ser exibidos
                st.session_state.exibindo_tabela = True
                st.session_state.tabela_selecionada = table

    # Controle de exibição
    if st.session_state.exibindo_tabela and st.session_state.tabela_selecionada:
        # Exibir a tabela selecionada
        display_table(engine, st.session_state.tabela_selecionada)
    elif st.session_state.pesquisou and categoria_selecionada == "Pedidos":
        # Exibir os gráficos se nenhuma tabela estiver sendo exibida
        show_orders_dashboard(engine)

def display_table(engine, table_name):
    st.markdown(f"<h3 style='text-align: center;'>Tabela {table_name}</h3>", unsafe_allow_html=True)
    df = load_data_from_db(engine, table_name)
    st.write(df)