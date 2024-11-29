from sqlalchemy import create_engine, text

# Consulta 1: produtos mais bem avaliados.
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

# Consulta 2: produtos mais bem avaliados em uma região (all-time).
def best_products_region(engine, state):
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

# Consulta 10: total de vendas por categoria de produto.
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

# Consulta 11: média de avaliação dos produtos por categoria.
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

# Consulta 13: número de produtos vendidos por cidade.
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

# Consulta 22: produtos mais comprados por faixa de preço.
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

# Consulta 23: total de vendas por estado e cidade.
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

# Consulta 27: produtos com mais comentários e avaliações.
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

# Consulta 33: top 10 produtos mais vendidos em termos de unidades.
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

# Consulta 34: produtos com maior valor de frete.
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

# Consulta 35: média de preço dos produtos por categoria.
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

# Consulta 39: média de avaliação por produto e categoria.
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

# Consulta 41: comparação entre vendas de produtos físicos e digitais.
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