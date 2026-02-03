class Persona:
    campos = ["nombre", "edad"]

    def __init__(self, **kwargs):
        for c in self.campos:
            setattr(self, c, kwargs.get(c))

    def presentarse(self):
        print(f"hola, soy {self.nombre} y tengo {self.edad}")


class Empleado(Persona):
    campos = Persona.campos + ["cargo"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cargo = kwargs.get("cargo")


    def presentarse(self):
        print(f"Hola, soy {self.nombre}, tengo {self.edad} y mi cargo es {self.cargo}")


    def trabajar(self):
        print(f"{self.nombre}, está trabajando en el cargo de {self.cargo}")

e1 = Empleado(nombre= "Ariel", edad= 31, cargo= "Programador")



e1.presentarse()
e1.trabajar()

print(e1.nombre)


class Animal:
    campos = ["nombres"]

    def __init__(self, **kwargs):
        for c in self.campos:
            setattr(self, c, kwargs.get(c))

    def emitir_sonido(self):
        print("sonido genérico")

class Perro(Animal):

    def emitir_sonido(self):
        print("Guauu!")

class Gato(Animal):

    def emitir_sonido(self):
        print("Miaaauuu!")

class Pajaro(Animal):
    pass


firulais = Perro(nombre= "Firulais")
a2 = Gato(nombre= "Mishi")
a3 = Pajaro(nombre= "piolin")

a3.emitir_sonido()

print(f"firualis dice...") 
firulais.emitir_sonido() 
a2.emitir_sonido()



class Vehiculo:
    campos = ["marca", "modelo"]

    def __init__(self, **kwargs):
        for c in self.campos:
            setattr(self, c, kwargs.get(c))

    def moverse(self):
        print("moviendome...")


class Auto(Vehiculo):

    def moverse(self):
        print("Conduciendo por la ciudad")

class Bicicleta(Vehiculo):

    def moverse(self):
        print ("Pedaleando por la ciudad")


class Moto(Vehiculo):
    campos = Vehiculo.campos + ["cilindrada"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clinidrada = kwargs.get("cilindrada")

    def moverse(self):
        print("También voy por la carreteras, pero más feliz")


vehiculos = [
    Auto(marca= "Toyota", modelo= "Rav 4"),
    Bicicleta(marca= "Trek", modelo= "Y3"),
    Moto(marca= "Kawasaky", modelo= "Versys", cilindrada= "650")
]

for v in vehiculos:
    v.moverse() 

    