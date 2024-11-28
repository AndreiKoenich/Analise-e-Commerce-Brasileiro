import pandas as pd
import streamlit as st

def load_data_from_db(engine, table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    return df

def show_info(engine):
    st.sidebar.header("Filtros de Análise")
    categoria_selecionada = st.sidebar.selectbox("Selecione uma categoria", ["Pedidos", "Clientes", "Vendedores", "Produtos"])

    if 'tabelas' not in st.session_state:
        st.session_state.tabelas = []

    if 'tabela_selecionada' not in st.session_state:
        st.session_state.tabela_selecionada = None

    if st.sidebar.button("Pesquisar"):
        st.session_state.pesquisou = True
        if categoria_selecionada == "Pedidos":
            st.session_state.tabelas = ["olist_order_items_dataset", "olist_order_payments_dataset", "olist_order_reviews_dataset", "olist_orders_dataset"]
        elif categoria_selecionada == "Clientes":
            st.session_state.tabelas = ["olist_customers_dataset", "olist_geolocation_dataset"]
        elif categoria_selecionada == "Vendedores":
            st.session_state.tabelas = ["olist_sellers_dataset"]
        elif categoria_selecionada == "Produtos":
            st.session_state.tabelas = ["olist_products_dataset", "product_category_name_translation"]

    if st.session_state.tabelas:
        st.sidebar.header("Tabelas Relacionadas:")
        for table in st.session_state.tabelas:
            if st.sidebar.button(table):
                st.session_state.tabela_selecionada = table

    if st.session_state.tabela_selecionada:
        st.markdown(
            f"<h3 style='text-align: center;'>Tabela {st.session_state.tabela_selecionada}.csv</h3>", 
            unsafe_allow_html=True
        )
        df = load_data_from_db(engine, st.session_state.tabela_selecionada)
        st.write(df)