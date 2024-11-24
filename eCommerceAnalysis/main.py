from startDatabase import import_data
import consultas

def main():
    engine = import_data()

    print()
    estado = input("Insira estado (RS, RN, SP, etc): ")
    print()
    
    print(consultas.best_products(engine, estado))

main()