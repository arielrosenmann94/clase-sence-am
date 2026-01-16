# Preguntar cuántos productos se quieren cargar
cantidad = int(input("¿Cuántos productos quieres cargar? "))

# Validar que sea un número positivo
if cantidad <= 0:
    print("Debes ingresar un número positivo de productos.")
else:
    # Lista para almacenar los productos
    productos = []
    
    # Cargar cada producto
    for i in range(cantidad):
        print(f"\n--- Producto {i + 1} ---")
        sku = input("SKU: ")
        nombre = input("Nombre del producto: ")
        precio = float(input("Precio: "))
        # Crear diccionario con los datos del producto
        producto = {
            'sku': sku,
            'nombre': nombre,
            'precio': precio
        }
        # Agregar el producto a la lista
        productos.append(producto)
    # Imprimir todos los productos cargados
    print("\n" + "="*50)
    print("PRODUCTOS CARGADOS:")
    print("="*50)
    
    if len(productos) == 0:
        print("No hay productos cargados.")
    else:
        for idx, prod in enumerate(productos, 1):
            print(f"\nProducto {idx}:")
            print(f"  SKU: {prod['sku']}")
            print(f"  Nombre: {prod['nombre']}")
            print(f"  Precio: ${prod['precio']:.2f}")
 # Imprimir la estructura completa (lista de diccionarios)
    print("\n" + "="*50)
    print("ESTRUCTURA COMPLETA (lista de diccionarios):")
    print("="*50)
    print(productos)