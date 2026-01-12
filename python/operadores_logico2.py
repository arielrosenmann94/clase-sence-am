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




















fingerprint_database = "X"
fingerprint_input = input("Ingrese su huella digital: ")
family_member = None

if fingerprint_input == fingerprint_database:
    print("La puerta se abre")
elif (fingerprint_database == None) and (family_member == True):
    print("Quiere regstrar su huella para entrar?")
else:
    print("Acceso denegado")