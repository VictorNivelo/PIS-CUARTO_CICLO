class Prediccion:
    def __init__(self, periodo_academico, fecha_creacion):
        self.periodo_academico = periodo_academico
        self.fecha_creacion = fecha_creacion

    def generar_prediccion(self):
        return (
            f"Predicción generada para el periodo académico '{self.periodo_academico}'."
        )

    def guardar_prediccion(self):
        return (
            f"Predicción guardada para el periodo académico '{self.periodo_academico}'."
        )

    def eliminar_prediccion(self):
        periodo_academico = self.periodo_academico
        self.periodo_academico = None
        self.fecha_creacion = None
        return f"Predicción del periodo académico '{periodo_academico}' eliminada."

    def generar_informe(self):
        return f"Informe generado para la predicción del periodo académico '{self.periodo_academico}'."

    def get_periodo_academico(self):
        return self.periodo_academico

    def set_periodo_academico(self, periodo_academico):
        self.periodo_academico = periodo_academico

    def get_fecha_creacion(self):
        return self.fecha_creacion

    def set_fecha_creacion(self, fecha_creacion):
        self.fecha_creacion = fecha_creacion
