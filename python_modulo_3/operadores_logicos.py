

try:
    edad = int(input("ingresa la edad: "))
    genero = input("ingresa el genero: ")
    localidad = input("Es local o forastero?")
    
    if (edad < 18):
        print("no entra")
    elif (genero == "mujer") and (localidad == "local"):
        print("entra gratis")
    elif (edad > 30) or (genero == "mujer"):
        print("50% de descuento")
    else:
        print("paga")

except ValueError:
    print("ingresa un número válido")



print("el programa se terminó de ejecutar")