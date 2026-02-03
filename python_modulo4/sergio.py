import re


class Cliente:
    campos = ["id", "nombre", "email", "telefono", "direccion"]

    def __init__(self, **kwargs):
        # Carga automática de atributos según lista "campos"
        for c in self.campos:
            setattr(self, c, kwargs.get(c))

        # Normalización mínima
        self.id = int(self.id)
        self.nombre = str(self.nombre).strip()
        self.email = str(self.email).strip()
        self.telefono = str(self.telefono).strip()
        self.direccion = str(self.direccion).strip()

        # Validaciones mínimas
        if not self.nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if not self.validar_email(self.email):
            raise ValueError(f"Email inválido: {self.email}")
        if not self.validar_telefono(self.telefono):
            raise ValueError(f"Teléfono inválido: {self.telefono}")
        if not self.direccion:
            raise ValueError("La dirección no puede estar vacía.")

    @staticmethod
    def validar_email(email: str) -> bool:
        patron = r"^[\w\.\+\-]+@[\w\-]+\.[\w\.\-]+$"
        return bool(re.match(patron, email))

    @staticmethod
    def validar_telefono(telefono: str) -> bool:
        t = telefono.replace(" ", "")
        patron = r"^\+?\d{8,15}$"
        return bool(re.match(patron, t))

    def beneficios(self) -> str:
        return "Cliente estándar: sin beneficios especiales."


class ClienteRegular(Cliente):
    campos = Cliente.campos + ["puntos_fidelidad"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.puntos_fidelidad = int(self.puntos_fidelidad or 0)

    def sumar_puntos(self, puntos: int) -> None:
        if puntos < 0:
            raise ValueError("No puedes sumar puntos negativos.")
        self.puntos_fidelidad += puntos

    def beneficios(self) -> str:
        return f"Cliente {self.nombre}: acumula puntos (actual: {self.puntos_fidelidad})."


class ClientePremium(Cliente):
    campos = Cliente.campos + ["descuento_pct"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.descuento_pct = float(self.descuento_pct or 0.0)

        if not (0.0 <= self.descuento_pct <= 100.0):
            raise ValueError("descuento_pct debe estar entre 0 y 100.")

    def calcular_descuento(self, monto: float) -> float:
        if monto < 0:
            raise ValueError("El monto no puede ser negativo.")
        return monto * (self.descuento_pct / 100.0)

    def beneficios(self) -> str:
        return f"Cliente {self.nombre}: descuento {self.descuento_pct:.1f}%."
    

c1 = ClienteRegular(
    id=input("ingresa ID"), nombre=input("ingresa nombre"), email="ana@mail.com",
    telefono="+56912345678", direccion="Concepción",
    puntos_fidelidad=10
)

c2 = ClientePremium(
    id=2, nombre="Luis", email="luis@mail.com",
    telefono="912345678", direccion="Santiago",
    descuento_pct=15
)

#main.py
print(c1.beneficios())
print(c2.beneficios())