with open("python_modulo4/miarchivo.txt", "w", encoding="utf-8") as f:
    f.write("Hola pirinola")

with open("python_modulo4/miarchivo.txt", "r", encoding="utf-8") as f:
    conetnido = f.read()

print("el contenido es:")
print(conetnido)

with open("python_modulo4/miarchivo.txt", "w", encoding="utf-8") as f:
    f.write("¿Cómo estás?")

with open("python_modulo4/miarchivo.txt", "r", encoding="utf-8") as f:
    conetnido = f.read()

print("el contenido es:")
print(conetnido)

with open("python_modulo4/miarchivo.txt", "w", encoding="utf-8") as f:
    f.write("Hola pirinola")


with open("python_modulo4/miarchivo.txt", "r", encoding="utf-8") as f:
    conetnido = f.read()

print("el contenido es:")
print(conetnido)


with open("python_modulo4/miarchivo.txt", "a", encoding="utf-8") as f:
    f.write("\n¿Cómo estás?")


with open("python_modulo4/miarchivo.txt", "r", encoding="utf-8") as f:
    conetnido = f.read()

print("el contenido es:")
print(conetnido)



def reemplazar_texto_en_archivo(**kwargs):
    ruta = kwargs.get("ruta")
    buscar = kwargs.get("buscar")
    reemplazo = kwargs.get("reemplazo")

    if ruta is None or buscar is None or reemplazo is None:
        raise ValueError("Falta 'ruta', 'buscar' o 'reemplazo'")

    # 1) Leer
    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read()

    # 2) Reemplazar
    nuevo_contenido = contenido.replace(buscar, reemplazo)

    # 3) Escribir (sobrescribe el archivo)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(nuevo_contenido)

    return True


# --- DEMO ---
reemplazar_texto_en_archivo(
    ruta="python_modulo4/miarchivo.txt",
    buscar="pirinola",
    reemplazo="Ariel"
)

print("OK: texto reemplazado")

