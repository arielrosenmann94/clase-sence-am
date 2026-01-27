client_database = []

# Estados posibles
estados = {
    1: "Cliente potencial",
    2: "Cliente con alto interés",
    3: "En proceso de compra",
    4: "Cliente efectivo",
    5: "Super cliente"
}

contador = 1
confirmation = "s"

while confirmation.lower() == "s":

    client = {}

    client["id"] = contador
    client["nombre"] = input("Ingrese el nombre del cliente:\n")
    client["apellido"] = input("Ingrese el apellido del cliente:\n")
    
    client["telefono"] = input("Ingrese el teléfono:\n")
    while not client["telefono"].isdigit() or not len(client["telefono"]) == 11 or not client["telefono"].startswith("569"): 
            client["telefono"] = input("Formato inválido. Por favor ingrese únicamente números incluyendo el 569: \n")
    client["correo"] = input("Ingrese el correo del cliente:\n")

    # Mostrar estados
    print("Cuál es el estado del cliente?")
    print("1 → Cliente potencial")
    print("2 → Cliente con alto interés")
    print("3 → En proceso de compra")
    print("4 → Cliente efectivo")
    print("5 → Super cliente")

    option_text = input("Ingrese una opción (1-5): ")

    if option_text.isdigit():
        option = int(option_text)
        if option >= 1 and option <= 5:
            client["estado"] = estados[option]
        else:
            client["estado"] = "Estado inválido"
    else:
        client["estado"] = "Estado inválido"

    client_database.append(client)

    contador += 1

    confirmation = input("¿Desea agregar otro cliente? (s/n): ")

# Mostrar clientes registrados
print("\nClientes registrados:")
for cliente in client_database:
    print(cliente)