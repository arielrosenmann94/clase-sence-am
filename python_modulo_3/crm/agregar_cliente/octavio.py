# Base de datos simulada
base_datos = []

# ID autoincremental
id_cliente = 1

while True:
    print("\n=== SISTEMA DE CLIENTES ===")
    print("1. Agregar cliente")
    print("2. Ver clientes")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    # SWITCH PRINCIPAL
    switch_menu = {
        "1": "agregar",
        "2": "mostrar",
        "3": "salir"
    }

    accion = switch_menu.get(opcion, "invalido")

    if accion == "agregar":
        print("\n--- NUEVO CLIENTE ---")

        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        telefono = input("Teléfono: ")
        correo = input("Correo: ")

        print("\nEstado del cliente:")
        print("1. Cliente potencial")
        print("2. Cliente con alto interés")
        print("3. En proceso de compra")
        print("4. Cliente efectivo")
        print("5. Super cliente")

        estado_opcion = input("Seleccione estado (1-5): ")

        # SWITCH DE ESTADOS
        switch_estado = {
            "1": "Cliente potencial",
            "2": "Cliente con alto interés",
            "3": "En proceso de compra",
            "4": "Cliente efectivo",
            "5": "Super cliente"
        }

        estado = switch_estado.get(estado_opcion, "Estado no válido")

        cliente = {
            "id": id_cliente,
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono,
            "correo": correo,
            "estado": estado
        }

        base_datos.append(cliente)
        print(f"\n✅ Cliente agregado con ID {id_cliente}")

        id_cliente += 1  # autoincremental

    elif accion == "mostrar":
        print("\n--- LISTADO DE CLIENTES ---")

        if len(base_datos) == 0:
            print("No hay clientes registrados.")
        else:
            for c in base_datos:
                print(
                    f"ID: {c['id']} | "
                    f"{c['nombre']} {c['apellido']} | "
                    f"Tel: {c['telefono']} | "
                    f"Correo: {c['correo']} | "
                    f"Estado: {c['estado']}"
                )

    elif accion == "salir":
        print("👋 Saliendo del sistema...")
        break

    else:
        print("❌ Opción inválida")