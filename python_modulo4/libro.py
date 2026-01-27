'''class Inventario:
    datos = ["titulo", "precio", "stock"]
    
    def __init__(self, **kwargs):
        for campo in self.datos:
            setattr(self, campo, kwargs.get(campo))

    def sumar_stock(self, cantidad):
        if cantidad > 0:
            self.stock += cantidad


libro = Inventario(titulo= "El principito", precio= "25000", stock= 50)

print(libro.stock)


libro.sumar_stock(50)

print("nuevo stock: ", libro.stock)

print("=" * 40)
print("=" * 40)
print("Nicolas")
print("=" * 40)
print("=" * 40)

class libro:
    datos = ["ISBN", "Titulo", "Autor", "Editorial","Precio", "Stock"]
    def __init__(self, **kwargs):
        for campo in self.datos:
            setattr(self, campo, kwargs.get(campo))

    def mostrar_info(self):
        for campo in self.datos:
            print(f"{campo}: {getattr(self, campo)}")
        
libros = [
    libro(ISBN="123456789", Titulo="Así habló Zaratustra", Autor="F. Nietzsche", Editorial="Editorial 1", Precio=100, Stock=10),
    libro(ISBN="987654321", Titulo="El ser y el tiempo", Autor="M. Heidegger", Editorial="Editorial 2", Precio=200, Stock=20),
    libro(ISBN="456789123", Titulo="El capital", Autor="K. Marx", Editorial="Editorial 3", Precio=300, Stock=30),
]   
for libro in libros:
    libro.mostrar_info()
    print("\n")'''

'''
print("=" * 40)
print("=" * 40)
print("Octavio")
print("=" * 40)
print("=" * 40)

class Libro:
    def __init__(self, inventario):
        self.inventario = inventario

    def mostrar_info(self):
        print(f"Título: {self.inventario.titulo}")
        print(f"Precio: ${self.inventario.precio}")
        print(f"Stock disponible: {self.inventario.stock}")

    def vender(self, cantidad):
        if cantidad <= 0:
            print("Cantidad inválida")
            return

        if self.inventario.stock >= cantidad:
            self.inventario.stock -= cantidad
            total = cantidad * int(self.inventario.precio)
            print(f"Venta realizada. Total: ${total}")
        else:
            print("Stock insuficiente")'''


'''print("=" * 40)
print("=" * 40)
print("Cintia")
print("=" * 40)
print("=" * 40)


class Inventario:
    datos = ["titulo", "precio", "stock"]

    def __init__(self, **kwargs):
        for campo in self.datos:
            setattr(self, campo, kwargs.get(campo))

    def sumar_stock(self, cantidad):
        if cantidad > 0:
            self.stock += cantidad 

    def restar_stock(self, cantidad):
        if 0 < cantidad <= self.stock:
            self.stock -= cantidad

libro = Inventario(titulo = "el principito", precio = "25000", stock = 50)

print(libro.stock)

libro.sumar_stock(50)

print("nuevo stock: ", libro.stock)

class MovimientoInventario:
    def __init__(self, inventario, tipo, cantidad):
        self.inventario = inventario   # asociación
        self.tipo = tipo               # "entrada" o "salida"
        self.cantidad = cantidad

    def ejecutar(self):
        if self.tipo == "entrada":
            self.inventario.sumar_stock(self.cantidad)
            print(f"Entrada de {self.cantidad} unidades")
        elif self.tipo == "salida":
            self.inventario.restar_stock(self.cantidad)
            print(f"Salida de {self.cantidad} unidades")
        else:
            print("Tipo de movimiento inválido")


libro = Inventario(
    titulo="El Principito",
    precio=25000,
    stock=50
)

mov1 = MovimientoInventario(libro, "entrada", 20)
mov1.ejecutar()

mov2 = MovimientoInventario(libro, "salida", 10)
mov2.ejecutar()

print("Stock final:", libro.stock) '''


'''print("=" * 40)
print("=" * 40)
print("Denissa")
print("=" * 40)
print("=" * 40)


from dataclasses import dataclass

@dataclass
class Libro:
    isbn: str
    titulo: str
    autor: str
    editorial: str
    precio: float
    stock: int

    def mostrar_info(self) -> dict:
        """Devuelve la información del libro sin imprimir (modelo desacoplado)."""
        return {
            "ISBN": self.isbn,
            "Título": self.titulo,
            "Autor": self.autor,
            "Editorial": self.editorial,
            "Precio": self.precio,
            "Stock": self.stock
        }

    def vender(self, cantidad: int) -> float:
        """Descuenta stock y devuelve el total de la venta."""
        if cantidad <= 0:
            raise ValueError("Cantidad inválida")

        if cantidad > self.stock:
            raise ValueError("Stock insuficiente")

        self.stock -= cantidad
        return self.precio * cantidad'''
    

print("=" * 40)
print("=" * 40)
print("Lala")
print("=" * 40)
print("=" * 40)

class ItemCarrito:
    campos_validos = ["titulo", "precio", "cantidad"]

    def __init__(self, **kwargs):
        for campo in self.campos_validos:
            valor = kwargs.get(campo, 0 if campo != "titulo" else "Sin título")
            setattr(self, campo, valor)

    def obtener_subtotal(self):
        if self.cantidad > 0:
            return self.cantidad * self.precio
        return 0


libro_1 = ItemCarrito(titulo="El Aleph", precio=1500, cantidad=2)
libro_2 = ItemCarrito(titulo="1984", precio=1200, cantidad=1)

print(f"Subtotal {libro_1.titulo}: ${libro_1.obtener_subtotal()}")
print(f"Subtotal {libro_2.titulo}: ${libro_2.obtener_subtotal()}")
