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

# Consulta 1: top 10 categorias de produtos melhor avaliadas.
def best_products(engine):
    query = """
        SELECT Produto.product_category_name, avg(Review.review_score)
        FROM olist_products_dataset Produto
        JOIN olist_order_items_dataset USING (product_id)
        JOIN olist_orders_dataset USING (order_id)
        JOIN olist_order_reviews_dataset Review USING (order_id)
        GROUP BY Produto.product_category_name
        ORDER BY avg(Review.review_score) DESC
        LIMIT 10;
    """

    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 10: total de vendas por categoria de produto.
def get_total_sales_by_category(engine):
    query = """
        SELECT Produto.product_category_name, SUM(olist_order_items_dataset.price + olist_order_items_dataset.freight_value) AS total_vendas
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
def get_avg_review_by_category(engine):
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

# Consulta 54: top 10 categorias com maior valor gasto com frete.
def top_10_freight_value_by_category(engine):
    query = """
        SELECT 
            p.product_category_name,
            SUM(i.freight_value) AS total_freight
        FROM 
            olist_order_items_dataset i
        JOIN 
            olist_products_dataset p
            ON i.product_id = p.product_id
        GROUP BY 
            p.product_category_name
        ORDER BY 
            total_freight DESC
        LIMIT 10;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 55: valor total gasto com frete, para cada categoria de produto.
def total_freight_value_by_category(engine):
    query = """
        SELECT 
            p.product_category_name,
            SUM(i.freight_value) AS total_freight
        FROM 
            olist_order_items_dataset i
        JOIN 
            olist_products_dataset p
            ON i.product_id = p.product_id
        GROUP BY 
            p.product_category_name
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 61: top 10 categorias mais adquiridas em um determinado estado.
def get_top_categories_by_state(engine, state_name):
    query = """
    SELECT Produto.product_category_name, COUNT(DISTINCT Orders.order_id) AS total_pedidos
    FROM olist_products_dataset Produto
    JOIN olist_order_items_dataset Item ON Produto.product_id = Item.product_id
    JOIN olist_orders_dataset Orders ON Item.order_id = Orders.order_id
    JOIN olist_customers_dataset Customer ON Orders.customer_id = Customer.customer_id
    WHERE Customer.customer_state = :state_name
    GROUP BY Produto.product_category_name
    ORDER BY total_pedidos DESC
    LIMIT 10;
    """
    
    with engine.connect() as connection:
        result = connection.execute(text(query), {"state_name": state_name})
        return result.fetchall()

# Consulta 62: quantidade de vezes que produtos de uma categoria foram adquiridos em cada estado.
def get_sales_by_category_state(engine):
    query = """
    SELECT Produto.product_category_name, Customer.customer_state, COUNT(DISTINCT Orders.order_id) AS total_pedidos
    FROM olist_products_dataset Produto
    JOIN olist_order_items_dataset Item ON Produto.product_id = Item.product_id
    JOIN olist_orders_dataset Orders ON Item.order_id = Orders.order_id
    JOIN olist_customers_dataset Customer ON Orders.customer_id = Customer.customer_id
    GROUP BY Produto.product_category_name, Customer.customer_state
    ORDER BY Produto.product_category_name, Customer.customer_state;
    """
    
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# Consulta 63: as dez categorias mais adquiridas.
def get_top_10_categories(engine):
    query = """
    SELECT Produto.product_category_name, COUNT(DISTINCT Orders.order_id) AS total_pedidos
    FROM olist_products_dataset Produto
    JOIN olist_order_items_dataset Item ON Produto.product_id = Item.product_id
    JOIN olist_orders_dataset Orders ON Item.order_id = Orders.order_id
    GROUP BY Produto.product_category_name
    ORDER BY total_pedidos DESC
    LIMIT 10;
    """
    
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()
    