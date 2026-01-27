from funciones import valor_compra

def main():
    tipo = input("Qué tipo de pán quieres llevar? (hallulla / marraqueta / amasado)")
    kg = int(input("Cuánto pesa? "))

    total = valor_compra(tipo, kg)

    if total is None:
        print("Tipo de pan no válido")
    else:
        print(f"Total por {kg}kg de {tipo}: ${total}")


if __name__ == "__main__":
    main()