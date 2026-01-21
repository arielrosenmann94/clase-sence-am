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



# ESTADOS DISPONIBLES
# -----------------------------
states = {
    "1": "Cliente potencial",
    "2": "Alto interés",
    "3": "En proceso de compra",
    "4": "Cliente efectivo",
    "5": "Super cliente"
}

# =============================
# MENÚ PRINCIPAL
# =============================
while True:
    print(
        "\n--- MENÚ CLIENTES ---\n"
        "1. Ver clientes\n"
        "2. Editar cliente\n"
        "3. Salir"
    )

    option = input("\nSeleccione opción: ").strip()

    # =============================
    # 1. LISTAR CLIENTES
    # =============================
    if option == "1":
        print("\n--- CLIENTES REGISTRADOS ---")

        if len(clients) == 0:
            print("No hay clientes.")
        else:
            for c in clients:
                print(
                    f"\nID: {c['id']}\n"
                    f"Nombre: {c['nombre_completo']}\n"
                    f"Correo: {c['correo']}\n"
                    f"Teléfono: {c['telefono']}\n"
                    f"Estado: {c['estado']}\n"
                    + "-" * 30
                )

    # =============================
    # 2. EDITAR CLIENTE
    # =============================
    elif option == "2":
        print("\n--- EDITAR CLIENTE ---")

        # Mostrar clientes
        for c in clients:
            print(f"{c['id']} - {c['nombre_completo']}")

        id_input = input("\nIngrese ID del cliente a editar: ").strip()

        if not id_input.isdigit():
            print("❌ El ID debe ser numérico.")
            continue

        id_edit = int(id_input)

        # Buscar cliente
        client = None
        for c in clients:
            if c["id"] == id_edit:
                client = c
                break

        if client is None:
            print("❌ Cliente no encontrado.")
            continue

        print(
            "\nCliente seleccionado:\n"
            f"Nombre: {client['nombre_completo']}\n"
            f"Correo: {client['correo']}\n"
            f"Teléfono: {client['telefono']}\n"
            f"Estado: {client['estado']}"
        )

        print("\n--- EDICIÓN (Enter para mantener valor) ---")

        # -----------------------------
        # EDITAR NOMBRE
        # -----------------------------
        new_name = input("Nuevo nombre completo: ").strip()
        if new_name:
            client["nombre_completo"] = new_name

        # -----------------------------
        # EDITAR CORREO
        # -----------------------------
        while True:
            new_email = input("Nuevo correo: ").strip()
            if new_email == "":
                break

            at_pos = new_email.find("@")
            dot_pos = new_email.rfind(".")

            if at_pos > 0 and dot_pos > at_pos + 1 and dot_pos < len(new_email) - 1:
                email_exists = False
                for c in clients:
                    if c["correo"].lower() == new_email.lower() and c["id"] != client["id"]:
                        email_exists = True
                        break

                if email_exists:
                    print("❌ Correo ya registrado.")
                else:
                    client["correo"] = new_email
                    break
            else:
                print("❌ Formato inválido. Ej: nombre@correo.com")
# EDITAR TELÉFONO (CHILE)
        # -----------------------------
        while True:
            new_phone = input("Nuevo teléfono (912345678 o +56912345678): ").strip()
            if new_phone == "":
                break

            new_phone = new_phone.replace(" ", "")

            if new_phone.startswith("+56"):
                phone_number = new_phone[3:]
                if phone_number.isdigit() and len(phone_number) == 9:
                    client["telefono"] = "+56" + phone_number
                    break
                else:
                    print("❌ Teléfono inválido.")
            elif new_phone.isdigit() and len(new_phone) == 9 and new_phone.startswith("9"):
                client["telefono"] = "+56" + new_phone
                break
            else:
                print("❌ Formato inválido.")

        # -----------------------------
        # EDITAR ESTADO
        # -----------------------------
        print("\nEstados disponibles:")
        for k, v in states.items():
            print(f"{k}. {v}")

        while True:
            state_option = input("Nuevo estado (Enter para mantener): ").strip()
            if state_option == "":
                break
            if state_option in states:
                client["estado"] = states[state_option]
                break
            else:
                print("❌ Estado inválido.")

        print(
            "\n✅ CLIENTE ACTUALIZADO:\n"
            f"{client['id']} - {client['nombre_completo']} | "
            f"{client['correo']} | {client['telefono']} | {client['estado']}"
        )

    # =============================
    # 3. SALIR
    # =============================
    elif option == "3":
        print("\nSaliendo del sistema...")
        break

    else:
        print("❌ Opción inválida.")