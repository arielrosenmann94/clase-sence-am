entrada = input("escribe un número: ")

try:
    numero = int(entrada)
    if numero == 0:
        print("el numero es cero")
    elif numero % 2 == 0:
        print("el numero es par")
    else:
        print("el numero es impar")
except ValueError:
    print("ingresa un número válido")



print("el programa se terminó de ejecutar")