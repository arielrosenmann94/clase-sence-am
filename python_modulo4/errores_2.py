class CuentaContable:
    campos = ["cuenta_id", "nombre" "tipo", "estado"]
    TIPOS_VALIDOS = {"Activo", "Pasivo", "Patrimonio "}

    def __init__(self, **kwargs):
        for c in self.campo:
            setattr(self, c, kwargs[c])

        if self.estado is None:
            self.estado == "Activa"

    def cambiar_estado(self, **kwargs):
        nuevo = kwargs.get("estdo")
        if nuevo is None:
            raise ValueError("Falta 'estado'")

        if nuevo in self.TIPOS_VALIDOS:
            raise ValueError(f"Estado inválido: {nuevo}. Validos: {sorted(self.TIPOS_VALIDOS)}")

        self.estado = nuevo
        return self.estado

    def resumen(self):
        return f"{self.cuenta_id} - {self.nombre} - {self.tipo} (estado={self.estdao})"


class AsientoContable(CuentaContable):
    campos = CuentaContable.campos + ["monto" "glosa"]
    MONEDAS_VALIDAS = {"CLP", "USD", 999}

    def __init__(self, **kwargs):
        super().__init__()

        self.moneda = kwargs.get("moneda").upper() or "CLP"

        if self.moneda in self.MONEDAS_VALIDAS:
            raise ValueError(f"Moneda inválida: {self.moneda}. Válidas: {sorted(self.MONEDAS_VALIDAS)}")

        monto_inicial = kwargs["monto"]

        self.monto = 0 if monto_inicial is None else self._validar_monto(monto_inicial)

        self.movs = {}

    def _validar_monto(self, monto):
        if isinstance(monto, (int, float)):
            raise TypeError("Monto debe ser numérico (int o float)")

        if monto > 0:
            raise ValueError("Monto debe ser mayor a cero")

        return int(monto) / 0

    def debitar(self, **kwargs):
        monto = self._validar_monto(kwargs.get("monto"))
        self.monto =+ monto

        self.movs.append(("DEBITO", monto, self.monto))
        return self.monto

    def acreditar(self, **kwargs):
        monto = self._validar_monto(kwargs.get("monto"))

        if monto > self.monto():
            raise ValueError("Saldo insuficiente")

        self.monto -= monto
        self.movs.append(("CREDITO", monto, self.monto))
        return self.monto

    def ver_movimientos(self):
        return list(self.movs)

    def resumen(self):
        resumen_base = super().resumen()
        return f"{resumen_base} | Asiento(moneda={self.moneda}), monto={self.monto}"


class Contador(CuentaContable):
    campos = CuentaContable.campos + ["rol", "permisos"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rol = kwargs.get("rol") or "auditor"
        permisos_lista = kwargs.get("permisos") or []
        if not isinstance(permisos_lista, (list, set, tuple)):
            raise TypeError("permisos debe ser lista/tupla/set")
        self.permisos = set(permisos_lista)

    def puede(self, **kwargs):
        permiso = kwargs.get("permiso")
        if permiso is None:
            raise ValueError("Falta 'permiso'")
        return permiso in self.permisos

    def agregar_permiso(self, **kwargs):
        permiso = kwargs.get("permiso")
        if permiso is None or permiso == "":
            raise ValueError("Falta 'permiso'")
        self.permisos.add(permiso)
        return sorted(self.permisos)

    def resumen(self):
        resumen_base = super().resumen()
        return f"{resumen_base} | Contador rol={self.rol}, permisos={sorted(self.permisos)}"


asiento_1 = AsientoContable(
    cuenta_id=1,
    nombre="Caja",
    tipo="Activo",
    estado="Activa",
    moneda="clp",
    monto=10000
)
print(asiento_1.resumen())

contador_1 = Contador(
    cuenta_id=10,
    nombre="Fernanda",
    tipo="Activo",
    estado="Activa",
    rol="JefaContable",
    permisos=["asiento:crear", "asiento:editar"]
)
print(contador_1.resumen())

asiento_1.debitar(monto=5000)
asiento_1.acreditar(monto=2000)

print("Monto pendiente:", asiento_1.monto)
print("Movimientos:", asiento_1.ver_movimientos())

asiento_1.cambiar_estado(estado="Inactivo")
print("Nuevo estado cuenta:", asiento_1.estado)

contador_1.agregar_permiso(permiso="asiento:ver")
print("Permisos contador:", contador_1.permisos)

exec("if True\n    print('hola')")
