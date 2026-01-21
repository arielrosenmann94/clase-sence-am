patients = [
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
    {"id": 19, "nombre_completo": "Ricardo Espinoza", "correo": "ricardo.espinoza@correo.com", "telefono": "+56 9 96432187", "estado": "Cliente efectivo"},
    {"id": 20, "nombre_completo": "Ricardo Vergara", "correo": "ricardo.vergara@correo.com", "telefono": "+56 9 78912345", "estado": "Super cliente"}
]

# ===================================
# SEARCH.PY - Módulo de búsqueda
# Se ejecuta cuando main.py lo importa con exec()
# ===================================

# --- SUBMENÚ BUSCAR (while con break) ---
while True:
    print("\n" + "-" * 30)
    print("BUSCAR PACIENTES")
    print("-" * 30)
    print("1. Buscar por ID")
    print("2. Buscar por nombre")
    print("3. Buscar por correo")
    print("4. Buscar por teléfono")
    print("5. Volver al menú principal")
    
    search_option = input("\nSelecciona (1-5): ")
    
    # --- BUSCAR POR ID ---
    if search_option == "1":
        print("\n" + "-" * 30)
        print("BUSCAR POR ID")
        print("-" * 30)
        
        search_id = input("Ingresa el ID: ")
        
        if search_id.isdigit():
            search_id = int(search_id)
            found = False
            
            for patient in patients:
                if patient["id"] == search_id:
                    found = True
                    print("\n✓ Paciente encontrado:")
                    print("  " + "-" * 30)
                    print(f"  ID: {patient['id']}")
                    print(f"  Nombre: {patient['nombre_completo']}")
                    print(f"  Correo: {patient['correo']}")
                    print(f"  Teléfono: {patient['telefono']}")
                    print(f"  Estado: {patient['estado']}")
                    print("  " + "-" * 30)
                    break
            
            if not found:
                print(f"\n✗ No se encontró paciente con ID: {search_id}")
        else:
            print("\n✗ El ID debe ser un número")
    
    # --- BUSCAR POR NOMBRE ---
    elif search_option == "2":
        print("\n" + "-" * 30)
        print("BUSCAR POR NOMBRE")
        print("-" * 30)
        
        search_name = input("Ingresa nombre o parte del nombre: ").strip().lower()
        
        if search_name:
            print("\n" + "=" * 50)
            print(f"RESULTADOS PARA: '{search_name}'")
            print("=" * 50)
            
            count = 0
            
            for patient in patients:
                if search_name in patient["nombre_completo"].lower():
                    count += 1
                    print(f"\n  ID: {patient['id']}")
                    print(f"  Nombre: {patient['nombre_completo']}")
                    print(f"  Correo: {patient['correo']}")
                    print(f"  Teléfono: {patient['telefono']}")
                    print(f"  Estado: {patient['estado']}")
                    print("  " + "-" * 30)
            
            if count == 0:
                print("\n✗ No se encontraron coincidencias")
            else:
                print(f"\nTotal encontrados: {count}")
        else:
            print("\n✗ Debes ingresar un nombre")
    
    # --- BUSCAR POR CORREO ---
    elif search_option == "3":
        print("\n" + "-" * 30)
        print("BUSCAR POR CORREO")
        print("-" * 30)
        
        search_email = input("Ingresa correo o parte del correo: ").strip().lower()
        
        if search_email:
            print("\n" + "=" * 50)
            print(f"RESULTADOS PARA: '{search_email}'")
            print("=" * 50)
            
            count = 0
            
            for patient in patients:
                if search_email in patient["correo"].lower():
                    count += 1
                    print(f"\n  ID: {patient['id']}")
                    print(f"  Nombre: {patient['nombre_completo']}")
                    print(f"  Correo: {patient['correo']}")
                    print(f"  Teléfono: {patient['telefono']}")
                    print(f"  Estado: {patient['estado']}")
                    print("  " + "-" * 30)
            
            if count == 0:
                print("\n✗ No se encontraron coincidencias")
            else:
                print(f"\nTotal encontrados: {count}")
        else:
            print("\n✗ Debes ingresar un correo")
    
  
# --- BUSCAR POR TELÉFONO ---
    elif search_option == "4":
        print("\n" + "-" * 30)
        print("BUSCAR POR TELÉFONO")
        print("-" * 30)
        
        search_phone = input("Ingresa teléfono o parte del número: ").strip()
        search_phone = search_phone.replace(" ", "")
        
        if search_phone:
            print("\n" + "=" * 50)
            print(f"RESULTADOS PARA: '{search_phone}'")
            print("=" * 50)
            
            count = 0
            
            for patient in patients:
                phone_clean = patient["telefono"].replace(" ", "")
                
                if search_phone in phone_clean:
                    count += 1
                    print(f"\n  ID: {patient['id']}")
                    print(f"  Nombre: {patient['nombre_completo']}")
                    print(f"  Correo: {patient['correo']}")
                    print(f"  Teléfono: {patient['telefono']}")
                    print(f"  Estado: {patient['estado']}")
                    print("  " + "-" * 30)
            
            if count == 0:
                print("\n✗ No se encontraron coincidencias")
            else:
                print(f"\nTotal encontrados: {count}")
        else:
            print("\n✗ Debes ingresar un teléfono")
    
    # --- VOLVER ---
    elif search_option == "5":
        break  # ← BREAK del submenú buscar
    
    else:
        print("\n✗ Opción no válida")