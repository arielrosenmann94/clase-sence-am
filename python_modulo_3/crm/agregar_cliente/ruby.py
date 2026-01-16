# 1. Preparación de la base de datos y el ID autoincremental
base_de_datos = []
proximo_id = 1

print("=== SISTEMA DE REGISTRO DE CLIENTES ===")

while True:
    # 2. Captura de datos básicos
    print(f"\n--- Registro de Cliente #{proximo_id} ---")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    telefono = input("Teléfono: ")
    correo = input("Correo: ")

    # 3. Clasificación del estado usando match (Switch)
    print("\nCategorías de Estado:")
    print("1. Cliente potencial\n2. Cliente con alto interés\n3. En proceso de compra\n4. Cliente efectivo\n5. Super cliente")
    
    opcion = input("Seleccione el número: ")

    match opcion:
        case "1":
            estado_texto = "Potencial"
        case "2":
            estado_texto = "Alto Interés"
        case "3":
            estado_texto = "En Proceso"
        case "4":
            estado_texto = "Efectivo"
        case "5":
            estado_texto = "Super Cliente"
        case _:
            estado_texto = "Sin Definir"

    # 4. Creación del diccionario y guardado en la lista
    cliente_dict = {
        "id": proximo_id,
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "correo": correo,
        "estado": estado_texto
    }
    
    base_de_datos.append(cliente_dict)
    
    # 5. Incremento del ID
    proximo_id += 1
    
    # Preguntar si desea continuar
    continuar = input("\n¿Desea agregar otro cliente? (s/n): ").lower()
    if continuar != 's':
        break

# 6. Visualización elegante de los datos
print("\n" + "="*85)
print(f"{'ID':<4} | {'NOMBRE':<12} | {'APELLIDO':<12} | {'TELÉFONO':<12} | {'CORREO':<20} | {'ESTADO'}")
print("-" * 85)

for c in base_de_datos:
    # Usamos f-strings con alineación para que parezca una tabla
    print(f"{c['id']:<4} | {c['nombre']:<12} | {c['apellido']:<12} | {c['telefono']:<12} | {c['correo']:<20} | {c['estado']}")

print("="*85)