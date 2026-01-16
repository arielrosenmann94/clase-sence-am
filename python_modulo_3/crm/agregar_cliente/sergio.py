# Base de datos de clientes (lista con diccionarios)
clientes = []

# Variable para el ID autoincremental
proximo_id = 1

print("=== SISTEMA DE REGISTRO DE CLIENTES ===\n")

# Solicitar datos del cliente
nombre = input("Ingresa el nombre del cliente: ")
apellido = input("Ingresa el apellido del cliente: ")
telefono = input("Ingresa el teléfono del cliente: ")
correo = input("Ingresa el correo del cliente: ")

# Mostrar opciones de estado
print("\n--- Selecciona el estado del cliente ---")
print("1. Cliente potencial")
print("2. Cliente con alto interés")
print("3. En proceso de compra")
print("4. Cliente efectivo")
print("5. Super cliente")

opcion_estado = input("\nElige una opción (1-5): ")

# Validar que sea un número
if opcion_estado.isdigit():
    opcion = int(opcion_estado)
    
    # Switch usando diccionario con .get()
    estados_switch = {
        1: "Cliente potencial",
        2: "Cliente con alto interés",
        3: "En proceso de compra",
        4: "Cliente efectivo",
        5: "Super cliente"
    }
    
    estado_seleccionado = estados_switch.get(opcion, None)
    
    # Verificar si la opción es válida
    if estado_seleccionado != None:
        # Crear el nuevo cliente
        nuevo_cliente = {
            "id": proximo_id,
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono,
            "correo": correo,
            "estado": estado_seleccionado
        }
        
        # Agregar a la base de datos
        clientes.append(nuevo_cliente)
        
        # Incrementar el ID para el próximo cliente
        proximo_id += 1
        
        print("\n✓ Cliente registrado exitosamente!")
        print(f"\nDatos del cliente:")
        print(f"ID: {nuevo_cliente['id']}")
        print(f"Nombre completo: {nuevo_cliente['nombre']} {nuevo_cliente['apellido']}")
        print(f"Teléfono: {nuevo_cliente['telefono']}")
        print(f"Correo: {nuevo_cliente['correo']}")
        print(f"Estado: {nuevo_cliente['estado']}")
    else:
        print("\n✗ La opción seleccionada es inválida. Debe ser un número entre 1 y 5.")
else:
    print("\n✗ Opción inválida, debes escribir un número.")

# Mostrar la base de datos actual
print("\n--- BASE DE DATOS ACTUAL ---")
print(clientes)