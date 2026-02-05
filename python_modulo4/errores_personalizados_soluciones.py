# =========================
# SOLUCIÓN (PROFESOR) — QA PRO (mensajes senior)
# - Captura real del error (raise ... from e)
# - No muestra traceback ni error real (sin debug)
# - Salida “tipo QA” consistente: código, severidad, componente, síntoma, acción
# - Loop de casos
# =========================


# 1) Excepciones personalizadas
class AppError(Exception):
    pass

class ErrorDeMonto(AppError):
    pass

class ErrorDeEstado(AppError):
    pass

class ErrorDePermiso(AppError):
    pass


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
    return c.resumen()

def case_02():
    Cuenta.campo = Cuenta.campos
    c = Cuenta(cuenta_id=1, nombre="Caja", tipo="Activo", estado="Activa")
    return c.resumen()

def case_03():
    Cuenta.campo = Cuenta.campos
    c = Cuenta(cuenta_id=1, **{"nombretipo": "Caja|Activo"}, estado="Activa")
    return c.resumen()

def case_04():
    Cuenta.campo = Cuenta.campos
    a = Asiento(cuenta_id=1, nombre="Caja", tipo="Activo", estado="Activa")
    return a.monto

def case_05():
    Cuenta.campo = Cuenta.campos
    a = Asiento(cuenta_id=1, nombre="Caja", tipo="Activo", estado="Activa", monto=10)
    return a.monto

def case_06():
    Cuenta.campo = Cuenta.campos
    s = Contador(cuenta_id=10, **{"nombretipo": "Ana|Activo"}, estado="Activa", permisos=["asiento:ver"])
    return s.puede()


# 4) Runner QA (captura real + mensaje senior)
def ejecutar_caso_qa(case_id, fn, error_cls, qa):
    """
    qa = dict con:
      - severity: "BLOCKER" | "CRITICAL" | "MAJOR" | "MINOR"
      - component: "Cuenta" | "Asiento" | "Contador" | etc
      - symptom: texto corto del síntoma observable
      - action: instrucción práctica (qué revisar)
      - expected: qué se esperaba
    """
    try:
        valor = fn()
        print(f"[PASS] {case_id} | component={qa['component']} | result={valor}")
        return

    except Exception as e:
        # Captura real (encadenamiento), pero NO mostramos la causa
        try:
            raise error_cls(
                f"[FAIL] {case_id} | severity={qa['severity']} | component={qa['component']} | "
                f"symptom={qa['symptom']} | expected={qa['expected']} | action={qa['action']}"
            ) from e

        except AppError as ae:
            # Salida “QA pro”: clara, consistente, sin debug
            print(str(ae))


# 5) Suite de pruebas (casos)
casos = [
    {
        "id": "TC-ACC-001",
        "fn": case_01,
        "err": ErrorDeEstado,
        "qa": {
            "severity": "MAJOR",
            "component": "Cuenta",
            "symptom": "Fallo al instanciar o acceder a lista de campos",
            "expected": "La cuenta debería inicializarse y resumirse sin errores",
            "action": "Revisar nombres de atributos (campo vs campos) y estructura de campos",
        }
    },
    {
        "id": "TC-ACC-002",
        "fn": case_02,
        "err": ErrorDeEstado,
        "qa": {
            "severity": "CRITICAL",
            "component": "Cuenta",
            "symptom": "Asignación de atributos desde kwargs falla con claves obligatorias",
            "expected": "La carga de datos desde kwargs debería tolerar ausencia de claves o validarlas",
            "action": "Revisar acceso kwargs[c] vs kwargs.get(c) y consistencia de nombres de campo",
        }
    },
    {
        "id": "TC-ACC-003",
        "fn": case_03,
        "err": ErrorDeEstado,
        "qa": {
            "severity": "MAJOR",
            "component": "Cuenta",
            "symptom": "Resumen falla por atributo inexistente (typo)",
            "expected": "resumen() debe usar atributos válidos y consistentes",
            "action": "Revisar typos en f-string y nombres de atributos (ej: estdao)",
        }
    },
    {
        "id": "TC-ACC-004",
        "fn": case_04,
        "err": ErrorDeMonto,
        "qa": {
            "severity": "BLOCKER",
            "component": "Asiento",
            "symptom": "Inicialización falla por dato obligatorio ausente",
            "expected": "Si falta monto, el sistema debe validar y reportar correctamente",
            "action": "Revisar lectura directa kwargs['monto'] y validaciones previas",
        }
    },
    {
        "id": "TC-ACC-005",
        "fn": case_05,
        "err": ErrorDeMonto,
        "qa": {
            "severity": "BLOCKER",
            "component": "Asiento",
            "symptom": "Validación de monto provoca error en tiempo de ejecución",
            "expected": "Validación debe aceptar/rechazar montos y nunca provocar operaciones inválidas",
            "action": "Revisar reglas de validación (condiciones invertidas / división por cero)",
        }
    },
    {
        "id": "TC-ACC-006",
        "fn": case_06,
        "err": ErrorDePermiso,
        "qa": {
            "severity": "MAJOR",
            "component": "Contador",
            "symptom": "Chequeo de permisos falla por entrada inválida o faltante",
            "expected": "puede() debe validar que 'permiso' exista y sea evaluable",
            "action": "Revisar kwargs.get('permiso') y manejo de None",
        }
    },
]


# 6) Ejecución
print("=" * 88)
print("QA RUN — Contabilidad | suite=TC-ACC | mode=student-safe (no-debug)")
print("=" * 88)

for t in casos:
    ejecutar_caso_qa(t["id"], t["fn"], t["err"], t["qa"])

print("=" * 88)
print("QA RUN COMPLETE")
print("=" * 88)
