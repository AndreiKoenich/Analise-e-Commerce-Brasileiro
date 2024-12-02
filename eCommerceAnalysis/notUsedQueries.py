from sqlalchemy import create_engine, text

# Consulta 2: produtos mais bem avaliados em uma região (all-time).
def best_products_region(engine):
    query = """
        SELECT Produto.product_category_name, avg(Review.review_score)
        FROM olist_products_dataset Produto
        JOIN olist_order_items_dataset USING (product_id)
        JOIN olist_orders_dataset USING (order_id)
        JOIN olist_order_reviews_dataset Review USING (order_id)
        WHERE Cliente.customer_state = :state AND Produto.product_category_name IS NOT NULL
        GROUP BY Produto.product_category_name
        ORDER BY avg(Review.review_score) DESC
    """

    with engine.connect() as connection:
        result = connection.execute(text(query), {"state": state})
        return result.fetchall()

# Consulta 13: número de produtos vendidos por cidade.
def get_products_sold_by_city(engine):
    query = """
        SELECT Cliente.customer_city, SUM(order_items_dataset.order_item_id) AS total_produtos_vendidos
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = olist_order_items_dataset.order_id
        GROUP BY Cliente.customer_city
        ORDER BY total_produtos_vendidos DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 15: número de pedidos entregues com atraso (data de entrega estimada vs. data real) em um determinado ano.
def get_delayed_orders_by_year_and_month(engine, year, month):
    query = """
        SELECT COUNT(*) AS delayed_orders
        FROM olist_orders_dataset
        WHERE EXTRACT(YEAR FROM order_estimated_delivery_date::timestamp) = :year
            AND EXTRACT(YEAR FROM order_estimated_delivery_date::timestamp) = :month
        AND order_delivered_customer_date > order_estimated_delivery_date
    """
    
    with engine.connect() as connection:
        result = connection.execute(text(query), {"year": year, "month": month})
        delayed_orders = result.scalar() 
    
    return delayed_orders


# Consulta 19: média de parcelas dos pagamentos.
def get_avg_payment_installments(engine):
    query = """
        SELECT AVG(payment_installments) AS avg_parcelas
        FROM olist_order_payments_dataset;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchone()

# Consulta 22: produtos mais comprados por faixa de preço.
def get_top_products_by_price_range(engine):
    query = """
        SELECT CASE 
                   WHEN price < 50 THEN 'Baixo'
                   WHEN price BETWEEN 50 AND 200 THEN 'Médio'
                   ELSE 'Alto'
               END AS faixa_preco,
               product_id, COUNT(*) AS total_compras
        FROM olist_order_items_dataset
        GROUP BY faixa_preco, product_id
        ORDER BY faixa_preco, total_compras DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 23: total de vendas por estado e cidade.
def get_total_sales_by_state_and_city(engine):
    query = """
        SELECT Cliente.customer_state, Cliente.customer_city, SUM(order_items_dataset.price + order_items_dataset.freight_value) AS total_sales
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = order_items_dataset.order_id
        GROUP BY Cliente.customer_state, Cliente.customer_city
        ORDER BY total_sales DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 24: média de tempo de entrega por estado.
def get_avg_delivery_time_by_state(engine):
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

# Consulta 27: produtos com mais comentários e avaliações.
def get_most_reviewed_products(engine):
    query = """
        SELECT product_id, COUNT(DISTINCT review_id) AS total_reviews
        FROM olist_order_reviews_dataset
        JOIN olist_order_items_dataset USING (order_id)
        GROUP BY product_id
        ORDER BY total_reviews DESC
        LIMIT 10;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 28: número de produtos vendidos por vendedor e estado.
def get_products_sold_by_seller_and_state(engine):
    query = """
        SELECT Seller.seller_id, Seller.seller_state, COUNT(*) AS total_products
        FROM olist_order_items_dataset
        JOIN olist_sellers_dataset Seller USING (seller_id)
        GROUP BY Seller.seller_id, Seller.seller_state
        ORDER BY total_products DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 30: vendas por categoria de produto, ordenadas por maior faturamento.
def get_sales_by_product_category(engine):
    query = """
        SELECT olist_products_dataset.product_category_name, SUM(order_items_dataset.price) AS total_vendas
        FROM olist_products_dataset
        JOIN order_items_dataset USING (product_id)
        GROUP BY olist_products_dataset.product_category_name
        ORDER BY total_vendas DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 33: top 10 produtos mais vendidos em termos de unidades.
def get_top_10_most_sold_products(engine):
    query = """
        SELECT Produto.product_id, Produto.product_category_name, SUM(Item.order_item_id) AS total_unidades
        FROM olist_products_dataset Produto
        JOIN order_items_dataset Item USING (product_id)
        GROUP BY Produto.product_id, Produto.product_category_name
        ORDER BY total_unidades DESC
        LIMIT 10;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 34: produtos com maior valor de frete.
def get_products_with_highest_freight_value(engine):
    query = """
        SELECT Produto.product_id, Produto.product_category_name, MAX(Item.freight_value) AS max_frete
        FROM olist_products_dataset Produto
        JOIN order_items_dataset Item USING (product_id)
        GROUP BY Produto.product_id, Produto.product_category_name
        ORDER BY max_frete DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 35: média de preço dos produtos por categoria.
def get_avg_price_by_category(engine):
    query = """
        SELECT Produto.product_category_name, AVG(Item.price) AS media_preco
        FROM olist_products_dataset Produto
        JOIN order_items_dataset Item USING (product_id)
        GROUP BY Produto.product_category_name
        ORDER BY media_preco DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 38: média de tempo de entrega por cidade.
def get_avg_delivery_time_by_city(engine):
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

# Consulta 39: média de avaliação por produto e categoria.
def get_avg_review_by_product_and_category(engine):
    query = """
        SELECT Produto.product_id, Produto.product_category_name, AVG(Review.review_score) AS media_avaliacao
        FROM olist_products_dataset Produto
        JOIN order_items_dataset Item USING (product_id)
        JOIN olist_order_reviews_dataset Review USING (order_id)
        GROUP BY Produto.product_id, Produto.product_category_name
        ORDER BY media_avaliacao DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 40: total de vendas por tipo de pagamento (dividido por cidade).
def get_sales_by_payment_type_and_city(engine):
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

# Consulta 41: comparação entre vendas de produtos físicos e digitais.
def get_comparison_physical_vs_digital_products(engine):
    query = """
        SELECT Produto.product_category_name, COUNT(*) AS total_vendas
        FROM olist_products_dataset Produto
        JOIN order_items_dataset Item USING (product_id)
        WHERE Produto.product_category_name IN ('physical', 'digital')
        GROUP BY Produto.product_category_name
        ORDER BY total_vendas DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 43: vendas totais por período do ano (por exemplo, verão, inverno, datas promocionais).
def get_sales_by_season(engine):
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
def get_top_5_categories_last_month(engine):
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
def get_orders_by_state_city_and_status(engine):
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

# Consulta 48: total de vendas por categoria de produto e vendedor.
def get_total_sales_by_category_and_seller(engine):
    query = """
        SELECT Produto.product_category_name, Vendedor.seller_id, SUM(Item.price * Item.order_item_id) AS total_vendas
        FROM olist_products_dataset Produto
        JOIN olist_order_items_dataset Item USING (product_id)
        JOIN olist_sellers_dataset Vendedor USING (seller_id)
        GROUP BY Produto.product_category_name, Vendedor.seller_id
        ORDER BY total_vendas DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 49: número de pedidos por status de pagamento.
def get_number_of_orders_by_payment_status(engine):
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

# Consulta 50: categorias mais vendidas em um intervalo de datas.
def get_top_categories_by_sales_in_date_range(start_date, end_date):
    query = """
        SELECT Produto.product_category_name, SUM(Item.price * Item.order_item_id) AS total_vendas
        FROM olist_products_dataset Produto
        JOIN olist_order_items_dataset Item USING (product_id)
        JOIN olist_orders_dataset Pedido USING (order_id)
        WHERE Pedido.order_purchase_timestamp BETWEEN :start_date AND :end_date
        GROUP BY Produto.product_category_name
        ORDER BY total_vendas DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {'start_date': start_date, 'end_date': end_date})
        return result.fetchall()