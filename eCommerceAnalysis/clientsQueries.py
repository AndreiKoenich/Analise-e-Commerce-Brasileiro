from sqlalchemy import create_engine, text

# Consulta 6: valor médio de compras efetuadas por clientes de todas as cidades.
def get_avg_purchase_all_cities(engine):
    query = """
        SELECT Cliente.customer_city AS cidade, 
               AVG(olist_order_items_dataset.price + olist_order_items_dataset.freight_value) AS avg_value
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = olist_order_items_dataset.order_id
        GROUP BY Cliente.customer_city
        ORDER BY Cliente.customer_city;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 7: valor médio das compras realizadas por estado.
def get_avg_purchase_by_state(engine):
    query = """
        SELECT Cliente.customer_state AS estado, 
               AVG(olist_order_items_dataset.price + olist_order_items_dataset.freight_value) AS avg_value
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = olist_order_items_dataset.order_id
        GROUP BY Cliente.customer_state
        ORDER BY avg_value DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()
    
# Consulta 18: total de produtos comprados por cliente.
def get_total_products_by_customer(engine):
    query = """
        SELECT Cliente.customer_id, COUNT(olist_order_items_dataset.order_item_id) AS total_produtos
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset USING (customer_id)
        JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = olist_order_items_dataset.order_id
        GROUP BY Cliente.customer_id
        ORDER BY total_produtos DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 37: top 10 clientes com maior volume de compras.
def get_top_10_customers_by_sales_volume(engine):
    query = """
        SELECT Cliente.customer_id, Cliente.customer_city, SUM(Item.price) AS total_compras
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset Pedido USING (customer_id)
        JOIN olist_order_items_dataset Item USING (order_id)
        GROUP BY Cliente.customer_id, Cliente.customer_city
        ORDER BY total_compras DESC
        LIMIT 10;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 47: média de avaliações dos clientes por cidade.
def get_avg_reviews_by_city(engine):
    query = """
        SELECT Cliente.customer_city, AVG(Review.review_score) AS media_avaliacoes
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset Pedido USING (customer_id)
        JOIN olist_order_reviews_dataset Review USING (order_id)
        GROUP BY Cliente.customer_city
        ORDER BY Cliente.customer_city;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 51: média de avaliações dos clientes por estado.
def get_avg_reviews_by_state(engine):
    query = """
        SELECT Cliente.customer_state AS estado, AVG(Review.review_score) AS media_avaliacoes
        FROM olist_customers_dataset Cliente
        JOIN olist_orders_dataset Pedido USING (customer_id)
        JOIN olist_order_reviews_dataset Review USING (order_id)
        GROUP BY Cliente.customer_state
        ORDER BY media_avaliacoes DESC;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()