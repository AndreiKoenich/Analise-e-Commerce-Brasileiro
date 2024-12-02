from sqlalchemy import create_engine, text

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
def get_top_months_by_volume(engine, year):
    query = """
        SELECT EXTRACT(MONTH FROM order_purchase_timestamp::timestamp) AS month, 
               COUNT(*) AS total_compras
        FROM olist_orders_dataset
        WHERE EXTRACT(YEAR FROM order_purchase_timestamp::timestamp) = :year
        GROUP BY month
        ORDER BY total_compras DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {"year": year})
        return result.fetchall()

# Consulta 8: total de pedidos realizados por cidade.
def get_total_orders_by_city(engine):
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
def get_total_orders_by_state(engine):
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
def get_orders_by_price_range(engine, low_price, high_price):
    query = """
        SELECT
            CASE
                WHEN (price + freight_value) < :low_price THEN 'Baixo'
                WHEN (price + freight_value) BETWEEN :low_price AND :high_price THEN 'Médio'
                WHEN (price + freight_value) > :high_price THEN 'Alto'
            END AS faixa_preco,
            COUNT(DISTINCT olist_orders_dataset.order_id) AS total_pedidos
        FROM olist_order_items_dataset
        JOIN olist_orders_dataset USING (order_id)
        GROUP BY faixa_preco
        ORDER BY total_pedidos DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {"low_price": low_price, "high_price": high_price})
        return result.fetchall()

# Consulta 14: vendas totais por tipo de pagamento (cartão de crédito, boleto, etc.).
def get_sales_by_payment_type(engine):
    query = """
        SELECT payment_type, SUM(payment_value) AS total_vendas
        FROM olist_order_payments_dataset
        GROUP BY payment_type
        ORDER BY total_vendas DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 17: vendas totais por estado.
def get_sales_by_state(engine):
    query = """
        SELECT Cliente.customer_state, SUM(olist_order_items_dataset.price + olist_order_items_dataset.freight_value) AS total_vendas
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = olist_order_items_dataset.order_id
        GROUP BY Cliente.customer_state
        ORDER BY total_vendas DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 20: número de pedidos por tipo de pagamento.
def get_orders_by_payment_type_and_state(engine):
    query = """
        SELECT Cliente.customer_state, 
               olist_order_payments_dataset.payment_type, 
               COUNT(olist_orders_dataset.order_id) AS total_pedidos
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset ON Cliente.customer_id = olist_orders_dataset.customer_id
        JOIN olist_order_payments_dataset ON olist_orders_dataset.order_id = olist_order_payments_dataset.order_id
        GROUP BY Cliente.customer_state, olist_order_payments_dataset.payment_type
        ORDER BY Cliente.customer_state, total_pedidos DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()


# Consulta 25: número de pedidos por status (pendente, aprovado, cancelado, etc.).
def get_orders_by_status(engine):
    query = """
        SELECT olist_orders_dataset.order_status, COUNT(*) AS total_orders
        FROM olist_orders_dataset
        GROUP BY olist_orders_dataset.order_status
        ORDER BY total_orders DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 26: vendas totais por cada valor de frete.
def get_total_sales_by_freight_type(engine):
    query = """
        SELECT olist_order_items_dataset.freight_value, COUNT(*) AS total_orders
        FROM olist_order_items_dataset
        GROUP BY olist_order_items_dataset.freight_value
        ORDER BY total_orders DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 29: top 10 cidades com maiores valores em vendas.
def get_top_cities_by_sales(engine):
    query = """
        SELECT Cliente.customer_city, SUM(olist_order_items_dataset.price + olist_order_items_dataset.freight_value) AS total_sales
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = olist_order_items_dataset.order_id
        GROUP BY Cliente.customer_city
        ORDER BY total_sales DESC
        LIMIT 10;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 32: comparação entre número de pedidos aprovados e pedidos cancelados por cidade.
def get_order_status_comparison_for_city(engine, city):
    query = """
        SELECT SUM(CASE WHEN olist_orders_dataset.order_status IN ('delivered', 'shipped') THEN 1 ELSE 0 END) AS pedidos_aprovados,
               SUM(CASE WHEN olist_orders_dataset.order_status IN ('canceled', 'unavailable', 'invoiced') THEN 1 ELSE 0 END) AS pedidos_cancelados
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        WHERE Cliente.customer_city = :city
        GROUP BY Cliente.customer_city;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {"city": city})
        return result.fetchone()

# Consulta 36: número de pedidos entregues dentro do prazo, para uma cidade específica.
def get_on_time_orders_by_city(engine):
    query = """
        SELECT Cliente.customer_city, COUNT(*) AS pedidos_no_prazo
        FROM olist_orders_dataset Pedido
        JOIN olist_customers_dataset Cliente USING (customer_id)
        WHERE Pedido.order_delivered_customer_date <= Pedido.order_estimated_delivery_date
        GROUP BY Cliente.customer_city
        ORDER BY Cliente.customer_city;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 42: número de pedidos por intervalo de datas, entre duas datas específicas
def get_orders_by_date_range(engine, start_date, end_date):
    query = f"""
        SELECT DATE(Pedido.order_purchase_timestamp) AS periodo, COUNT(*) AS total_pedidos
        FROM olist_orders_dataset Pedido
        WHERE Pedido.order_purchase_timestamp::date BETWEEN :start_date AND :end_date
        GROUP BY periodo
        ORDER BY periodo;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {"start_date": start_date, "end_date": end_date})
        return result.fetchall()


# Consulta 46: total de vendas por tipo de produto (eletrônicos, roupas, etc.).
def get_total_sales_by_product_type(engine):
    query = """
        SELECT p.product_category_name AS categoria, COUNT(o.order_id) AS total_pedidos
        FROM olist_order_items_dataset oi
        JOIN olist_orders_dataset o ON oi.order_id = o.order_id
        JOIN olist_products_dataset p ON oi.product_id = p.product_id
        GROUP BY p.product_category_name
        ORDER BY total_pedidos DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()