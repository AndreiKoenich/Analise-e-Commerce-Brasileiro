from sqlalchemy import create_engine, text

# Consulta 16: valor total em vendas por vendedor.
def get_sales_by_seller(engine):
    query = """
        SELECT seller_id, SUM(olist_order_items_dataset.price + olist_order_items_dataset.freight_value) AS total_vendas
        FROM olist_order_items_dataset
        JOIN olist_orders_dataset USING (order_id)
        GROUP BY seller_id
        ORDER BY total_vendas DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 21: média de avaliação dos vendedores por estado.
def get_avg_seller_reviews_by_state(engine):
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

# Consulta 31: número de itens vendidos por vendedor.
def get_items_sold_by_seller(engine):
    query = """
        SELECT olist_sellers_dataset.seller_id, COUNT(olist_order_items_dataset.product_id) AS total_itens
        FROM olist_sellers_dataset
        JOIN olist_order_items_dataset USING (seller_id)
        GROUP BY olist_sellers_dataset.seller_id
        ORDER BY total_itens DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 52: quantidade total de vendedores por estado.
def get_total_sellers_by_state(engine):
    query = """
        SELECT Seller.seller_state, COUNT(Seller.seller_id) AS seller_count
        FROM olist_sellers_dataset Seller
        GROUP BY Seller.seller_state
        ORDER BY seller_count DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 58: número de vendedores por cidade.
def get_sellers_count_by_city(engine):
    query = """
        SELECT Seller.seller_city, COUNT(Seller.seller_id) AS seller_count
        FROM olist_sellers_dataset Seller
        GROUP BY Seller.seller_city
        ORDER BY seller_count DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 59: top 10 cidades com maior quantidade de vendedores.
def get_top_10_cities_by_sellers(engine):
    query = """
        SELECT Seller.seller_city, COUNT(Seller.seller_id) AS seller_count
        FROM olist_sellers_dataset Seller
        GROUP BY Seller.seller_city
        ORDER BY seller_count DESC
        LIMIT 10;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 60: quantidade de vendedores por categoria de produto.
def get_sellers_count_by_category(engine):
    query = """
        SELECT Produto.product_category_name, COUNT(DISTINCT Seller.seller_id) AS seller_count
        FROM olist_products_dataset Produto
        JOIN olist_order_items_dataset oi ON oi.product_id = Produto.product_id
        JOIN olist_sellers_dataset Seller ON oi.seller_id = Seller.seller_id
        GROUP BY Produto.product_category_name
        ORDER BY seller_count DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

