class Estudiante:
    def __init__(
        self, modalidad_estudio, tipo_educacion, origen, trabajo, discapacidad, hijos
    ):
        super().__init__(
            modalidad_estudio=modalidad_estudio,
            tipo_educacion=tipo_educacion,
            origen=origen,
            trabajo=trabajo,
            discapacidad=discapacidad,
            hijos=hijos,
        )

    def get_modalidad_estudio(self):
        return self.modalidad_estudio

    def set_modalidad_estudio(self, modalidad_estudio):
        self.modalidad_estudio = modalidad_estudio

    def get_tipo_educacion(self):
        return self.tipo_educacion

    def set_tipo_educacion(self, tipo_educacion):
        self.tipo_educacion = tipo_educacion

    def get_origen(self):
        return self.origen

    def set_origen(self, origen):
        self.origen = origen

    def get_trabajo(self):
        return self.trabajo

    def set_trabajo(self, trabajo):
        self.trabajo = trabajo

    def get_discapacidad(self):
        return self.discapacidad

    def set_discapacidad(self, discapacidad):
        self.discapacidad = discapacidad

    def get_hijos(self):
        return self.hijos

    def set_hijos(self, hijos):
        self.hijos = hijos
