class DatosHistoricos:
    def __init__(self, no_matriculados, no_aprobados, no_reprobados, no_desertores):
        super().__init__(
            no_matriculados=no_matriculados,
            no_aprobados=no_aprobados,
            no_reprobados=no_reprobados,
            no_desertores=no_desertores,
        )

    def importar_datos(self):
        pass

    def exportar_datos(self):
        pass

    def get_no_matriculados(self):
        return self.no_matriculados

    def set_no_matriculados(self, no_matriculados):
        self.no_matriculados = no_matriculados

    def get_no_aprobados(self):
        return self.no_aprobados

    def set_no_aprobados(self, no_aprobados):
        self.no_aprobados = no_aprobados

    def get_no_reprobados(self):
        return self.no_reprobados

    def set_no_reprobados(self, no_reprobados):
        self.no_reprobados = no_reprobados

    def get_no_desertores(self):
        return self.no_desertores

    def set_no_desertores(self, no_desertores):
        self.no_desertores = no_desertores
