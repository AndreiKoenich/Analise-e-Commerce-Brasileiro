import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

DATABASE_URL = 'postgresql://postgres:123456@localhost/e_commerce'
DATABASE_NAME = 'e_commerce'

def create_tables(engine):
    create_table_queries = [
        """
        DROP TABLE IF EXISTS olist_customers_dataset;
        CREATE TABLE olist_customers_dataset (
            customer_id VARCHAR(255) PRIMARY KEY,
            customer_unique_id VARCHAR(255),
            customer_zip_code_prefix VARCHAR(5),
            customer_city VARCHAR(255),
            customer_state VARCHAR(2)
        );
        """,
        """
        DROP TABLE IF EXISTS olist_geolocation_dataset;
        CREATE TABLE olist_geolocation_dataset (
            geolocation_zip_code_prefix VARCHAR(5) PRIMARY KEY,
            geolocation_lat FLOAT,
            geolocation_lng FLOAT,
            geolocation_city VARCHAR(255),
            geolocation_state VARCHAR(2)
        );
        """,
        """
        DROP TABLE IF EXISTS olist_order_payments_dataset;
        CREATE TABLE olist_order_payments_dataset (
            order_id VARCHAR(255),
            payment_sequential INT,
            payment_type VARCHAR(50),
            payment_installments INT,
            payment_value FLOAT,
            PRIMARY KEY (order_id, payment_sequential)
        );
        """,
        """
        DROP TABLE IF EXISTS olist_order_reviews_dataset;
        CREATE TABLE olist_order_reviews_dataset (
            review_id VARCHAR(255) PRIMARY KEY,
            order_id VARCHAR(255),
            review_score INT,
            review_comment_title VARCHAR(255),
            review_comment_message TEXT,
            review_creation_date TIMESTAMP,
            review_answer_timestamp TIMESTAMP
        );
        """,
        """
        DROP TABLE IF EXISTS olist_orders_dataset;
        CREATE TABLE olist_orders_dataset (
            order_id VARCHAR(255) PRIMARY KEY,
            customer_id VARCHAR(255),
            order_status VARCHAR(50),
            order_purchase_timestamp TIMESTAMP,
            order_approved_at TIMESTAMP,
            order_delivered_carrier_date TIMESTAMP,
            order_delivered_customer_date TIMESTAMP,
            order_estimated_delivery_date TIMESTAMP
        );
        """,
        """
        DROP TABLE IF EXISTS olist_products_dataset;
        CREATE TABLE olist_products_dataset (
            product_id VARCHAR(255) PRIMARY KEY,
            product_category_name VARCHAR(255),
            product_name_length INT,
            product_description_length INT,
            product_photos_qty INT,
            product_weight_g INT,
            product_length_cm INT
        );
        """,
        """
        DROP TABLE IF EXISTS olist_sellers_dataset;
        CREATE TABLE olist_sellers_dataset (
            seller_id VARCHAR(50) PRIMARY KEY,
            seller_zip_code_prefix VARCHAR(10),
            seller_city VARCHAR(100),
            seller_state VARCHAR(2)
        );
        """,
        """
        DROP TABLE IF EXISTS product_category_name_translation;
        CREATE TABLE product_category_name_translation (
            product_category_name VARCHAR(255),
            product_category_name_english VARCHAR(255),
            PRIMARY KEY (product_category_name)
        );
        """
    ]

    for query in create_table_queries:
        engine.execute(query)
    print("Todas as nove tabelas foram criadas com sucesso!")

def import_csv_to_postgres(csv_file, table_name, engine):
    df = pd.read_csv(csv_file)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f'Dados inseridos com sucesso na tabela {table_name}')

def import_data():
    engine = create_engine(DATABASE_URL)
    if not database_exists(engine.url):
        create_database(engine.url)
    print(f"Banco de dados {DATABASE_NAME} criado com sucesso!")

    create_tables(engine)
    
    import_csv_to_postgres('olist_customers_dataset.csv', 'olist_customers_dataset', engine)
    import_csv_to_postgres('olist_geolocation_dataset.csv', 'olist_geolocation_dataset', engine)
    import_csv_to_postgres('olist_order_items_dataset.csv', 'olist_order_items_dataset', engine)
    import_csv_to_postgres('olist_order_payments_dataset.csv', 'olist_order_payments_dataset', engine)
    import_csv_to_postgres('olist_order_reviews_dataset.csv', 'olist_order_reviews_dataset', engine)
    import_csv_to_postgres('olist_orders_dataset.csv', 'olist_orders_dataset', engine)
    import_csv_to_postgres('olist_products_dataset.csv', 'olist_products_dataset', engine)
    import_csv_to_postgres('olist_sellers_dataset.csv', 'olist_sellers_dataset', engine)
    import_csv_to_postgres('product_category_name_translation.csv', 'product_category_name_translation', engine)