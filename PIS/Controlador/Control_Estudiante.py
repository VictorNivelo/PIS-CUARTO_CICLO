from PIS.Modelo import Estudiante


class EstudianteControlador:
    def __init__(self):
        self.estudiantes = []

    def agregar_estudiante(
        self, modalidad_estudio, tipo_educacion, origen, trabajo, discapacidad, hijos
    ):
        estudiante = Estudiante(
            modalidad_estudio, tipo_educacion, origen, trabajo, discapacidad, hijos
        )
        self.estudiantes.append(estudiante)
        return f"Estudiante '{origen}' agregado con éxito."

    def modificar_estudiante(
        self,
        index,
        nueva_modalidad_estudio=None,
        nuevo_tipo_educacion=None,
        nuevo_origen=None,
        nuevo_trabajo=None,
        nueva_discapacidad=None,
        nuevos_hijos=None,
    ):
        if 0 <= index < len(self.estudiantes):
            estudiante = self.estudiantes[index]
            estudiante.set_modalidad_estudio(
                nueva_modalidad_estudio
                if nueva_modalidad_estudio
                else estudiante.get_modalidad_estudio()
            )
            estudiante.set_tipo_educacion(
                nuevo_tipo_educacion
                if nuevo_tipo_educacion
                else estudiante.get_tipo_educacion()
            )
            estudiante.set_origen(
                nuevo_origen if nuevo_origen else estudiante.get_origen()
            )
            estudiante.set_trabajo(
                nuevo_trabajo if nuevo_trabajo else estudiante.get_trabajo()
            )
            estudiante.set_discapacidad(
                nueva_discapacidad
                if nueva_discapacidad
                else estudiante.get_discapacidad()
            )
            estudiante.set_hijos(
                nuevos_hijos if nuevos_hijos else estudiante.get_hijos()
            )
            return f"Estudiante '{estudiante.origen}' modificado con éxito."
        return "Índice fuera de rango."

    def eliminar_estudiante(self, index):
        if 0 <= index < len(self.estudiantes):
            self.estudiantes.pop(index)
            return f"Estudiante eliminado con éxito."
        return "Índice fuera de rango."

    def buscar_estudiante(self, index):
        if 0 <= index < len(self.estudiantes):
            estudiante = self.estudiantes[index]
            return f"Estudiante encontrado: Modalidad de Estudio: {estudiante.modalidad_estudio}, Tipo de Educación: {estudiante.tipo_educacion}, Origen: {estudiante.origen}, Trabajo: {estudiante.trabajo}, Discapacidad: {estudiante.discapacidad}, Hijos: {estudiante.hijos}"
        return "Índice fuera de rango."
