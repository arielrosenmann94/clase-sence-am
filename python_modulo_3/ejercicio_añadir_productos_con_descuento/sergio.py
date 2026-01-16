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
    {"sku": "P1010", "nombre": "Kit de Limpieza Electrónica", "precio": 10990},
]

# Productos en oferta
productos_en_oferta = ["P1010", "P1007", "P1003"]

# Carrito de compras (lista vacía)
carrito = []

# --- AGREGAR PRODUCTOS AL CARRITO ---
# Ejemplo: Agregar Teclado Mecánico
carrito.append({"sku": "P1002", "nombre": "Teclado Mecánico", "precio": 44990, "cantidad": 1})

# Agregar Disco Duro
carrito.append({"sku": "P1009", "nombre": "Disco Duro Externo 500GB", "precio": 49990, "cantidad": 1})

# Agregar Mouse Gamer (en oferta) - 2 unidades
carrito.append({"sku": "P1003", "nombre": "Mouse Gamer", "precio": 19990, "cantidad": 2})

# Agregar Parlante (en oferta)
carrito.append({"sku": "P1007", "nombre": "Parlante Portátil", "precio": 29990, "cantidad": 1})


# --- MOSTRAR CARRITO ---
print("\n" + "="*60)
print("🛒 CARRITO DE COMPRAS")
print("="*60)

for item in carrito:
    # Verificar si está en oferta
    if item["sku"] in productos_en_oferta:
        oferta_tag = " 🏷️ EN OFERTA"
    else:
        oferta_tag = ""
    
    subtotal_item = item["precio"] * item["cantidad"]
    
    print(f"{item['nombre']}{oferta_tag}")
    print(f"  SKU: {item['sku']} | Precio: ${item['precio']:,} | Cantidad: {item['cantidad']}")
    print(f"  Subtotal: ${subtotal_item:,}")
    print()


# --- CALCULAR TOTALES ---
# Calcular subtotal total
subtotal_total = 0
for item in carrito:
    subtotal_total += item["precio"] * item["cantidad"]

# Calcular total de productos SIN oferta (para aplicar descuento)
total_sin_oferta = 0
for item in carrito:
    if item["sku"] not in productos_en_oferta:
        total_sin_oferta += item["precio"] * item["cantidad"]

# Verificar si aplica descuento del 10%
if subtotal_total >= 100000:
    aplica_descuento = True
    descuento = total_sin_oferta * 0.10
    total_final = subtotal_total - descuento
else:
    aplica_descuento = False
    descuento = 0
    total_final = subtotal_total


# --- MOSTRAR RESUMEN ---
print("-"*60)
print(f"Subtotal: ${subtotal_total:,}")

if aplica_descuento:
    print(f"Descuento 10% (sobre productos sin oferta): -${descuento:,.0f}")
    print(f"TOTAL A PAGAR: ${total_final:,.0f}")
else:
    print(f"TOTAL A PAGAR: ${total_final:,}")
    falta = 100000 - subtotal_total
    print(f"(Agregue ${falta:,} más para obtener 10% de descuento)")

print("="*60)

print("\n--- INFORMACIÓN ---")
print("• Productos en oferta: P1003, P1007, P1010")
print("• Los productos en oferta NO reciben el descuento del 10%")
print("• Pero SÍ suman para alcanzar los $100,000 que activan el descuento")