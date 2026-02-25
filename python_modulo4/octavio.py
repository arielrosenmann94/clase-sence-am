class ParticipanteSalaOnline:
    campos = ["nombre", "edad", "rut"]

    def __init__(self, **kwargs):
        for campo in self.campos:
            setattr(self, campo, kwargs.get(campo))

    def marcar_presente(self):
        print(f"{self.nombre} ha marcado presente")

    def escribir_chat(self, mensaje):
        print(f"{self.nombre} escribe en el chat: {mensaje}")

    def hablar_sala_virtual(self):
        print(f"{self.nombre} está hablando en la sala virtual")


class Estudiante(ParticipanteSalaOnline):
    campos = ParticipanteSalaOnline.campos + ["carrera", "asignatura"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Profesor(ParticipanteSalaOnline):
    campos = ParticipanteSalaOnline.campos + ["asignatura_dicta"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        