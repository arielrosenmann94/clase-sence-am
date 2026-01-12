estudiantes = ["Aquiles", "Zeus", "Apolo", "Atenea", "Hermes"]

for nombre in estudiantes:
    print("Estudiante: ", nombre)


total = 0

while total < 50:
    entrada = input("ingresa un numero para sumar (total actual = " + str(total) +"):")
    try:
        numero = int(entrada)
        total += numero
    except ValueError:
        print("Entrada invalida: ingresa una entrada correcta")
        continue

print("listo, total actual: ", total)     