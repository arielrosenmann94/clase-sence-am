import re

print("=== VALIDACIÓN DE CORREO ELECTRÓNICO ===\n")

correo_valido = False
while not correo_valido:
    correo = input("Ingrese su correo electrónico: ").strip()
    
    # Validar formato del correo con regex
    patron_correo = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(patron_correo, correo):
        print(f"\n✓ Correo válido: {correo}\n")
        correo_valido = True
    else:
        print("✗ Formato de correo incorrecto. Intente nuevamente.\n")


print("=== VALIDACIÓN DE TELÉFONO CHILENO ===")
print("Formatos aceptados:")
print("  - Celular: 9 XXXX XXXX o +569 XXXX XXXX")
print("  - Fijo: 2 XXXX XXXX o +562 XXXX XXXX\n")

telefono_valido = False
while not telefono_valido:
    telefono = input("Ingrese su teléfono: ").strip()
    
    # Eliminar espacios, guiones y paréntesis
    tel_limpio = re.sub(r'[\s\-()]', '', telefono)
    
    # Patrones aceptados para teléfonos chilenos
    patrones_telefono = [
        r'^9\d{8}$',              # 9 XXXXXXXX (celular)
        r'^\+569\d{8}$',          # +569 XXXXXXXX (celular con código país)
        r'^2\d{8}$',              # 2 XXXXXXXX (fijo Santiago)
        r'^\+562\d{8}$',          # +562 XXXXXXXX (fijo Santiago con código país)
        r'^(3[1-9]|4[1-5]|5[1-5]|6[1-5]|7[1-5])\d{7}$',  # Otros códigos de área
        r'^\+56(3[1-9]|4[1-5]|5[1-5]|6[1-5]|7[1-5])\d{7}$'  # Con +56
    ]
    
    # Verificar si el teléfono coincide con algún patrón
    es_valido = False
    for patron in patrones_telefono:
        if re.match(patron, tel_limpio):
            es_valido = True
            break
    
    if es_valido:
        print(f"\n✓ Teléfono válido: {telefono}\n")
        telefono_valido = True
    else:
        print("✗ Formato de teléfono incorrecto. Intente nuevamente.\n")


# Resumen final
print("=" * 50)
print("DATOS VALIDADOS CORRECTAMENTE")
print("=" * 50)
print(f"Correo:   {correo}")
print(f"Teléfono: {telefono}")
print("=" * 50)