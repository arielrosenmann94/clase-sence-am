product_list = [
    {"sku": "P1001", "nombre": "Audífonos Bluetooth", "precio": 24990},
    {"sku": "P1002", "nombre": "Teclado Mecánico", "precio": 44990},
    {"sku": "P1003", "nombre": "Mouse Gamer", "precio": 19990},
    {"sku": "P1004", "nombre": "Lámpara LED de Escritorio", "precio": 15990},
    {"sku": "P1005", "nombre": "Cargador Inalámbrico", "precio": 22990},
    {"sku": "P1006", "nombre": "Soporte para Notebook", "precio": 17990},
    {"sku": "P1007", "nombre": "Parlante Portátil", "precio": 29990},
    {"sku": "P1008", "nombre": "Cámara Web HD", "precio": 30990},
    {"sku": "P1009", "nombre": "Disco Duro Externo 500GB", "precio": 49990},
    {"sku": "P1010", "nombre": "Kit de Limpieza Electrónica", "precio": 10990}
]

# SKUs que están en oferta
ofertas = ["P1010", "P1007", "P1003"]

subtotal_normal = 0
subtotal_oferta = 0

print("--- TIENDA TECH - CARRITO ---")

while True:
    sku_ingresado = input("Ingrese SKU del producto (o 'fin'): ").upper()
    if sku_ingresado == "FIN":
        break
    
    # Buscamos el producto en la lista
    encontrado = False
    for p in product_list:
        if p["sku"] == sku_ingresado:
            encontrado = True
            precio = p["precio"]
            nombre = p["nombre"]
            
            # Clasificamos según el requerimiento
            if sku_ingresado in ofertas:
                subtotal_oferta += precio
                print(f"Agregado: {nombre} (En Oferta)")
            else:
                subtotal_normal += precio
                print(f"Agregado: {nombre}")
            break
    
    if not encontrado:
        print("Error: SKU no válido")

# LOGICA DE DESCUENTO
total_carrito = subtotal_normal + subtotal_oferta
descuento = 0

# Condición: Si supera los 100.000 se aplica 10% solo a lo normal
if total_carrito > 100000:
    descuento = (subtotal_normal * 10) // 100

total_pagar = total_carrito - descuento

print("-" * 30)
print(f"Total Carrito: ${total_carrito}")
print(f"Descuento Aplicado: -${descuento}")
print(f"TOTAL FINAL: ${total_pagar}")
print("-" * 30)