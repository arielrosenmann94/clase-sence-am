productos = {}

cantidad = int(input("¿Cuántos productos desea cargar?: "))

contador = 1

while contador <= cantidad:
    sku = "SKU" + str(contador)
    
    nombre = input("Ingrese el nombre del producto: ")
    precio = int(input("Ingrese el precio del producto: "))

    productos[sku] = {
        "nombre": nombre,
        "precio": precio
    }

    contador = contador + 1

print("\nDiccionario de productos cargados:")
print(productos)