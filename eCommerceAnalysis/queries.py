from sqlalchemy import create_engine, text

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
#TODO

# Consulta: estado com maior poder aquisitivo por ano/mês (maior valor de compra por número de pedidos).
#TODO

# Consulta: meses do ano com maior volume de compras.
#TODO

# Consulta: valor médio de compras efetuadas por clientes de certa cidade.
#TODO

# Análise: relatório completo de tendências mensais de um mês específico.
#TODO

# Visualização: Gráfico de tendências de uma categoria específica
#TODO