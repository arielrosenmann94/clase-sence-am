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


## ===================================
# CRM FOR THERAPISTS - BASIC VERSION
# Patient Management (No Functions)
# ===================================

patients = []          # database
last_id = 0            # auto-increment ID

# Switch-like dictionary for patient states
patient_states = {
    1: "Paciente potencial",
    2: "Paciente con alto interés",
    3: "En proceso de compra",
    4: "Cliente efectivo",
    5: "Super cliente"
}

print(
    "=" * 50 + "\n"
    "    SISTEMA CRM PARA TERAPEUTAS\n"
    "    Gestión de Pacientes\n"
    + "=" * 50
)

# -------- MAIN MENU --------
while True:
    print(
        "\n--- MENÚ PRINCIPAL ---\n"
        "1. Agregar nuevo paciente\n"
        "2. Ver todos los pacientes\n"
        "3. Salir"
    )

    option = input("\nSelecciona una opción (1-3): ")

    # ============================
    # OPTION 1: ADD PATIENT
    # ============================
    if option == "1":
        print(
            "\n" + "=" * 50 + "\n"
            "REGISTRAR NUEVO PACIENTE\n"
            + "=" * 50
        )

        print("\nSelecciona el tipo de paciente:")
        for key, value in patient_states.items():
            print(f"{key}. {value}")

        patient_type = input("\nIngresa el número (1-5): ")

        if patient_type.isdigit():
            patient_type = int(patient_type)

            if patient_type in patient_states:
                last_id += 1

                print(
                    f"\nRegistrando paciente como: {patient_states[patient_type]}\n"
                    + "-" * 50
                )

                first_name = input("Nombre: ")
                last_name = input("Apellido: ")

                # =============================
                # RUT VALIDATION (CHILE)
                # =============================
                rut_valid = False
                while not rut_valid:
                    rut = input("RUT (formato: 12345678-9): ")

                    if "-" in rut:
                        parts = rut.split("-")
                        if len(parts) == 2:
                            number = parts[0]
                            digit = parts[1]

                            if number.isdigit() and 7 <= len(number) <= 8:
                                if digit.isdigit() or digit.upper() == "K":
                                    rut_valid = True
                                else:
                                    print("✗ El dígito verificador debe ser un número o 'K'")
                            else:
                                print("✗ El número debe tener entre 7 y 8 dígitos")
                        else:
                            print("✗ Formato inválido. Usa 12345678-9")
                    else:
                        print("✗ Debes incluir el guión (ej: 12345678-9)")

                # =============================
                # PHONE VALIDATION (CHILE)
                # =============================
                phone_valid = False
                while not phone_valid:
                    phone = input("Teléfono (formato: +56912345678 o 912345678): ")
                    phone = phone.replace(" ", "")

                    if phone.startswith("+56"):
                        phone_number = phone[3:]
                        if phone_number.isdigit() and len(phone_number) == 9:
                            phone = "+56" + phone_number
                            phone_valid = True
                            print(f"✓ Teléfono válido: {phone}")
                        else:
                            print("✗ Después de +56 deben ir 9 dígitos")

                    elif phone.isdigit() and len(phone) == 9 and phone.startswith("9"):
                        phone = "+56" + phone
                        phone_valid = True
                        print(f"✓ Teléfono válido: {phone}")

                    else:
                        print("✗ Formato inválido. Usa +56912345678 o 912345678")

                # =========================













































'''def list_all_clients(client_list):
    print("\nLISTADO DE TODOS LOS CLIENTES\n" + "-" * 40)

    for client in client_list:
        print(
            f"ID: {client['id']}\n"
            f"Nombre: {client['nombre_completo']}\n"
            f"Correo: {client['correo']}\n"
            f"Teléfono: {client['telefono']}\n"
            f"Estado: {client['estado']}\n"
            + "-" * 40
        )
def list_clients_by_state(client_list, state):
    print(f"\nCLIENTES CON ESTADO: {state}\n" + "-" * 40)
    found = False

    for client in client_list:
        if client["estado"].lower() == state.lower():
            found = True
            print(
                f"ID: {client['id']}\n"
                f"Nombre: {client['nombre_completo']}\n"
                f"Correo: {client['correo']}\n"
                f"Teléfono: {client['telefono']}\n"
                + "-" * 40
            )

    if not found:
        print("No se encontraron clientes con ese estado.")
while True:
    print(
        "\n--- MENÚ PRINCIPAL ---\n"
        "1. Listar todos los clientes\n"
        "2. Listar clientes por estado\n"
        "3. Salir"
    )

    option = input("Selecciona una opción: ")

    if option == "1":
        list_all_clients(clients)

    elif option == "2":
        state = input("Ingresa el estado a filtrar: ")
        list_clients_by_state(clients, state)

    elif option == "3":
        print("Saliendo del sistema...")
        break

    else:
        print("Opción inválida.")'''