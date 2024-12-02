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

# Consulta 52: os dez estados com o maior número de vendedores.
def get_top_seller_states(engine):
    query = """
        SELECT Seller.seller_state, COUNT(Seller.seller_id) AS seller_count
        FROM olist_sellers_dataset Seller
        GROUP BY Seller.seller_state
        ORDER BY seller_count DESC
        LIMIT 10;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 53: valor total obtido pelos vendedores por categoria.
def get_total_sales_by_category(engine):
    query = """
        SELECT p.product_category_name AS category_name,
               SUM(oi.price + oi.freight_value) AS total_sales
        FROM olist_order_items_dataset oi
        JOIN olist_products_dataset p ON oi.product_id = p.product_id
        GROUP BY p.product_category_name
        ORDER BY total_sales DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()
