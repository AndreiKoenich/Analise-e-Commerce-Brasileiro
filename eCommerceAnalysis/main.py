from startDatabase import import_data
from queries import best_products

def main():
    engine = import_data()
    best_products(engine, 'SP')

main()