cliente_db = []

cliente_id = 1

cantidad_clientes = int(input("Ingrese la cantidad de clientes a agregar: "))

for i in range(cantidad_clientes):
    print(f"\nAgregando cliente {i + 1}:")
    nombre = input("Ingrese el nombre del cliente: ")
    apellido = input("Ingrese el apellido del cliente: ")
    telefono = input("Ingrese el teléfono del cliente: ")
    correo = input("Ingrese el correo del cliente: ")
    
    print("Seleccione el estado del cliente:")
    print("1. Cliente potencial")
    print("2. Cliente con alto interés")
    print("3. En proceso de compra")
    print("4. Cliente efectivo")
    print("5. Super cliente")
    
    estado_opcion = int(input("Ingrese el número correspondiente al estado: "))
    estado_dict = {
        1: "Cliente potencial",
        2: "Cliente con alto interés",
        3: "En proceso de compra",
        4: "Cliente efectivo",
        5: "Super cliente"
    }
    
    if estado_opcion == 1:
        estado = "Cliente potencial"
    elif estado_opcion == 2:
        estado = "Cliente con alto interés"
    elif estado_opcion == 3:
        estado = "En proceso de compra"
    elif estado_opcion == 4:
        estado = "Cliente efectivo"
    elif estado_opcion == 5:
        estado = "Super cliente"
    else:
        estado = "Estado desconocido"
        
    cliente = {
        "id": cliente_id,
        "nombre": nombre,
        "apellido": apellido,
        "teléfono": telefono,
        "correo": correo,
        "estado": estado
    }
    
    cliente_db.append(cliente)
    cliente_id += 1
    
print("\nBase de datos de clientes:")
for cliente in cliente_db:
    print(cliente)