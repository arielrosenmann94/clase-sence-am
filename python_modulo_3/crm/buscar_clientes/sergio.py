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
# ========== PROGRAMA PRINCIPAL ==========

continuar = True

while continuar:
    # Mostrar menú
    print("\n=== SISTEMA DE BÚSQUEDA DE CLIENTES ===")
    print("1. Buscar por ID")
    print("2. Buscar por Nombre")
    print("3. Buscar por Correo")
    print("4. Buscar por Teléfono")
    print("0. Salir")
    
    opcion = input("\nSeleccione una opción: ")
    
    # Opción 1: Buscar por ID
    if opcion == "1":
        id_buscar = int(input("Ingrese el ID a buscar: "))
        resultados = []
        
        # Buscar en la lista
        for cliente in clients:
            if cliente['id'] == id_buscar:
                resultados.append(cliente)
        
        # Mostrar resultados
        if len(resultados) == 0:
            print("\nNo se encontraron resultados.")
        else:
            print(f"\nSe encontraron {len(resultados)} resultado(s):\n")
            for cliente in resultados:
                print(f"ID: {cliente['id']}")
                print(f"Nombre: {cliente['nombre_completo']}")
                print(f"Correo: {cliente['correo']}")
                print(f"Teléfono: {cliente['telefono']}")
                print(f"Estado: {cliente['estado']}")
                print("-" * 50)
    
    # Opción 2: Buscar por Nombre
    elif opcion == "2":
        nombre_buscar = input("Ingrese el nombre a buscar: ")
        nombre_buscar = nombre_buscar.lower()
        resultados = []
        
        # Buscar en la lista
        for cliente in clients:
            if nombre_buscar in cliente['nombre_completo'].lower():
                resultados.append(cliente)
        
        # Mostrar resultados
        if len(resultados) == 0:
            print("\nNo se encontraron resultados.")
        else:
            print(f"\nSe encontraron {len(resultados)} resultado(s):\n")
            for cliente in resultados:
                print(f"ID: {cliente['id']}")
                print(f"Nombre: {cliente['nombre_completo']}")
                print(f"Correo: {cliente['correo']}")
                print(f"Teléfono: {cliente['telefono']}")
                print(f"Estado: {cliente['estado']}")
                print("-" * 50)
    
    # Opción 3: Buscar por Correo
    elif opcion == "3":
        correo_buscar = input("Ingrese el correo a buscar: ")
        correo_buscar = correo_buscar.lower()
        resultados = []
        
        # Buscar en la lista
        for cliente in clients:
            if correo_buscar in cliente['correo'].lower():
                resultados.append(cliente)
        
        # Mostrar resultados
        if len(resultados) == 0:
            print("\nNo se encontraron resultados.")
        else:
            print(f"\nSe encontraron {len(resultados)} resultado(s):\n")
            for cliente in resultados:
                print(f"ID: {cliente['id']}")
                print(f"Nombre: {cliente['nombre_completo']}")
                print(f"Correo: {cliente['correo']}")
                print(f"Teléfono: {cliente['telefono']}")
                print(f"Estado: {cliente['estado']}")
                print("-" * 50)
    
    # Opción 4: Buscar por Teléfono
    elif opcion == "4":
        telefono_buscar = input("Ingrese el teléfono a buscar: ")
        resultados = []
        
        # Buscar en la lista
        for cliente in clients:
            if telefono_buscar in cliente['telefono']:
                resultados.append(cliente)
        
        # Mostrar resultados
        if len(resultados) == 0:
            print("\nNo se encontraron resultados.")
        else:
            print(f"\nSe encontraron {len(resultados)} resultado(s):\n")
            for cliente in resultados:
                print(f"ID: {cliente['id']}")
                print(f"Nombre: {cliente['nombre_completo']}")
                print(f"Correo: {cliente['correo']}")
                print(f"Teléfono: {cliente['telefono']}")
                print(f"Estado: {cliente['estado']}")
                print("-" * 50)
# Opción 0: Salir
    elif opcion == "0":
        print("\nSaliendo del sistema...")
        continuar = False
    
    # Opción inválida
    else:
        print("\nOpción no válida. Intente nuevamente.")