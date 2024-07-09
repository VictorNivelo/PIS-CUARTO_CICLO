class PeriodoAcademico:
    def __init__(self, codigo, fecha_inicio, fecha_fin, estado):
        self.codigo = codigo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado

    def crear_periodo(self):
        return f"Periodo académico '{self.codigo}' creado con éxito."

    def modificar_periodo(
        self, codigo=None, fecha_inicio=None, fecha_fin=None, estado=None
    ):
        if codigo:
            self.codigo = codigo
        if fecha_inicio:
            self.fecha_inicio = fecha_inicio
        if fecha_fin:
            self.fecha_fin = fecha_fin
        if estado:
            self.estado = estado
        return f"Periodo académico '{self.codigo}' modificado con éxito."

    def eliminar_periodo(self):
        codigo = self.codigo
        self.codigo = None
        self.fecha_inicio = None
        self.fecha_fin = None
        self.estado = None
        return f"Periodo académico '{codigo}' eliminado con éxito."

    def buscar_periodo(self, codigo):
        if self.codigo == codigo:
            return f"Periodo académico encontrado: {self.codigo}, Fecha de Inicio: {self.fecha_inicio}, Fecha de Fin: {self.fecha_fin}, Estado: {self.estado}"
        else:
            return "Periodo académico no encontrado."

    def get_codigo(self):
        return self.codigo

    def set_codigo(self, codigo):
        self.codigo = codigo

    def get_fecha_inicio(self):
        return self.fecha_inicio

    def set_fecha_inicio(self, fecha_inicio):
        self.fecha_inicio = fecha_inicio

    def get_fecha_fin(self):
        return self.fecha_fin

    def set_fecha_fin(self, fecha_fin):
        self.fecha_fin = fecha_fin

    def get_estado(self):
        return self.estado
