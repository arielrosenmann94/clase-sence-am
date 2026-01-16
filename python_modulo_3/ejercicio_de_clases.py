#Nicolás
import random
sistema_de_huellas=["huella_1", "huella_2", "huella_3"]
huellas_validadas=   ["huella_2"]
parentezco= ["familiar", "no_familiar"]

usuario= [random.choice(sistema_de_huellas), random.choice(parentezco)]
print(usuario) 
if usuario[0] in huellas_validadas:
    print("la puerta se abre")
elif usuario[0] not in huellas_validadas and usuario[1] == parentezco[1]:
    print("acceso denegado")
elif usuario[0] not in huellas_validadas and usuario[1] == parentezco[0]:
    print("Acceso denegado, ¿Desea ingresar su huella?")




#octavio

huella = input("Ingresa huella")
familiar = "es familiar"
registrada = False

try:
    if huella == registrada:
        print ("Se abre puerta")
    elif huella == familiar:
        print ("se puede registrar para entrar")
    else:
        print("No se puede entrar")
except ValueError:
    print("es un error de valor")



#Jorge
huelladigital = int(input("ingresa huella: "))
familiar = input("es parte del grupo familiar?:" )

try:
    if (huelladigital != True):
        print("la puerta se abre")
    elif (familiar != True):
        print("Quiere registrar su huella?")
    elif (huelladigital != False):
        print("Acceso denegado")
except ValueError:
    print("Huella no valida")


try:
    huelladigital = int(input("ingresa huella (id numerica): "))
    familiar = input("es parte del grupo familiar? (si/no): ").strip().lower()

    if huelladigital == 1:
        print("la puerta se abre")
    elif familiar in ("si", "s", "yes", "y"):
        print("Quiere registrar su huella?")
    else:
        print("Acceso denegado")
except ValueError:
    print("Huella no valida")





## Roberto


fingerprint_database = "X"
fingerprint_input = input("Ingrese su huella digital: ")
family_member = None

if fingerprint_input == fingerprint_database:
    print("La puerta se abre")
elif (fingerprint_database == None) and (family_member == True):
    print("Quiere regstrar su huella para entrar?")
else:
    print("Acceso denegado")