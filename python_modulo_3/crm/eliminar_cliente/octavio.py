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

clientes_eliminados = []

# ===============================
# MENÚ PRINCIPAL
# ===============================

while True:
    print("\n=== SISTEMA DE CLIENTES ===")
    print("1. Ver clientes activos")
    print("2. Eliminar cliente (mover a eliminados)")
    print("3. Ver clientes eliminados")
    print("4. Salir")

    opcion = input("Seleccione una opción: ")

    # ---------------------------
    # VER CLIENTES ACTIVOS
    # ---------------------------
    if opcion == "1":
        print("\n--- CLIENTES ACTIVOS ---")
        if len(clients) == 0:
            print("No hay clientes activos.")
        else:
            for cliente in clients:
                print(
                    cliente["id"], "-",
                    cliente["nombre_completo"], "|",
                    cliente["correo"], "|",
                    cliente["telefono"], "|",
                    cliente["estado"]
                )

    # ---------------------------
    # ELIMINAR CLIENTE
    # ---------------------------
    elif opcion == "2":
        id_eliminar = int(input("Ingrese el ID del cliente a eliminar: "))
        encontrado = False

        for cliente in clients:
            if cliente["id"] == id_eliminar:
                clientes_eliminados.append(cliente)
                clients.remove(cliente)
                encontrado = True
                print("Cliente eliminado correctamente (registro conservado).")
                break

        if not encontrado:
            print("No existe un cliente con ese ID.")

    # ---------------------------
    # VER CLIENTES ELIMINADOS
    # ---------------------------
    elif opcion == "3":
        print("\n--- CLIENTES ELIMINADOS ---")
        if len(clientes_eliminados) == 0:
            print("No hay clientes eliminados.")
        else:
            for cliente in clientes_eliminados:
                print(
                    cliente["id"], "-",
                    cliente["nombre_completo"], "|",
                    cliente["correo"], "|",
                    cliente["telefono"], "|",
                    cliente["estado"]
                )

    # ---------------------------
    # SALIR
    # ---------------------------
    elif opcion == "4":
        print("Saliendo del sistema...")
        break

    else:
        print("Opción inválida. Intente nuevamente.")