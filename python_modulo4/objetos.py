'''#Forma "A": para definir una clase
class Personas:
    def __init__(self, id, nombre, rut, correo):
                #      1  juan  18669554-3 juan@mail.com

        self.id = id
        self.nombre = nombre
        self.rut = rut
        self.correo = correo
        
p1 = Personas(
    id= 1,
    nombre= "Juan",
    rut= "18669554-3",
    correo= "juan@mail.com",
)

print(p1.nombre)


#Forma B: Para definir una clase
class Personas:
    def __init__(self, datos):
        self.id = datos["id"]
        self.nombre = datos["nombre"]
        self.rut = datos["rut"]
        self.correo = datos["correo"]

datos_persona = {
    "id": 1,
    "nombre": "María",
    "rut": "156958541-4", 
    "correo": "maria@mail.cl"
}

p2 = Personas(datos_persona)

print(p2.nombre)
'''
#Forma C: para definir una clase
class Personas:
    datos = ["id", "nombre", "rut", "correo"]

    def __init__(self, **kwargs):
        for campo in self.datos:
            setattr(self, campo, kwargs.get(campo))


p3 = Personas(
    id= 3,
    nombre= "Boris",
    rut="12658965-6",
    correo= "boris@mimail.ia",
    WhatsApp= "+569"
)


print(p3.__dict__)



        




















