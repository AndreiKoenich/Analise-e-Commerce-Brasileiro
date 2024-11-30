import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
from ordersQueries import *
from utils import estado_dict

def show_orders_dashboard(engine):
    show_get_top_categories(engine)
    show_top_state_by_purchasing_power(engine)
    show_top_months_by_volume(engine)
    show_total_orders_by_city(engine)
    show_on_time_orders_by_city(engine)
    show_total_orders_by_state(engine)
    show_orders_by_price_range(engine)
    show_sales_by_payment_type(engine)
    show_sales_by_state(engine)
    show_orders_by_payment_type(engine)
    show_orders_by_status(engine)
    show_total_sales_by_freight_type(engine)
    show_top_cities_by_sales(engine)
    show_order_status_comparison_by_city(engine)
    show_orders_by_date_range(engine)
    show_orders_by_category(engine)

# Consulta 3: categorias mais compradas em um ano/mês.
def show_get_top_categories(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Categorias Mais Compradas</h2>", unsafe_allow_html=True)

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
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Estado com Maior Valor de Compra por Número de Pedidos</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox(
            "Selecione o Ano", 
            [2017, 2018], 
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

    result = get_top_state_by_purchasing_power(engine, selected_year, selected_month)

    if result:
        state_sigla, avg_value = result
        state_full_name = estado_dict.get(state_sigla, state_sigla)  

        avg_value = f"R${avg_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.markdown(
            f"""
            <div style="text-align: center; padding: 20px; border: 1px solid # Ccc; border-radius: 10px; background-color: #f9f9f9;">
                <h3 style="color: #4CAF50;">{state_full_name}</h3>
                <p><strong>Valor Médio por Pedido:</strong> {avg_value}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown("<p style='text-align: center;'>Nenhum dado encontrado para o período selecionado.</p>", unsafe_allow_html=True)

# Consulta 5: meses do ano com maior volume de compras.
def show_top_months_by_volume(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Meses do Ano com Maior Volume de Compras</h2>", unsafe_allow_html=True)
    selected_year = st.selectbox("Selecione o ano", [2016, 2017, 2018])
    data = get_top_months_by_volume(engine, selected_year)
    df = pd.DataFrame(data, columns=["Month", "Volume"])
    
    month_names = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    
    df["Month"] = df["Month"].apply(lambda x: month_names[int(x) - 1] if isinstance(x, int) else str(x))
    df = df.set_index("Month")
    st.bar_chart(df["Volume"])

# Consulta 8: total de pedidos realizados por cidade.
def show_total_orders_by_city(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Total de Pedidos Realizados por Cidade</h2>", unsafe_allow_html=True)
    data = get_total_orders_by_city(engine)
    df = pd.DataFrame(data, columns=["City", "Total Orders"])
    selected_city = st.selectbox("Selecione a cidade", df["City"].unique())
    city_data = df[df["City"] == selected_city]
    total_orders = city_data["Total Orders"].values[0]
    st.markdown(f"O número total de pedidos realizados na cidade de {selected_city} é: **{total_orders}**")

# Consulta 9: total de pedidos realizados por estado.
def show_total_orders_by_state(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Total de Pedidos Realizados por Estado</h2>", unsafe_allow_html=True)
    data = get_total_orders_by_state(engine)
    df = pd.DataFrame(data, columns=["State", "Total Orders"])
    st.bar_chart(df.set_index("State")["Total Orders"])

# Consulta 12: número de pedidos por faixa de preço (baixo, médio, alto).
def show_orders_by_price_range(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Número de Pedidos por Faixa de Preço</h2>", unsafe_allow_html=True)
    low_price = st.number_input("Informe o valor para preços baixos", min_value=0, value=50)
    high_price = st.number_input("Informe o valor para preços altos", min_value=low_price, value=200)
    data = get_orders_by_price_range(engine, low_price, high_price)
    df = pd.DataFrame(data, columns=["Faixa de Preço", "Total de Pedidos"])
    st.table(df)

# Consulta 14: vendas totais por tipo de pagamento (cartão de crédito, boleto, etc.).
def show_sales_by_payment_type(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Valores Totais Pagos por Tipo de Pagamento</h2>", unsafe_allow_html=True)
    data = get_sales_by_payment_type(engine)
    df = pd.DataFrame(data, columns=["Tipo de Pagamento", "Total de Vendas"])
    st.bar_chart(df.set_index("Tipo de Pagamento")["Total de Vendas"])

# Consulta 17: vendas totais por estado.
def show_sales_by_state(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Valores Totais em Vendas por Estado</h2>", unsafe_allow_html=True)
    data = get_sales_by_state(engine)
    df = pd.DataFrame(data, columns=["Estado", "Total Vendas"])
    st.bar_chart(df.set_index("Estado")["Total Vendas"])

# Consulta 20: número de pedidos por tipo de pagamento.
def show_orders_by_payment_type(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Número de Pedidos por Tipo de Pagamento</h2>", unsafe_allow_html=True)
    data = get_orders_by_payment_type_and_state(engine)
    df = pd.DataFrame(data, columns=["Estado", "Tipo de Pagamento", "Total Pedidos"])
    df_grouped = df.groupby("Tipo de Pagamento")["Total Pedidos"].sum().reset_index()
    st.bar_chart(df_grouped.set_index("Tipo de Pagamento")["Total Pedidos"])

# Consulta 25: número de pedidos por status (pendente, aprovado, cancelado, etc.).
def show_orders_by_status(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Número de Pedidos por Status</h2>", unsafe_allow_html=True)
    data = get_orders_by_status(engine)
    df = pd.DataFrame(data, columns=["Order Status", "Total Orders"])
    st.bar_chart(df.set_index("Order Status")["Total Orders"])

# Consulta 26: vendas totais por cada valor de frete.
def show_total_sales_by_freight_type(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Vendas Totais por Cada Valor de Frete</h2>", unsafe_allow_html=True)
    data = get_total_sales_by_freight_type(engine)
    df = pd.DataFrame(data, columns=["Freight Type", "Total Orders"])
    st.bar_chart(df.set_index("Freight Type")["Total Orders"])

# Consulta 29: top 10 cidades com maiores valores em vendas.
def show_top_cities_by_sales(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Top 10 Cidades com Mais Valores em Vendas</h2>", unsafe_allow_html=True)
    data = get_top_cities_by_sales(engine)
    df = pd.DataFrame(data, columns=["City", "Total Sales"])
    st.bar_chart(df.set_index("City")["Total Sales"])

# Consulta 32: comparação entre número de pedidos aprovados e pedidos cancelados por cidade.
def show_order_status_comparison_by_city(engine):
    st.markdown("<h2 style='text-align: center; font-size: 24px;'>Comparação entre Pedidos Aprovados e Cancelados por Cidade</h2>", unsafe_allow_html=True)
    all_cities_query = """
        SELECT DISTINCT Cliente.customer_city
        FROM olist_customers_dataset Cliente
        ORDER BY Cliente.customer_city;
    """
    with engine.connect() as connection:
        all_cities = connection.execute(text(all_cities_query)).fetchall()
    cities = [row[0] for row in all_cities]

    selected_city = st.selectbox("Selecione uma cidade:", cities)
    
    if selected_city:
        data = get_order_status_comparison_for_city(engine, selected_city)
        if data:
            chart_data = pd.DataFrame({
                "Status": ["Aprovados", "Não Aprovados"],
                "Total": [data[0], data[1]]
            })
            st.bar_chart(chart_data.set_index("Status")["Total"])
        else:
            st.write("Nenhum dado encontrado para a cidade selecionada.")

# Consulta 36: número de pedidos entregues dentro do prazo, para uma cidade específica.
def show_on_time_orders_by_city(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Número de Pedidos Entregues Dentro do Prazo por Cidade</h2>", unsafe_allow_html=True)
    data = get_on_time_orders_by_city(engine)
    df = pd.DataFrame(data, columns=["City", "On Time Orders"])
    selected_city = st.selectbox("Selecione a cidade", df["City"].unique(), key="select_city_on_time_orders")
    city_data = df[df["City"] == selected_city]
    on_time_orders = city_data["On Time Orders"].values[0]
    st.markdown(f"O número de pedidos entregues dentro do prazo na cidade de {selected_city} é: **{on_time_orders}**")

# Consulta 42: número de pedidos por intervalo de datas (diário, semanal, mensal).
def show_orders_by_date_range(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Número de Pedidos por Intervalo de Datas</h2>", unsafe_allow_html=True)

    min_date = datetime.date(2016, 1, 1)
    max_date = datetime.date(2018, 12, 31)
    
    start_date = st.date_input("Selecione a data inicial", min_value=min_date, max_value=max_date)
    end_date = st.date_input("Selecione a data final", min_value=min_date, max_value=max_date)

    if start_date and end_date:
        if start_date > end_date:
            st.error("A data inicial não pode ser posterior à data final.")
        else:
            data = get_orders_by_date_range(engine, start_date, end_date)
            total_orders = sum(order[1] for order in data)  # Somando os pedidos no intervalo selecionado
            st.write(f"Número total de pedidos entre {start_date} e {end_date}: {total_orders}")

# Consulta 46: total de vendas por tipo de produto (eletrônicos, roupas, etc.).
def show_orders_by_category(engine):
    st.markdown("<h2 style='text-align: center; font-size: 26px;'>Número de Pedidos por Categoria</h2>", unsafe_allow_html=True)
    
    data = get_total_sales_by_product_type(engine)
    categories = [row[0] for row in data]
    
    category = st.selectbox("Selecione a categoria de produto", categories)
    
    if category:
        category_data = [row for row in data if row[0] == category]
        if category_data:
            st.write(f"Número total de pedidos para a categoria '{category}': {category_data[0][1]}")
        else:
            st.write(f"Nenhum pedido encontrado para a categoria '{category}'.")

# Consulta 15: número de pedidos entregues com atraso (data de entrega estimada vs. data real) em um determinado ano.
# Consulta 19: média de parcelas dos pagamentos.
# Consulta 24: média de tempo de entrega por estado.
# Consulta 38: média de tempo de entrega por cidade.
# Consulta 40: total de vendas por tipo de pagamento (dividido por cidade).
# Consulta 44: top 5 categorias de produto mais compradas no último mês.
# Consulta 49: número de pedidos por status de pagamento.
# Consulta 43: vendas totais por período do ano (por exemplo, verão, inverno, datas promocionais).
# Consulta 45: número de pedidos por estado e cidade, dividido por status do pedido.