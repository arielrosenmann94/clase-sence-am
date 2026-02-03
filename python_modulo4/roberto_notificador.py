'''Notificador que sirve para enviar mensajes por WhatsApp, Email y SMS'''

#Súper clase: Notificador
class Notificador:
    CAMPOS_OBLIGATORIOS = ["nombre_remitente", "nombre_destinatario", "texto_mensaje"]

    def __init__(self, **kwargs):
        self.datos = kwargs

    def validar_datos(self) -> bool:
        for campo in self.CAMPOS_OBLIGATORIOS:
            if not self.datos.get(campo):
                return False
        return True

    def mostrar_mensaje(self) -> str:
        return f"{self.datos.get('nombre_remitente')} -> {self.datos.get('nombre_destinatario')}: {self.datos.get('texto_mensaje')}"

    def enviar(self) -> bool:
        raise NotImplementedError("Este método debe ser implementado por las subclases")

#Subclase: Notificador por Email
class Notificador_Email(Notificador):
    CAMPOS_OBLIGATORIOS = Notificador.CAMPOS_OBLIGATORIOS + [
        "correo_remitente",
        "correo_destinatario",
        "asunto"
    ]

    def validar_correo(self) -> bool:
        correo = self.datos.get("correo_destinatario", "")
        return "@" in correo and "." in correo

    def enviar(self) -> bool:
        if not self.validar_datos() or not self.validar_correo():
            return False

        print("Enviando Email :")
        print(self.mostrar_mensaje())
        return True

#Subclase intermedia: Notificador por Teléfono
class Notificador_Telefono(Notificador):
    CAMPOS_OBLIGATORIOS = Notificador.CAMPOS_OBLIGATORIOS + [
        "telefono_remitente",
        "telefono_destinatario"
    ]

    def validar_telefono(self) -> bool:
        for campo in ["telefono_remitente", "telefono_destinatario"]:
            if not isinstance(self.datos.get(campo), int):
                return False
        return True

    def enviar(self) -> bool:
        raise NotImplementedError("Debe ser implementado por WhatsApp o SMS")

#Subclase concreta: Notificador por WhatsApp
class Notificador_WhatsApp(Notificador_Telefono):
    def verificar_conexion(self) -> bool:
        return True  # Simulación de conexión

    def enviar(self) -> bool:
        if not self.validar_datos() or not self.validar_telefono():
            return False

        if not self.verificar_conexion():
            return False

        print("Enviando WhatsApp: ")
        print(self.mostrar_mensaje())
        return True

#Subclase concreta: Notificador por SMS
class Notificador_SMS(Notificador_Telefono):
    LIMITE_DEFECTO = 160

    def validar_longitud(self) -> bool:
        limite = self.datos.get("limite_caracteres", self.LIMITE_DEFECTO)
        return len(self.datos.get("texto_mensaje", "")) <= limite

    def enviar(self) -> bool:
        if not self.validar_datos() or not self.validar_telefono():
            return False

        if not self.validar_longitud():
            return False

        print("Enviando SMS: ")
        print(self.mostrar_mensaje())
        return True

datos_prueba = [
    {
        "tipo": "email",
        "nombre_remitente": "Ana",
        "nombre_destinatario": "Luis",
        "texto_mensaje": "Hola Luis, este es un correo de prueba.",
        "correo_remitente": "ana@mail.com",
        "correo_destinatario": "luis@mail.com",
        "asunto": "Saludo"
    },
    {
        "tipo": "whatsapp",
        "nombre_remitente": "Pedro",
        "nombre_destinatario": "María",
        "texto_mensaje": "Hola María, mensaje por WhatsApp.",
        "telefono_remitente": 123456789,
        "telefono_destinatario": 987654321,
        "usa_multimedia": False
    },
    {
        "tipo": "sms",
        "nombre_remitente": "Juan",
        "nombre_destinatario": "Carla",
        "texto_mensaje": "Hola Carla, mensaje SMS.",
        "telefono_remitente": 111222333,
        "telefono_destinatario": 444555666,
        "limite_caracteres": 160
    }
]

notificadores = []


for datos in datos_prueba:
    tipo = datos.pop("tipo")

    if tipo == "email":
        notificadores.append(Notificador_Email(**datos))

    elif tipo == "whatsapp":
        notificadores.append(Notificador_WhatsApp(**datos))

    elif tipo == "sms":
        notificadores.append(Notificador_SMS(**datos))

# Prueba de funcionalidad
for notificador in notificadores:
    resultado = notificador.enviar()
    print("Resultado:", resultado)
    print("-" * 40)