clientes = []
id_cliente = 1

continuar = "si"

while continuar == "si":
    print("\n--- INGRESO DE NUEVO CLIENTE ---")

    nombre = input("Ingrese nombre: ")
    apellido = input("Ingrese apellido: ")
    telefono = input("Ingrese teléfono: ")
    correo = input("Ingrese correo: ")

    print("\nSeleccione estado del cliente:")
    print("1. Cliente potencial")
    print("2. Cliente con alto interés")
    print("3. En proceso de compra")
    print("4. Cliente efectivo")
    print("5. Super cliente")

    estado_opcion = int(input("Ingrese opción (1 a 5): "))

    if estado_opcion == 1:
        estado = "Cliente potencial"
    elif estado_opcion == 2:
        estado = "Cliente con alto interés"
    elif estado_opcion == 3:
        estado = "En proceso de compra"
    elif estado_opcion == 4:
        estado = "Cliente efectivo"
    elif estado_opcion == 5:
        estado = "Super cliente"
    else:
        estado = "Estado no válido"

    cliente = {
        "id": id_cliente,
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "correo": correo,
        "estado": estado
    }

    clientes.append(cliente)
    id_cliente = id_cliente + 1

    continuar = input("\n¿Desea ingresar otro cliente? (si/no): ")

print("\n--- BASE DE DATOS DE CLIENTES ---")
for c in clientes:
    print("ID:", c["id"])
    print("Nombre:", c["nombre"], c["apellido"])
    print("Teléfono:", c["telefono"])
    print("Correo:", c["correo"])
    print("Estado:", c["estado"])
    print("-----------------------------")