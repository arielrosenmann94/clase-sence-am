try:
    with open("ejemplo.txt", "w", encoding="utf-8") as f:
        f.write("hola como estás")
except ValueError:
    print("Solo se deben ingresar números")

except ZeroDivisionError:
    print("no puedes dividir por cero")

finally:
    f.close()





print(6*3)
print("El programa continua")