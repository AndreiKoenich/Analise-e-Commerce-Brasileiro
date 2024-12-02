import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
from productsQueries import *

def show_products_dashboard(engine):
    show_get_top_categories(engine)
    show_total_sales_by_category(engine)
    show_best_product_categories(engine)
    show_avg_review_by_category(engine)
    show_top_10_freight_value_categories(engine)
    show_total_freight_value_by_category(engine)

# Consulta 3: categorias mais compradas em um ano/mês.
def show_get_top_categories(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Categorias de Produtos Mais Compradas</h2>", unsafe_allow_html=True)

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

# Consulta 10: total de vendas por categoria de produto.
def show_total_sales_by_category(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Valor Total Obtido por Categoria de Produto</h2>", unsafe_allow_html=True)
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
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Top 10 Categorias de Produtos Melhor Avaliadas</h2>", unsafe_allow_html=True)
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
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Top 10 Categorias com Maior Gasto em Frete</h2>", unsafe_allow_html=True)
    
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