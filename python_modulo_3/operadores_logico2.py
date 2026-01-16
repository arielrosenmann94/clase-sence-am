temperatura = int(input("ingresa temperatura: "))
hora = int(input("Qué hora es?"))
ocupacion = input("hay personas en casa?:" )

try:
    if (ocupacion != True) or (6 <= hora > 23):
        print("no hacer nada")
    elif (temperatura > 23) or (hora > 18):
            print("el aire se ha encendido en frio")
    elif (temperatura < 19) or (hora > 18):
            print("se enciende en calor")
    else:
        print("no pasa nada")
except ValueError:
    print("ingresa un dato valida")


print("se termió de ejecutar")



