clients = [
    {"id": 1, "nombre_completo": "Ana Torres", "correo": "ana.torres@correo.com", "telefono": "+56 9 42351234", "estado": "Cliente potencial"},
    {"id": 2, "nombre_completo": "Luis Ramírez", "correo": "luis.ramirez@correo.com", "telefono": "+56 9 93481234", "estado": "Alto interés"},
    {"id": 3, "nombre_completo": "Claudia Soto", "correo": "claudia.soto@correo.com", "telefono": "+56 9 78123456", "estado": "Cliente efectivo"},
    {"id": 4, "nombre_completo": "Jorge Fuentes", "correo": "jorge.fuentes@correo.com", "telefono": "+56 9 63547812", "estado": "En proceso de compra"},
    {"id": 5, "nombre_completo": "Marta Herrera", "correo": "marta.herrera@correo.com", "telefono": "+56 9 98124578", "estado": "Super cliente"},
    {"id": 6, "nombre_completo": "Carlos Díaz", "correo": "carlos.diaz@correo.com", "telefono": "+56 9 71234598", "estado": "Alto interés"},
    {"id": 7, "nombre_completo": "Francisca Rojas", "correo": "francisca.rojas@correo.com", "telefono": "+56 9 91234871", "estado": "Cliente efectivo"},
    {"id": 8, "nombre_completo": "Pedro Gutiérrez", "correo": "pedro.gutierrez@correo.com", "telefono": "+56 9 84567213", "estado": "Cliente potencial"},
    {"id": 9, "nombre_completo": "Valentina Bravo", "correo": "valentina.bravo@correo.com", "telefono": "+56 9 78341236", "estado": "Super cliente"},
    {"id": 10, "nombre_completo": "Diego Castro", "correo": "diego.castro@correo.com", "telefono": "+56 9 93456781", "estado": "En proceso de compra"},
    {"id": 11, "nombre_completo": "Camila Paredes", "correo": "camila.paredes@correo.com", "telefono": "+56 9 91234578", "estado": "Cliente potencial"},
    {"id": 12, "nombre_completo": "Andrés Molina", "correo": "andres.molina@correo.com", "telefono": "+56 9 89451236", "estado": "Cliente efectivo"},
    {"id": 13, "nombre_completo": "Patricia Silva", "correo": "patricia.silva@correo.com", "telefono": "+56 9 74382910", "estado": "Alto interés"},
    {"id": 14, "nombre_completo": "Matías Reyes", "correo": "matias.reyes@correo.com", "telefono": "+56 9 87234561", "estado": "En proceso de compra"},
    {"id": 15, "nombre_completo": "Isidora Méndez", "correo": "isidora.mendez@correo.com", "telefono": "+56 9 98127345", "estado": "Super cliente"},
    {"id": 16, "nombre_completo": "Sebastián Núñez", "correo": "sebastian.nunez@correo.com", "telefono": "+56 9 65432178", "estado": "Cliente efectivo"},
    {"id": 17, "nombre_completo": "Fernanda Loyola", "correo": "fernanda.loyola@correo.com", "telefono": "+56 9 72345681", "estado": "Alto interés"},
    {"id": 18, "nombre_completo": "Tomás Aravena", "correo": "tomas.aravena@correo.com", "telefono": "+56 9 83451234", "estado": "Cliente potencial"},
    {"id": 19, "nombre_completo": "Josefa Espinoza", "correo": "josefa.espinoza@correo.com", "telefono": "+56 9 96432187", "estado": "Cliente efectivo"},
    {"id": 20, "nombre_completo": "Ricardo Vergara", "correo": "ricardo.vergara@correo.com", "telefono": "+56 9 78912345", "estado": "Super cliente"}
]



while True:
    print("\n1. Ver clientes")
    print("2. Editar cliente")
    print("3. Salir")

    opcion = input("Seleccione opción: ")

    if opcion == "1":
        print("\n--- CLIENTES ---")
        for c in clients:
            print(c["id"], "-", c["nombre_completo"], "|", c["correo"], "|", c["telefono"], "|", c["estado"])

    elif opcion == "2":
        estados = {
            "1": "Cliente potencial",
            "2": "Alto interés",
            "3": "Cliente efectivo",
            "4": "En proceso de compra",
            "5": "Super cliente"
        }

        print("\n--- CLIENTES ---")
        for c in clients:
            print(c["id"], "-", c["nombre_completo"], "|", c["correo"], "|", c["telefono"], "|", c["estado"])

        id_editar = int(input("\nIngrese el ID del cliente a editar: "))

        cliente = None
        for c in clients:
            if c["id"] == id_editar:
                cliente = c
                break

        if cliente is None:
            print("❌ Cliente no encontrado.")
        else:
            print("\nCliente seleccionado:")
            print(cliente)

            print("\n--- EDICIÓN (Enter para mantener valor actual) ---")

            nuevo_nombre = input("Nuevo nombre completo: ").strip()
            if nuevo_nombre != "":
                cliente["nombre_completo"] = nuevo_nombre

            while True:
                nuevo_correo = input("Nuevo correo: ").strip()
                if nuevo_correo == "":
                    break
                if "@" in nuevo_correo and "." in nuevo_correo:
                    cliente["correo"] = nuevo_correo
                    break
                else:
                    print("❌ Correo inválido. Ejemplo: nombre@correo.com")

            while True:
                nuevo_telefono = input("Nuevo teléfono (+56 9 XXXXXXXX): ").strip()
                if nuevo_telefono == "":
                    break
                if (
                    nuevo_telefono.startswith("+56 9 ")
                    and len(nuevo_telefono) == 14
                    and nuevo_telefono[6:].isdigit()
                ):
                    cliente["telefono"] = nuevo_telefono
                    break
                else:
                    print("❌ Teléfono inválido. Ejemplo válido: +56 9 91234567")

            print("\nEstados disponibles:")
            for numero, nombre in estados.items():
                print(numero, "-", nombre)

            while True:
                opcion_estado = input("Seleccione número de nuevo estado (Enter para mantener): ").strip()
                if opcion_estado == "":
                    break
                if opcion_estado in estados:
                    cliente["estado"] = estados[opcion_estado]
                    break
                else:
                    print("❌ Opción inválida. Ingrese un número válido.")

            print("\n✅ CLIENTE ACTUALIZADO:")
            print(cliente["id"], "-", cliente["nombre_completo"], "|", cliente["correo"], "|", cliente["telefono"], "|", cliente["estado"])

    elif opcion == "3":
        break

    else:
        print("Opción inválida. Intente nuevamente.")