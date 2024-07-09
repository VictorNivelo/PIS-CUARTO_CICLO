from PIS.Modelo import Prediccion


class PrediccionControlador:
    def __init__(self):
        self.predicciones = []

    def crear_prediccion(self, periodo_academico, fecha_creacion):
        prediccion = Prediccion(periodo_academico, fecha_creacion)
        self.predicciones.append(prediccion)
        return prediccion.generar_prediccion()

    def modificar_prediccion(
        self, periodo_academico, nuevo_periodo_academico=None, nueva_fecha_creacion=None
    ):
        for prediccion in self.predicciones:
            if prediccion.periodo_academico == periodo_academico:
                prediccion.set_periodo_academico(
                    nuevo_periodo_academico
                    if nuevo_periodo_academico
                    else prediccion.get_periodo_academico()
                )
                prediccion.set_fecha_creacion(
                    nueva_fecha_creacion
                    if nueva_fecha_creacion
                    else prediccion.get_fecha_creacion()
                )
                return f"Predicción del periodo académico '{prediccion.periodo_academico}' modificada con éxito."
        return "Predicción no encontrada."

    def eliminar_prediccion(self, periodo_academico):
        for prediccion in self.predicciones:
            if prediccion.periodo_academico == periodo_academico:
                self.predicciones.remove(prediccion)
                return prediccion.eliminar_prediccion()
        return "Predicción no encontrada."

    def buscar_prediccion(self, periodo_academico):
        for prediccion in self.predicciones:
            if prediccion.periodo_academico == periodo_academico:
                return f"Predicción encontrada: Periodo Académico: {prediccion.periodo_academico}, Fecha de Creación: {prediccion.fecha_creacion}"
        return "Predicción no encontrada."
