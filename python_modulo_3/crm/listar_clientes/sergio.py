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

# Menú principal
print("=== SISTEMA DE GESTIÓN DE CLIENTES ===")
print("1. Listar todos los clientes")
print("2. Listar clientes por estado")
print("0. Salir")

opcion = input("\nSeleccione una opción: ")

# Opción 1: Listar todos los clientes
if opcion == "1":
    print("\n--- LISTADO DE TODOS LOS CLIENTES ---\n")
    
    # Usamos for porque sabemos exactamente cuántos elementos recorrer
    for client in clients:
        print(f"ID: {client['id']}")
        print(f"Nombre: {client['nombre_completo']}")
        print(f"Correo: {client['correo']}")
        print(f"Teléfono: {client['telefono']}")
        print(f"Estado: {client['estado']}")
        print("-" * 50)

# Opción 2: Listar por estado
elif opcion == "2":
    print("\n--- ESTADOS DISPONIBLES ---")
    print("1. Cliente potencial")
    print("2. Alto interés")
    print("3. Cliente efectivo")
    print("4. En proceso de compra")
    print("5. Super cliente")
    
    estado_buscado = input("\nIngrese el estado a filtrar: ")
    
    print(f"\n--- CLIENTES CON ESTADO: {estado_buscado} ---\n")
    
    contador = 0  # Para saber si encontramos clientes
    
    # Usamos for para recorrer toda la lista
    for client in clients:
        if client['estado'] == estado_buscado:
            print(f"ID: {client['id']}")
            print(f"Nombre: {client['nombre_completo']}")
            print(f"Correo: {client['correo']}")
            print(f"Teléfono: {client['telefono']}")
            print(f"Estado: {client['estado']}")
            print("-" * 50)
            contador += 1
    
    if contador == 0:
        print("No se encontraron clientes con ese estado.")
    else:
        print(f"\nTotal de clientes encontrados: {contador}")

elif opcion == "0":
    print("Saliendo del sistema...")

else:
    print("Opción no válida")