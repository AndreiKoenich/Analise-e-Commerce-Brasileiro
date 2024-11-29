from sqlalchemy import create_engine, text

# Consulta 3: categorias mais compradas em um ano/mês.
def get_top_categories(engine, year, month):
    query = """
        SELECT Produto.product_category_name, COUNT(*) AS total_compras
        FROM olist_products_dataset Produto
        JOIN olist_order_items_dataset USING (product_id)
        JOIN olist_orders_dataset USING (order_id)
        WHERE EXTRACT(YEAR FROM order_purchase_timestamp::timestamp) = :year
        AND EXTRACT(MONTH FROM order_purchase_timestamp::timestamp) = :month
        GROUP BY Produto.product_category_name
        ORDER BY total_compras DESC
        LIMIT 10;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {"year": year, "month": month})
        return result.fetchall()

# Consulta 4: estado com maior poder aquisitivo por ano/mês (maior valor de compra por número de pedidos).
def get_top_state_by_purchasing_power(engine, year, month):
    query = """
        SELECT Cliente.customer_state, 
               SUM(olist_order_items_dataset.price + olist_order_items_dataset.freight_value) / COUNT(DISTINCT olist_orders_dataset.order_id) AS avg_value
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset ON Cliente.customer_id = olist_orders_dataset.customer_id
        JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = olist_order_items_dataset.order_id
        WHERE EXTRACT(YEAR FROM olist_orders_dataset.order_purchase_timestamp::timestamp) = :year
          AND EXTRACT(MONTH FROM olist_orders_dataset.order_purchase_timestamp::timestamp) = :month
        GROUP BY Cliente.customer_state
        ORDER BY avg_value DESC
        LIMIT 1;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {"year": year, "month": month})
        return result.fetchone()

# Consulta 5: meses do ano com maior volume de compras.
def get_top_months_by_volume(year):
    query = """
        SELECT EXTRACT(MONTH FROM order_purchase_timestamp) AS month, COUNT(*) AS total_compras
        FROM olist_orders_dataset
        WHERE EXTRACT(YEAR FROM order_purchase_timestamp) = :year
        GROUP BY month
        ORDER BY total_compras DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {"year": year})
        return result.fetchall()

# Consulta 8: total de pedidos realizados por cidade.
def get_total_orders_by_city():
    query = """
        SELECT Cliente.customer_city, COUNT(DISTINCT olist_orders_dataset.order_id) AS total_pedidos
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        GROUP BY Cliente.customer_city
        ORDER BY total_pedidos DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 9: total de pedidos realizados por estado.
def get_total_orders_by_state():
    query = """
        SELECT Cliente.customer_state, COUNT(DISTINCT olist_orders_dataset.order_id) AS total_pedidos
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        GROUP BY Cliente.customer_state
        ORDER BY total_pedidos DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 12: número de pedidos por faixa de preço (baixo, médio, alto).
def get_orders_by_price_range():
    query = """
        SELECT
            CASE
                WHEN (price + freight_value) < 50 THEN 'Baixo'
                WHEN (price + freight_value) BETWEEN 50 AND 200 THEN 'Médio'
                WHEN (price + freight_value) > 200 THEN 'Alto'
            END AS faixa_preco,
            COUNT(DISTINCT olist_orders_dataset.order_id) AS total_pedidos
        FROM olist_order_items_dataset
        JOIN olist_orders_dataset USING (order_id)
        GROUP BY faixa_preco
        ORDER BY total_pedidos DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 14: vendas totais por tipo de pagamento (cartão de crédito, boleto, etc.).
def get_sales_by_payment_type():
    query = """
        SELECT payment_type, SUM(payment_value) AS total_vendas
        FROM olist_order_payments_dataset
        GROUP BY payment_type
        ORDER BY total_vendas DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 15: número de pedidos entregues com atraso (data de entrega estimada vs. data real).
def get_delayed_orders():
    query = """
        SELECT COUNT(*) AS total_atrasos
        FROM olist_orders_dataset
        WHERE order_delivered_customer_date > order_estimated_delivery_date;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchone()

# Consulta 17: vendas totais por estado.
def get_sales_by_state():
    query = """
        SELECT Cliente.customer_state, SUM(order_items_dataset.price + order_items_dataset.freight_value) AS total_vendas
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = olist_order_items_dataset.order_id
        GROUP BY Cliente.customer_state
        ORDER BY total_vendas DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 19: média de parcelas dos pagamentos.
def get_avg_payment_installments():
    query = """
        SELECT AVG(payment_installments) AS avg_parcelas
        FROM olist_order_payments_dataset;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchone()

# Consulta 20: número de pedidos por tipo de pagamento e estado.
def get_orders_by_payment_type_and_state():
    query = """
        SELECT Cliente.customer_state, olist_order_payments_dataset.payment_type, COUNT(DISTINCT olist_orders_dataset.order_id) AS total_pedidos
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_payments_dataset USING (order_id)
        GROUP BY Cliente.customer_state, olist_order_payments_dataset.payment_type
        ORDER BY Cliente.customer_state, total_pedidos DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 24: média de tempo de entrega por estado.
def get_avg_delivery_time_by_state():
    query = """
        SELECT Cliente.customer_state, AVG(olist_orders_dataset.order_delivered_customer_date - olist_orders_dataset.order_purchase_timestamp) AS avg_delivery_time
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        WHERE olist_orders_dataset.order_delivered_customer_date IS NOT NULL
        GROUP BY Cliente.customer_state
        ORDER BY avg_delivery_time;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 25: número de pedidos por status (pendente, aprovado, cancelado, etc.).
def get_orders_by_status():
    query = """
        SELECT olist_orders_dataset.order_status, COUNT(*) AS total_orders
        FROM olist_orders_dataset
        GROUP BY olist_orders_dataset.order_status
        ORDER BY total_orders DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 26: vendas totais por cada tipo de frete.
def get_total_sales_by_freight_type():
    query = """
        SELECT olist_order_items_dataset.freight_value, COUNT(*) AS total_orders
        FROM olist_order_items_dataset
        GROUP BY olist_order_items_dataset.freight_value
        ORDER BY total_orders DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 29: top 10 cidades com mais vendas.
def get_top_cities_by_sales():
    query = """
        SELECT Cliente.customer_city, SUM(order_items_dataset.price + order_items_dataset.freight_value) AS total_sales
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = order_items_dataset.order_id
        GROUP BY Cliente.customer_city
        ORDER BY total_sales DESC
        LIMIT 10;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 32: comparação entre número de pedidos aprovados e pedidos cancelados por cidade.
def get_order_status_comparison_by_city():
    query = """
        SELECT Cliente.customer_city,
               SUM(CASE WHEN olist_orders_dataset.order_status = 'approved' THEN 1 ELSE 0 END) AS pedidos_aprovados,
               SUM(CASE WHEN olist_orders_dataset.order_status = 'canceled' THEN 1 ELSE 0 END) AS pedidos_cancelados
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        GROUP BY Cliente.customer_city
        ORDER BY pedidos_aprovados DESC, pedidos_cancelados DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 36: número de pedidos entregues dentro do prazo, por cidade.
def get_on_time_orders_by_city():
    query = """
        SELECT Cliente.customer_city, COUNT(*) AS pedidos_no_prazo
        FROM olist_orders_dataset Pedido
        JOIN olist_customers_dataset Cliente USING (customer_id)
        WHERE Pedido.order_delivered_customer_date <= Pedido.order_estimated_delivery_date
        GROUP BY Cliente.customer_city
        ORDER BY pedidos_no_prazo DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 38: média de tempo de entrega por cidade.
def get_avg_delivery_time_by_city():
    query = """
        SELECT Cliente.customer_city, AVG(DATE_PART('day', Pedido.order_delivered_customer_date - Pedido.order_purchase_timestamp)) AS media_tempo_entrega
        FROM olist_orders_dataset Pedido
        JOIN olist_customers_dataset Cliente USING (customer_id)
        WHERE Pedido.order_delivered_customer_date IS NOT NULL
        GROUP BY Cliente.customer_city
        ORDER BY media_tempo_entrega;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 40: total de vendas por tipo de pagamento (dividido por cidade).
def get_sales_by_payment_type_and_city():
    query = """
        SELECT Cliente.customer_city, Pagamento.payment_type, SUM(Pagamento.payment_value) AS total_vendas
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset Pedido USING (customer_id)
        JOIN olist_order_payments_dataset Pagamento USING (order_id)
        GROUP BY Cliente.customer_city, Pagamento.payment_type
        ORDER BY total_vendas DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 42: número de pedidos por intervalo de datas (diário, semanal, mensal).
def get_orders_by_date_range(interval):
    query = f"""
        SELECT DATE_TRUNC('{interval}', Pedido.order_purchase_timestamp) AS periodo, COUNT(*) AS total_pedidos
        FROM olist_orders_dataset Pedido
        GROUP BY periodo
        ORDER BY periodo;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 43: vendas totais por período do ano (por exemplo, verão, inverno, datas promocionais).
def get_sales_by_season():
    query = """
        SELECT EXTRACT(MONTH FROM Pedido.order_purchase_timestamp) AS mes, SUM(Item.price) AS total_vendas
        FROM olist_orders_dataset Pedido
        JOIN order_items_dataset Item USING (order_id)
        GROUP BY mes
        ORDER BY mes;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 44: top 5 categorias de produto mais compradas no último mês.
def get_top_5_categories_last_month():
    query = """
        SELECT Produto.product_category_name, COUNT(Item.product_id) AS total_compras
        FROM olist_products_dataset Produto
        JOIN order_items_dataset Item USING (product_id)
        WHERE Pedido.order_purchase_timestamp >= NOW() - INTERVAL '1 month'
        GROUP BY Produto.product_category_name
        ORDER BY total_compras DESC
        LIMIT 5;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 45: número de pedidos por estado e cidade, dividido por status do pedido.
def get_orders_by_state_city_and_status():
    query = """
        SELECT Cliente.customer_state, Cliente.customer_city, Pedido.order_status, COUNT(*) AS total_pedidos
        FROM olist_orders_dataset Pedido
        JOIN olist_customers_dataset Cliente USING (customer_id)
        GROUP BY Cliente.customer_state, Cliente.customer_city, Pedido.order_status
        ORDER BY Cliente.customer_state, Cliente.customer_city, total_pedidos DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 46: total de vendas por tipo de produto (eletrônicos, roupas, etc.).
def get_total_sales_by_product_type():
    query = """
        SELECT Produto.product_category_name, SUM(Item.price * Item.order_item_id) AS total_vendas
        FROM olist_products_dataset Produto
        JOIN olist_order_items_dataset Item USING (product_id)
        GROUP BY Produto.product_category_name
        ORDER BY total_vendas DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 49: número de pedidos por status de pagamento.
def get_number_of_orders_by_payment_status():
    query = """
        SELECT Payment.payment_type, COUNT(Pedido.order_id) AS num_pedidos
        FROM olist_order_payments_dataset Payment
        JOIN olist_orders_dataset Pedido USING (order_id)
        GROUP BY Payment.payment_type
        ORDER BY num_pedidos DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()