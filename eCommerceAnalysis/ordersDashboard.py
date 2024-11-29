import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import text
from ordersQueries import *

# Consulta 3: categorias mais compradas em um ano/mês.
def show_get_top_categories(engine):
    st.markdown("<h2 style='text-align: center;'>Análise de Pedidos</h2>", unsafe_allow_html=True)

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

# Consulta 4: estado com maior poder aquisitivo por ano/mês (maior valor de compra por número de pedidos).
def show_top_state_by_purchasing_power(engine):
    st.markdown("<h2 style='text-align: center;'>Estado com Maior Poder Aquisitivo</h2>", unsafe_allow_html=True)

    # Seletores de ano e mês com keys únicos
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox(
            "Selecione o Ano", 
            [2016, 2017, 2018], 
            index=1, 
            key="select_year_top_state"
        )
    with col2:
        selected_month = st.selectbox(
            "Selecione o Mês", 
            list(range(1, 13)), 
            format_func=lambda x: f"{x:02d}", 
            key="select_month_top_state"
        )

    # Executa a consulta e obtém os resultados
    result = get_top_state_by_purchasing_power(engine, selected_year, selected_month)

    if result:
        state, avg_value = result
        avg_value = f"R${avg_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")  # Formato monetário brasileiro
        st.markdown(
            f"""
            <div style="text-align: center; padding: 20px; border: 1px solid # Ccc; border-radius: 10px; background-color: #f9f9f9;">
                <h3 style="color: #4CAF50;">{state}</h3>
                <p><strong>Valor Médio por Pedido:</strong> {avg_value}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown("<p style='text-align: center;'>Nenhum dado encontrado para o período selecionado.</p>", unsafe_allow_html=True)

def show_orders_dashboard(engine):
    show_get_top_categories(engine)
    show_top_state_by_purchasing_power(engine)

# Consulta 5: meses do ano com maior volume de compras.
# Consulta 8: total de pedidos realizados por cidade.
# Consulta 9: total de pedidos realizados por estado.
# Consulta 12: número de pedidos por faixa de preço (baixo, médio, alto).
# Consulta 14: vendas totais por tipo de pagamento (cartão de crédito, boleto, etc.).
# Consulta 15: número de pedidos entregues com atraso (data de entrega estimada vs. data real).
# Consulta 17: vendas totais por estado.
# Consulta 19: média de parcelas dos pagamentos.
# Consulta 20: número de pedidos por tipo de pagamento e estado.
# Consulta 24: média de tempo de entrega por estado.
# Consulta 25: número de pedidos por status (pendente, aprovado, cancelado, etc.).
# Consulta 26: vendas totais por cada tipo de frete.
# Consulta 29: top 10 cidades com mais vendas.
# Consulta 32: comparação entre número de pedidos aprovados e pedidos cancelados por cidade.
# Consulta 36: número de pedidos entregues dentro do prazo, por cidade.
# Consulta 38: média de tempo de entrega por cidade.
# Consulta 40: total de vendas por tipo de pagamento (dividido por cidade).
# Consulta 42: número de pedidos por intervalo de datas (diário, semanal, mensal).
# Consulta 43: vendas totais por período do ano (por exemplo, verão, inverno, datas promocionais).
# Consulta 44: top 5 categorias de produto mais compradas no último mês.
# Consulta 45: número de pedidos por estado e cidade, dividido por status do pedido.
# Consulta 46: total de vendas por tipo de produto (eletrônicos, roupas, etc.).
# Consulta 49: número de pedidos por status de pagamento.