from PIS.Modelo import PeriodoAcademico


class PeriodoAcademicoControlador:
    def __init__(self):
        self.periodos_academicos = []

    def crear_periodo(self, codigo, fecha_inicio, fecha_fin, estado):
        periodo = PeriodoAcademico(codigo, fecha_inicio, fecha_fin, estado)
        self.periodos_academicos.append(periodo)
        return periodo.crear_periodo()

    def modificar_periodo(
        self,
        codigo,
        nuevo_codigo=None,
        nueva_fecha_inicio=None,
        nueva_fecha_fin=None,
        nuevo_estado=None,
    ):
        for periodo in self.periodos_academicos:
            if periodo.codigo == codigo:
                return periodo.modificar_periodo(
                    nuevo_codigo, nueva_fecha_inicio, nueva_fecha_fin, nuevo_estado
                )
        return "Periodo académico no encontrado."

    def eliminar_periodo(self, codigo):
        for periodo in self.periodos_academicos:
            if periodo.codigo == codigo:
                self.periodos_academicos.remove(periodo)
                return periodo.eliminar_periodo()
        return "Periodo académico no encontrado."

    def buscar_periodo(self, codigo):
        for periodo in self.periodos_academicos:
            if periodo.codigo == codigo:
                return periodo.buscar_periodo(codigo)
        return "Periodo académico no encontrado."
