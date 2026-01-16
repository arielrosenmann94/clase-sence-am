print("\n" + "=" * 50)
print("ADMINISTRADOR DE PRODUCTOS PYME")
print("=" * 50)

productos = {}

# Solicitar cantidad de productos
while True:
    try:
        cantidad = int(input("\n¿Cuántos productos desea cargar? "))
        if cantidad > 0:
            break
        print(" El número debe ser mayor a 0.")
    except ValueError:
        print(" Por favor, ingrese un número válido.")

print(f"\n Ingrese los datos de {cantidad} producto(s):\n")

# Cargar productos
for i in range(cantidad):
    print(f"── Producto {i + 1} de {cantidad} ──")
    
    # Validar SKU
    while True:
        sku = input("   SKU: ").strip().upper()
        if not sku:
            print("    El SKU no puede estar vacío.")
        elif sku in productos:
            print(f"    El SKU '{sku}' ya existe. Ingrese uno diferente.")
        else:
            break
    
    # Validar nombre
    while True:
        nombre = input("   Nombre: ").strip()
        if nombre:
            break
        print("    El nombre no puede estar vacío.")
    
    # Validar precio
    while True:
        try:
            precio = float(input("   Precio: $"))
            if precio > 0:
                break
            print("    El precio debe ser mayor a 0.")
        except ValueError:
            print("    Por favor, ingrese un precio válido.")
    
    # Agregar producto al diccionario
    productos[sku] = {
        "nombre": nombre,
        "precio": precio
    }
    print(f"   Producto '{nombre}' agregado correctamente.\n")

# Mostrar productos cargados
print("\n" + "=" * 60)
print("LISTADO DE PRODUCTOS CARGADOS")
print("=" * 60)
print(f"{'SKU':<12} {'NOMBRE':<25} {'PRECIO':>15}")
print("-" * 60)

total = 0
for sku, datos in productos.items():
    precio = datos['precio']
    total += precio
    print(f"{sku:<12} {datos['nombre']:<25} ${precio:>14,.0f}")

print("-" * 60)
print(f"{'TOTAL PRODUCTOS:':<38} {len(productos)}")
print(f"{'SUMA TOTAL:':<37} ${total:>14,.0f}")
print("=" * 60)

print("\n ¡Gracias por usar el sistema!\n")


