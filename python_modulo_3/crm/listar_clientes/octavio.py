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
    print("\n=== MENÚ CLIENTES ===")
    print("1. Listar todos")
    print("2. Listar por estado")
    print("3. Salir")

    opcion = input("Seleccione una opción: ").strip()

    # -------- LISTAR TODOS --------
    if opcion == "1":
        print("\n--- LISTADO DE TODOS LOS CLIENTES ---")
        for c in clients:
            print(
                f"ID: {c['id']} | "
                f"{c['nombre_completo']} | "
                f"Correo: {c['correo']} | "
                f"Tel: {c['telefono']} | "
                f"Estado: {c['estado']}"
            )

# -------- LISTAR POR ESTADO --------
    elif opcion == "2":
        print("\nEstados disponibles:")
        print("1. Cliente potencial")
        print("2. Alto interés")
        print("3. En proceso de compra")
        print("4. Cliente efectivo")
        print("5. Super cliente")

        switch_estado = {
            "1": "Cliente potencial",
            "2": "Alto interés",
            "3": "En proceso de compra",
            "4": "Cliente efectivo",
            "5": "Super cliente"
        }

        estado_opcion = input("Seleccione estado (1-5): ").strip()
        estado_buscado = switch_estado.get(estado_opcion)

        if estado_buscado is None:
            print("❌ Estado no válido.")
        else:
            print(f"\n--- CLIENTES CON ESTADO: {estado_buscado} ---")
            encontrados = False

            for c in clients:
                if c["estado"] == estado_buscado:
                    print(
                        f"ID: {c['id']} | "
                        f"{c['nombre_completo']} | "
                        f"Correo: {c['correo']} | "
                        f"Tel: {c['telefono']}"
                    )
                    encontrados = True

            if not encontrados:
                print("No hay clientes con ese estado.")

    # -------- SALIR --------
    elif opcion == "3":
        print("👋 Saliendo del sistema...")
        break

    else:
        print("❌ Opción inválida")