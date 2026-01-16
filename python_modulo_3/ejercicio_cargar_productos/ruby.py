# 1. Preguntamos cuántos productos se van a cargar
cantidad_productos = int(input("¿Cuántos productos deseas cargar? "))

# Creamos una lista vacía para almacenar los productos
inventario = []

# 2. Iniciamos un ciclo para pedir los datos de cada producto
for i in range(cantidad_productos):
    print(f"\nCargando datos del producto {i + 1}:")
    
    sku = input("Introduce el SKU: ")
    nombre = input("Introduce el nombre del producto: ")
    precio = float(input("Introduce el precio: "))
    
    # Creamos un diccionario para el producto actual
    producto = {
        "sku": sku,
        "nombre": nombre,
        "precio": precio
    }
    
    # Guardamos el diccionario en nuestra lista
    inventario.append(producto)

# 3. Imprimimos el resultado final
print("\n--- Lista de productos cargados ---")
for p in inventario:
    print(p)