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
    print("\n" + "="*50)
    print("                PythonCRM")
    print("="*50)
    print("1: Mostrar todos los clientes")
    print("2: Filtrar clientes por estado")
    print("3: Buscar por ID, Nombre, Correo o Teléfono")
    print("4: Salir")
    
    user_input = input("\nSelecciona una opción: ")

    if user_input.isdigit():
        option = int(user_input)

        if option == 1:
            print("\n--- LISTADO COMPLETO DE CLIENTES ---")
            for i in range(len(clients)):
                c = clients[i]
                print(f"ID: {c['id']} | Nombre: {c['nombre_completo']} | Correo: {c['correo']} | Tel: {c['telefono']} | Estado: {c['estado']}")

        elif option == 2:
            # CORRECCIÓN 1: No uses 'option' para el input, porque 'option' 
            # guarda el número del menú (2) y lo sobreescribes.
            search_status = input("Escribe el estado que quieres filtrar: ").lower()
            found = False
            # CORRECCIÓN 2: Aquí usabas 'search_status' en el print pero no existía.
            print(f"\n--- CLIENTES CON ESTADO: '{search_status}' ---")
            for i in range(len(clients)):
                c = clients[i]
                if c["estado"].lower() == search_status:
                    print(f"ID: {c['id']} | Nombre: {c['nombre_completo']} | Correo: {c['correo']} | Tel: {c['telefono']} | Estado: {c['estado']}")
                    found = True
            if not found:
                print("No pillamos a ningún cliente con ese estado.")

        elif option == 3:
            search_term = input("Ingresa el dato del cliente a buscar: ").lower()
            found_general = False
            print(f"\n--- RESULTADOS PARA LA BÚSQUEDA: '{search_term}' ---")
            
            for i in range(len(clients)):
                c = clients[i]
                id_txt = str(c["id"])
                name = c["nombre_completo"].lower()
                mail = c["correo"].lower()
                phone = c["telefono"].lower()

                if search_term == id_txt or search_term in name or search_term in mail or search_term in phone:
                    print(f"ID: {c['id']} | Nombre: {c['nombre_completo']} | Correo: {c['correo']} | Tel: {c['telefono']} | Estado: {c['estado']}")
                    found_general = True
            
            # CORRECCIÓN 3: Aquí decía 'encontrado_general' (en español) 
            # pero tu variable se llama 'found_general'.
            if not found_general:
                print(f"No hay coincidencias para '{search_term}'.")

        elif option == 4:
            print("Cerrando el CRM... ¡Nos vemos!")
            break
        
        else:
            print("Esa opción no existe. Elige del 1 al 4.")
            
    else:
        print("¡Ojo! Tienes que meter un número entero.")