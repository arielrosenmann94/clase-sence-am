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
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Listados")
    print("2. Buscar cliente")
    print("3. Salir")

    opcion_menu = input("Seleccione una opción: ").strip()
# =================== MÓDULO LISTADOS ===================
    if opcion_menu == "1":
        print("\n--- SUBMENÚ LISTADOS ---")
        print("1. Listar todos")
        print("2. Listar por estado")
        print("3. Volver")

        opcion_listado = input("Seleccione una opción: ").strip()

        if opcion_listado == "1":
            print("\n--- LISTADO DE TODOS LOS CLIENTES ---")
            if len(clients) == 0:
                print("No hay clientes registrados.")
            else:
                for c in clients:
                    print(
                        f"ID: {c['id']} | {c['nombre_completo']} | "
                        f"Correo: {c['correo']} | Tel: {c['telefono']} | "
                        f"Estado: {c['estado']}"
                    )

        elif opcion_listado == "2":
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
                encontrados = 0

                for c in clients:
                    if c["estado"] == estado_buscado:
                        print(
                            f"ID: {c['id']} | {c['nombre_completo']} | "
                            f"Correo: {c['correo']} | Tel: {c['telefono']}"
                        )
                        encontrados += 1

                if encontrados == 0:
                    print("No hay clientes con ese estado.")

        elif opcion_listado == "3":
            pass
        else:
            print("❌ Opción inválida en listados.")
# =================== MÓDULO BUSCADOR ===================
    
    elif opcion_menu == "2":
        print("\n--- BUSCADOR DE CLIENTES ---")
        print("1. Buscar por ID")
        print("2. Buscar por nombre o apellido")
        print("3. Buscar por correo electrónico")
        print("4. Buscar por número de teléfono")
        print("5. Volver")

        opcion_buscar = input("Seleccione una opción: ").strip()

        # ================= BUSCAR POR ID =================
        if opcion_buscar == "1":
            print("\n💡 SUGERENCIA:")
            print("- Ingrese solo números")
            print("- El ID debe ser un número entero (ejemplo: 3, 10, 25)")

            id_texto = input("Ingrese ID: ").strip()

            if not id_texto.isdigit():
                print("❌ ID inválido. Debe contener solo números.")
            else:
                id_buscado = int(id_texto)
                encontrado = False

                for c in clients:
                    if c["id"] == id_buscado:
                        print("\n✅ Cliente encontrado:")
                        print(
                            f"ID: {c['id']} | {c['nombre_completo']} | "
                            f"Correo: {c['correo']} | Tel: {c['telefono']} | "
                            f"Estado: {c['estado']}"
                        )
                        encontrado = True
                        break

                if not encontrado:
                    print("No existe un cliente con ese ID.")

        # ================= BUSCAR POR NOMBRE =================
        elif opcion_buscar == "2":
            print("\n💡 SUGERENCIA:")
            print("- Puede ingresar nombre, apellido o parte de ellos")
            print("- No distingue mayúsculas/minúsculas")
            print("- Ejemplos: ana, torres, ramírez")

            texto = input("Ingrese nombre o apellido: ").strip().lower()

            if texto == "":
                print("❌ Búsqueda vacía.")
            else:
                encontrados = 0
                print("\nResultados:")

                for c in clients:
                    if texto in c["nombre_completo"].lower():
                        print(
                            f"ID: {c['id']} | {c['nombre_completo']} | "
                            f"Correo: {c['correo']} | Tel: {c['telefono']} | "
                            f"Estado: {c['estado']}"
                        )
                        encontrados += 1

                if encontrados == 0:
                    print("No hay coincidencias por nombre o apellido.")

        # ================= BUSCAR POR CORREO =================
        elif opcion_buscar == "3":
            print("\n💡 SUGERENCIA:")
            print("- Puede ingresar el correo completo o solo una parte")
            print("- No distingue mayúsculas/minúsculas")
            print("- Ejemplos: ana.torres, @correo.com")

            texto = input("Ingrese correo o parte del correo: ").strip().lower()

            if texto == "":
                print("❌ Búsqueda vacía.")
            else:
                encontrados = 0
                print("\nResultados:")

                for c in clients:
                    if texto in c["correo"].lower():
                        print(
                            f"ID: {c['id']} | {c['nombre_completo']} | "
                            f"Correo: {c['correo']} | Tel: {c['telefono']} | "
                            f"Estado: {c['estado']}"
                        )
                        encontrados += 1

                if encontrados == 0:
                    print("No hay coincidencias por correo.")
# ================= BUSCAR POR TELÉFONO =================
        elif opcion_buscar == "4":
            print("\n💡 SUGERENCIA:")
            print("- Puede ingresar el número completo o solo algunos dígitos")
            print("- Se aceptan formatos con espacios o +56")
            print("- Ejemplos: 94235, 942351234, +56 9")

            buscado = input("Ingrese número de teléfono o parte de él: ").strip()

            buscado_digitos = ""
            for ch in buscado:
                if ch.isdigit():
                    buscado_digitos += ch

            if buscado_digitos == "":
                print("❌ Debe ingresar al menos un dígito.")
            else:
                encontrados = 0
                print("\nResultados:")

                for c in clients:
                    tel_digitos = ""
                    for ch in c["telefono"]:
                        if ch.isdigit():
                            tel_digitos += ch

                    if buscado_digitos in tel_digitos:
                        print(
                            f"ID: {c['id']} | {c['nombre_completo']} | "
                            f"Correo: {c['correo']} | Tel: {c['telefono']} | "
                            f"Estado: {c['estado']}"
                        )
                        encontrados += 1

                if encontrados == 0:
                    print("No hay coincidencias por teléfono.")

        elif opcion_buscar == "5":
            pass
        else:
            print("❌ Opción inválida en buscador.")


    # =================== SALIR ===================
    elif opcion_menu == "3":
        print("👋 Saliendo del sistema...")
        break

    else:
        print("❌ Opción inválida")