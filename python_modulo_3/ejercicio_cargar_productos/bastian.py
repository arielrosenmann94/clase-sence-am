productos = {}

cantidad = int(input("¿Cuántos productos desea cargar? "))

for i in range(cantidad):
    print(f"\nProducto {i + 1}")
    sku = input("Ingrese el SKU: ")
    nombre = input("Ingrese el nombre del producto: ")
    precio = float(input("Ingrese el precio del producto: "))

    productos[sku] = {
        "nombre": nombre,
        "precio": precio
    }

print("\nProductos cargados:")
for sku, datos in productos.items():
    print(f"SKU: {sku} | Nombre: {datos['nombre']} | Precio: ${datos['precio']}")