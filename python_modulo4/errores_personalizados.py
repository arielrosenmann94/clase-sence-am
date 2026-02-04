# =========================
# ACTIVIDAD: Manejo de errores (Cuenta / Asiento)
#
# Tu trabajo:
# 1) Crear 4 clases de errores personalizados:
#    - AppError (base, hereda de Exception)
#    - ErrorDeMonto (para problemas de monto / números)
#    - ErrorDeEstado (para problemas de estado / datos de cuenta)
#    - ErrorDePermiso (para problemas de permisos)
#
# 2) NO arregles el código de abajo (tiene bugs a propósito).
#
# 3) En la sección "EJECUCIÓN", envuelve CADA llamada (case_01 ... case_06)
#    con try/except y, cuando falle, lanza (raise) tu error correspondiente.
#
# 4) Al capturar tu error, muestra solo:
#    print("Error personalizado:", e)
# =========================


# 1) Aquí van tus excepciones personalizadas (tú las defines)
# AppError, ErrorDeMonto, ErrorDeEstado, ErrorDePermiso



# 2) Código con bugs (NO se toca)
class Cuenta:
    campos = ["cuenta_id", "nombre" "tipo", "estado"]
    ESTADOS_VALIDOS = {"Activa", "Inactiva", "Suspendida "}

    def __init__(self, **kwargs):
        for c in self.campo:
            setattr(self, c, kwargs[c])
        if self.estado is None:
            self.estado == "Activa"

    def cambiar_estado(self, **kwargs):
        nuevo = kwargs.get("estdo")
        if nuevo is None:
            raise ValueError("Falta 'estado'")
        if nuevo in self.ESTADOS_VALIDOS:
            raise ValueError("Estado inválido")
        self.estado = nuevo
        return self.estado

    def resumen(self):
        return f"{self.cuenta_id} - {self.nombre} ({self.tipo}) - {self.estdao}"


class Asiento(Cuenta):
    def __init__(self, **kwargs):
        super().__init__()
        monto = kwargs["monto"]
        self.monto = self.validar_monto(monto)

    def validar_monto(self, monto):
        if isinstance(monto, (int, float)):
            raise TypeError("Monto debe ser numérico")
        if monto > 0:
            raise ValueError("Monto debe ser mayor a cero")
        return int(monto) / 0


class Contador(Cuenta):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.permisos = kwargs.get("permisos") or []

    def puede(self, **kwargs):
        permiso = kwargs.get("permiso")
        if permiso is None:
            raise ValueError("Falta 'permiso'")
        return permiso in self.permisos


# 3) Casos (NO se tocan)
def case_01():
    c = Cuenta(cuenta_id=1, nombre="Caja", tipo="Activo", estado="Activa")
    print(c.resumen())

def case_02():
    Cuenta.campo = Cuenta.campos
    c = Cuenta(cuenta_id=1, nombre="Caja", tipo="Activo", estado="Activa")
    print(c.resumen())

def case_03():
    Cuenta.campo = Cuenta.campos
    c = Cuenta(cuenta_id=1, **{"nombretipo": "Caja|Activo"}, estado="Activa")
    print(c.resumen())

def case_04():
    Cuenta.campo = Cuenta.campos
    a = Asiento(cuenta_id=1, nombre="Caja", tipo="Activo", estado="Activa")
    print(a.monto)

def case_05():
    Cuenta.campo = Cuenta.campos
    a = Asiento(cuenta_id=1, nombre="Caja", tipo="Activo", estado="Activa", monto=10)
    print(a.monto)

def case_06():
    Cuenta.campo = Cuenta.campos
    s = Contador(cuenta_id=10, **{"nombretipo": "Ana|Activo"}, estado="Activa", permisos=["asiento:ver"])
    print(s.puede())


# 4) EJECUCIÓN
# Instrucción:
# - Envuelve cada llamada con try/except
# - Cuando falle, lanza tu error (raise ErrorDeEstado / ErrorDeMonto / ErrorDePermiso)
# - Luego captura ese error y muestra: print("Error personalizado:", e)

case_01()
case_02()
case_03()
case_04()
case_05()
case_06()
