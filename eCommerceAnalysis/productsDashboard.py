import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
from productsQueries import *
from utils import estado_dict

def show_products_dashboard(engine):
    show_top_10_categories(engine)
    show_top_categories_by_year_and_month(engine)
    show_top_categories_by_state(engine)
    show_total_sales_by_category(engine)
    show_best_product_categories(engine)
    show_avg_review_by_category(engine)
    show_top_10_freight_value_categories(engine)
    show_total_freight_value_by_category(engine)
    show_sales_by_category_state(engine)

# Consulta 63: as dez categorias mais adquiridas.
def show_top_10_categories(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>As 10 Categorias de Produtos Mais Adquiridas</h2>", unsafe_allow_html=True)
    data = get_top_10_categories(engine)
    df = pd.DataFrame(data, columns=["product_category_name", "total_pedidos"])
    st.bar_chart(df.set_index("product_category_name")["total_pedidos"])

# Consulta 3: categorias mais compradas em um ano/mês.
def show_top_categories_by_year_and_month(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Categorias de Produtos Mais Compradas em um Período</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Selecione o Ano", [2016, 2017, 2018], index=1)
    with col2:
        selected_month = st.selectbox("Selecione o Mês", list(range(1, 13)), format_func=lambda x: f"{x:02d}")

    data = get_top_categories(engine, selected_year, selected_month)
    df = pd.DataFrame(data, columns=["Categoria", "Total de Compras"])

    if df.empty:
        st.markdown("<p style='text-align: center;'>Nenhum dado encontrado para o período selecionado.</p>", unsafe_allow_html=True)
    else:
        fig = px.bar(
            df,
            x="Categoria",
            y="Total de Compras",
            title=f"Top 10 Categorias Mais Compradas - {selected_month:02d}/{selected_year}",
            text="Total de Compras",
        )
        fig.update_layout(title_x=0.5, xaxis_title="Categorias", yaxis_title="Total de Compras")
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Consulta 61: top 10 categorias mais adquiridas em um determinado estado.
def show_top_categories_by_state(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>As 10 Categorias Mais Adquiridas por Estado</h2>", unsafe_allow_html=True)
    reversed_estado_dict = {v: k for k, v in estado_dict.items()}
    states = list(estado_dict.values())
    selected_state_name = st.selectbox("Selecione o Estado", states)

    if selected_state_name:
        selected_state = reversed_estado_dict[selected_state_name]
        data = get_top_categories_by_state(engine, selected_state)
        df = pd.DataFrame(data, columns=["Categoria", "Total de Compras"])

        if df.empty:
            st.markdown("<p style='text-align: center;'>Nenhum dado encontrado para o estado selecionado.</p>", unsafe_allow_html=True)
        else:
            fig = px.bar(
                df,
                x="Categoria",
                y="Total de Compras",
                title=f"Top 10 Categorias Mais Adquiridas",
                text="Total de Compras",
            )
            fig.update_layout(title_x=0.5, xaxis_title="Categorias", yaxis_title="Total de Compras")
            st.plotly_chart(fig, use_container_width=True)

# Consulta 10: total de vendas por categoria de produto.
def show_total_sales_by_category(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Valor Total em Vendas por Categoria de Produto</h2>", unsafe_allow_html=True)
    data = get_total_sales_by_category(engine)
    categories = [row[0] for row in data]
    category = st.selectbox("Selecione a categoria de produto", categories)
    if category:
        category_data = [row for row in data if row[0] == category]
        if category_data:
            st.write(f"Valor total em vendas para a categoria '{category}': R${category_data[0][1]:,.2f}")
        else:
            st.write(f"Nenhuma venda encontrada para a categoria '{category}'.")

# Consulta 1: top 10 categorias de produtos melhor avaliadas.
def show_best_product_categories(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>As 10 Categorias de Produtos Melhor Avaliadas</h2>", unsafe_allow_html=True)
    data = best_products(engine)
    df = pd.DataFrame(data, columns=["Category", "Average Review Score"])
    df["Average Review Score"] = pd.to_numeric(df["Average Review Score"], errors='coerce')
    st.bar_chart(df.set_index("Category")["Average Review Score"])

# Consulta 11: média de avaliação dos produtos por categoria.
def show_avg_review_by_category(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Média de Avaliação dos Produtos por Categoria</h2>", unsafe_allow_html=True)
    
    data = get_avg_review_by_category(engine)
    categories = [row[0] for row in data]
    
    category = st.selectbox("Selecione a categoria de produto", categories)
    
    if category:
        category_data = [row for row in data if row[0] == category]
        if category_data:
            avg_review = float(category_data[0][1])
            st.write(f"A média de avaliação da categoria '{category}' é: {avg_review:.2f}")
        else:
            st.write(f"Nenhuma avaliação encontrada para a categoria '{category}'.")

# Consulta 54: top 10 categorias com maior valor gasto com frete.
def show_top_10_freight_value_categories(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>As 10 Categorias com Maiores Gastos em Frete</h2>", unsafe_allow_html=True)
    
    data = top_10_freight_value_by_category(engine)
    df = pd.DataFrame(data, columns=["Category", "Total Freight Value"])
    df["Total Freight Value"] = pd.to_numeric(df["Total Freight Value"], errors='coerce')
    st.bar_chart(df.set_index("Category")["Total Freight Value"])

# Consulta 55: valor total gasto com frete, para cada categoria de produto.
def show_total_freight_value_by_category(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Valor Total Gasto com Frete por Categoria</h2>", unsafe_allow_html=True)
    
    data = total_freight_value_by_category(engine)
    categories = [row[0] for row in data]
    
    category = st.selectbox("Selecione a categoria de produto", categories)
    
    if category:
        category_data = [row for row in data if row[0] == category]
        if category_data:
            st.write(f"Valor total gasto com frete para a categoria '{category}': R$ {category_data[0][1]:,.2f}")
        else:
            st.write(f"Nenhum gasto com frete encontrado para a categoria '{category}'.")

# Consulta 62: quantidade de vezes que produtos de uma categoria foram adquiridos em cada estado.
def show_sales_by_category_state(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Quantidade de Pedidos de Uma Categoria em Cada Estado</h2>", unsafe_allow_html=True)
    data = get_sales_by_category_state(engine)
    df = pd.DataFrame(data, columns=["product_category_name", "customer_state", "total_pedidos"])
    categories = df["product_category_name"].unique()
    category = st.selectbox("Selecione a categoria de produto", categories, key="category_selectbox")
    
    if category:
        category_data = df[df["product_category_name"] == category]
        st.bar_chart(category_data.set_index("customer_state")["total_pedidos"])