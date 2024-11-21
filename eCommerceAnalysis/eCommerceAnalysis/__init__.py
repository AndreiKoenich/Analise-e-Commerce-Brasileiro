import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = 'postgresql://postgres:123456@localhost/e_commerce'
engine = create_engine(DATABASE_URL)

def import_csv_to_postgres(csv_file, table_name):
    df = pd.read_csv(csv_file)
    
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f'Dados inseridos com sucesso na tabela {table_name}')

def import_data():
    import_csv_to_postgres('olist_customers_dataset.csv', 'customers')
    import_csv_to_postgres('olist_geolocation_dataset.csv', 'geolocation')
    import_csv_to_postgres('olist_order_items_dataset.csv', 'order_items')
    import_csv_to_postgres('olist_order_payments_dataset.csv', 'order_payments')
    import_csv_to_postgres('olist_order_reviews_dataset.csv', 'order_reviews')
    import_csv_to_postgres('olist_orders_dataset.csv', 'orders')
    import_csv_to_postgres('olist_products_dataset.csv', 'products')
    import_csv_to_postgres('olist_sellers_dataset.csv', 'sellers')
    import_csv_to_postgres('product_category_name_translation.csv', 'translations')

def main():
    import_data()

main()