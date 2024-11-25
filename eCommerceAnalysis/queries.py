from sqlalchemy import create_engine, text

# Consulta: produtos mais bem avaliados.
def best_products(engine):
    state = state.upper()
    query = """
        SELECT Produto.product_category_name, avg(Review.review_score)
        FROM olist_products_dataset Produto
        JOIN olist_order_items_dataset USING (product_id)
        JOIN olist_orders_dataset USING (order_id)
        JOIN olist_order_reviews_dataset Review USING (order_id)
        GROUP BY Produto.product_category_name
        ORDER BY avg(Review.review_score) DESC
    """

    with engine.connect() as connection:
        result = connection.execute(text(query))

    for row in result:
        print(row)

# Consulta: produtos mais bem avaliados em uma região (all-time).
def best_products(engine, state):
    state = state.upper()
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

    for row in result:
        print(row)

# Consulta: categorias mais compradas em um ano/mês.
def get_top_categories(year, month):
    query = """
        SELECT Produto.product_category_name, COUNT(*) AS total_compras
        FROM olist_products_dataset Produto
        JOIN olist_order_items_dataset USING (product_id)
        JOIN olist_orders_dataset USING (order_id)
        WHERE EXTRACT(YEAR FROM order_purchase_timestamp) = :year
          AND EXTRACT(MONTH FROM order_purchase_timestamp) = :month
        GROUP BY Produto.product_category_name
        ORDER BY total_compras DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {"year": year, "month": month})
        return result.fetchall()

# Consulta: estado com maior poder aquisitivo por ano/mês (maior valor de compra por número de pedidos).
def get_top_state_by_purchasing_power(year, month):
    query = """
        SELECT Cliente.customer_state, 
               SUM(order_items_dataset.price + order_items_dataset.freight_value) / COUNT(DISTINCT order_id) AS avg_value
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = order_items_dataset.order_id
        WHERE EXTRACT(YEAR FROM order_purchase_timestamp) = :year
          AND EXTRACT(MONTH FROM order_purchase_timestamp) = :month
        GROUP BY Cliente.customer_state
        ORDER BY avg_value DESC
        LIMIT 1;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {"year": year, "month": month})
        return result.fetchone()

# Consulta: meses do ano com maior volume de compras.
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

# Consulta: valor médio de compras efetuadas por clientes de certa cidade.
def get_avg_purchase_by_city(city):
    query = """
        SELECT AVG(order_items_dataset.price + order_items_dataset.freight_value) AS avg_value
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = order_items_dataset.order_id
        WHERE Cliente.customer_city = :city;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {"city": city})
        return result.fetchone()

# Consulta: valor médio de compras efetuadas por clientes de certo estado.
def get_avg_purchase_by_state(state):
    query = """
        SELECT AVG(order_items_dataset.price + order_items_dataset.freight_value) AS avg_value
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = order_items_dataset.order_id
        WHERE Cliente.customer_state = :state;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {"state": state})
        return result.fetchone()

# Consulta: total de pedidos realizados por cidade.
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

# Consulta: total de pedidos realizados por estado.
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

# Consulta: total de vendas por categoria de produto.
def get_total_sales_by_category():
    query = """
        SELECT Produto.product_category_name, SUM(order_items_dataset.price + order_items_dataset.freight_value) AS total_vendas
        FROM olist_products_dataset Produto
        JOIN olist_order_items_dataset USING (product_id)
        JOIN olist_orders_dataset USING (order_id)
        GROUP BY Produto.product_category_name
        ORDER BY total_vendas DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta: média de avaliação dos produtos por categoria.
def get_avg_review_by_category():
    query = """
        SELECT Produto.product_category_name, AVG(Review.review_score) AS avg_review
        FROM olist_products_dataset Produto
        JOIN olist_order_items_dataset USING (product_id)
        JOIN olist_orders_dataset USING (order_id)
        JOIN olist_order_reviews_dataset Review USING (order_id)
        GROUP BY Produto.product_category_name
        ORDER BY avg_review DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta: número de pedidos por faixa de preço (baixo, médio, alto).
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

# Consulta: número de produtos vendidos por cidade.
def get_products_sold_by_city():
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

# Consulta: vendas totais por tipo de pagamento (cartão de crédito, boleto, etc.).
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

# Consulta: número de pedidos entregues com atraso (data de entrega estimada vs. data real).
def get_delayed_orders():
    query = """
        SELECT COUNT(*) AS total_atrasos
        FROM olist_orders_dataset
        WHERE order_delivered_customer_date > order_estimated_delivery_date;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchone()

# Consulta: vendas totais por vendedor.
def get_sales_by_seller():
    query = """
        SELECT seller_id, SUM(order_items_dataset.price + order_items_dataset.freight_value) AS total_vendas
        FROM olist_order_items_dataset
        JOIN olist_orders_dataset USING (order_id)
        GROUP BY seller_id
        ORDER BY total_vendas DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta: vendas totais por estado.
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

# Consulta: total de produtos comprados por cliente.
def get_total_products_by_customer():
    query = """
        SELECT Cliente.customer_id, COUNT(order_items_dataset.order_item_id) AS total_produtos
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = olist_order_items_dataset.order_id
        GROUP BY Cliente.customer_id
        ORDER BY total_produtos DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta: média de parcelas dos pagamentos.
def get_avg_payment_installments():
    query = """
        SELECT AVG(payment_installments) AS avg_parcelas
        FROM olist_order_payments_dataset;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchone()

# Consulta: número de pedidos por tipo de pagamento e estado.
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

# Consulta: média de avaliação dos vendedores por estado.
def get_avg_seller_reviews_by_state():
    query = """
        SELECT Cliente.customer_state, AVG(Review.review_score) AS avg_review_score
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_reviews_dataset Review USING (order_id)
        JOIN olist_order_items_dataset USING (order_id)
        JOIN olist_sellers_dataset Seller ON olist_order_items_dataset.seller_id = Seller.seller_id
        GROUP BY Cliente.customer_state
        ORDER BY avg_review_score DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta: produtos mais comprados por faixa de preço.
def get_top_products_by_price_range():
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

# Consulta: total de vendas por estado e cidade.
def get_total_sales_by_state_and_city():
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

# Consulta: média de tempo de entrega por estado.
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

# Consulta: número de pedidos por status (pendente, aprovado, cancelado, etc.).
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

# Consulta: vendas totais por cada tipo de frete.
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

# Consulta: produtos com mais comentários e avaliações.
def get_most_reviewed_products():
    query = """
        SELECT product_id, COUNT(DISTINCT review_id) AS total_reviews
        FROM olist_order_reviews_dataset
        JOIN olist_order_items_dataset USING (order_id)
        GROUP BY product_id
        ORDER BY total_reviews DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta: número de produtos vendidos por vendedor e estado.
def get_products_sold_by_seller_and_state():
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

# Consulta: top 10 cidades com mais vendas.
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

# Consulta: vendas por categoria de produto, ordenadas por maior faturamento.
def get_sales_by_product_category():
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
    
# Consulta: número de itens vendidos por vendedor.
def get_items_sold_by_seller():
    query = """
        SELECT olist_sellers_dataset.seller_id, COUNT(order_items_dataset.product_id) AS total_itens
        FROM olist_sellers_dataset
        JOIN order_items_dataset USING (seller_id)
        GROUP BY olist_sellers_dataset.seller_id
        ORDER BY total_itens DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta: comparação entre número de pedidos aprovados e pedidos cancelados por cidade.
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

# Consulta: top 10 produtos mais vendidos em termos de unidades.
def get_top_10_most_sold_products():
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

# Consulta: produtos com maior valor de frete.
def get_products_with_highest_freight_value():
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

# Consulta: média de preço dos produtos por categoria.
def get_avg_price_by_category():
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

# Consulta: número de pedidos entregues dentro do prazo, por cidade.
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

# Consulta: top 10 clientes com maior volume de compras.
def get_top_10_customers_by_sales_volume():
    query = """
        SELECT Cliente.customer_id, Cliente.customer_city, SUM(Item.price) AS total_compras
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset Pedido USING (customer_id)
        JOIN order_items_dataset Item USING (order_id)
        GROUP BY Cliente.customer_id, Cliente.customer_city
        ORDER BY total_compras DESC
        LIMIT 10;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta: média de tempo de entrega por cidade.
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

# Consulta: média de avaliação por produto e categoria.
def get_avg_review_by_product_and_category():
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

# Consulta: total de vendas por tipo de pagamento (dividido por cidade).
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

# Consulta: comparação entre vendas de produtos físicos e digitais.
def get_comparison_physical_vs_digital_products():
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

# Consulta: número de pedidos por intervalo de datas (diário, semanal, mensal).
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

# Consulta: vendas totais por período do ano (por exemplo, verão, inverno, datas promocionais).
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

# Consulta: top 5 categorias de produto mais compradas no último mês.
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

# Consulta: número de pedidos por estado e cidade, dividido por status do pedido.
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

# Consulta: total de vendas por tipo de produto (eletrônicos, roupas, etc.).
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

# Consulta: média de avaliações por cidade.
def get_avg_reviews_by_city():
    query = """
        SELECT Cliente.customer_city, AVG(Review.review_score) AS media_avaliacoes
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset Pedido USING (customer_id)
        JOIN olist_order_reviews_dataset Review USING (order_id)
        GROUP BY Cliente.customer_city
        ORDER BY media_avaliacoes DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta: total de vendas por categoria de produto e vendedor.
def get_total_sales_by_category_and_seller():
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

# Consulta: número de pedidos por status de pagamento.
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

# Consulta: categorias mais vendidas em um intervalo de datas.
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