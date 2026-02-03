class Usuario:
    campos = ["user_id", "nombre", "email", "estado"]

    def __init__(self, **kwargs):
        for c in self.campos:
            setattr(self, c, kwargs.get(c))
        if self.estado is None or self.estado is "":
            self.estado = "Activo"

    def resumen(self):
        return f"{self.user_id} - {self.nombre} - {self.email} (estado={self.estado})"

class Cliente(Usuario):
    campos = Usuario.campos + ["plan", "saldo"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.plan = kwargs.get("plan") or "free"

    def cobrar(self, **kwargs):
        monto = int(kwargs.get("monto", 0))
        if not isinstance(monto, (int, float)):
            raise TypeError("Monto debe ser numérico")
        if monto <= 0:
            raise ValueError("monto debe ser mayor a cero")
        
        self.saldo += int(monto)
        return self.saldo
    
    def pagar(self, **kwargs):
        monto = int(kwargs.get("monto", 0))
        if not isinstance(monto, (int, float)):
            raise TypeError("El monto debe ser numérico")
        
        if monto <= 0:
            raise ValueError("monto debe ser mayor a cero")

        if monto > self.saldo:
            raise ValueError("Saldo insuficiente")
        
    def resumen(self):
        resumen_base = super().resumen()
        return f"{resumen_base} | Cliente(plan = {self.plan}), saldo={self.saldo}"
    

        
class Staff(Usuario):
    campos = Usuario.campos + ["rol", "permisos"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rol = kwargs.get("rol") or "soporte"
        permisos_lista = kwargs.get("permisos") or []
        self.permisos = set(permisos_lista)
    
    def puede(self, **kwargs):
        permiso = kwargs.get("permiso")
        if permiso is None:
                raise ValueError("Faltan 'permisos'")
        return permiso in self.permisos
    
    def resumen(self):
        resumen_base = super().resumen()
        return f"{resumen_base} | Staff rol = {self.rol}, Permisos={sorted(self.permisos)}"
    
try:
    cliente_1 = Cliente(user_id= 1, nombre= "Carla", email= "carla@mimail.cl", estado= "Activo", plan= "Pro", saldo= 10000)
except Exception as e:
    print("Error client_1" , type(e).__name__, "-", e)


'''staff_1 = Staff(user_id= 10, nombre= "Josefa", email= "josefa@miempresa.cl", estado= "Activo", rol= "Gerenta", permisos= ["cliente:editar", "tickets:Responder"])


print(cliente_1.resumen())
print(staff_1.resumen())

cliente_1.cobrar(monto=5000)
cliente_1.pagar(monto=2000)

print("Saldo pendiente:", cliente_1.saldo)

'''