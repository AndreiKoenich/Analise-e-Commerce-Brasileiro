from sqlalchemy import create_engine, text

# Consulta: produtos mais bem avaliados em uma região (all-time).
def best_products(engine, state):
    state = state.upper()
    query = """
        SELECT Produto.product_category_name, avg(Review.review_score)
        FROM olist_products_dataset Produto
        JOIN olist_order_items_dataset USING (product_id)
        JOIN olist_orders_dataset USING (order_id)
        JOIN olist_customers_dataset Cliente USING (customer_id)
        JOIN olist_order_reviews_dataset Review USING (order_id)
        WHERE Cliente.customer_state = :state AND Produto.product_category_name IS NOT NULL
        GROUP BY Produto.product_category_name
        ORDER BY avg(Review.review_score) DESC
    """

    with engine.connect() as connection:
        result = connection.execute(text(query), {"state": state})

    for row in result:
        print(row)

# Consulta: categorias mais compradas em um ano/mês
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

# Análise: relatório completo de tendências mensais de um mês específico.
# Visualização: Gráfico de tendências de uma categoria específica
