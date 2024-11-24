from execute_query import execute_sql
import pandas as pd

# Consulta: produtos mais bem avaliados em uma região (all-time).

# (região == estado)

# (ok aparentemente produtos não tem nome então tem que ser mudado pra categorias? ou a gente mostra o product id mesmo...?)

def best_products(engine, estado):
    estado = estado.upper() # "rn" = "RN"
    
    query = """
        SELECT Produto.product_category_name, avg(Review.review_score)

        FROM olist_products_dataset Produto 
        JOIN olist_order_items_dataset USING (product_id)
        JOIN olist_orders_dataset USING (order_id)
        JOIN olist_customers_dataset Cliente USING (customer_id)
        JOIN olist_order_reviews_dataset Review USING (order_id)

        WHERE Cliente.customer_state = :estado AND Produto.product_category_name IS NOT NULL

        GROUP BY Produto.product_category_name

        ORDER BY avg(Review.review_score) DESC
        """

    result = execute_sql(engine, query, {'estado': estado})

    return pd.DataFrame.from_records(result)

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