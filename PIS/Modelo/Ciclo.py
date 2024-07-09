class Ciclo:
    def __init__(self, nombre, numero, fecha_inicio, fecha_fin):
        self.nombre = nombre
        self.numero = numero
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def crear_ciclo(self):
        return f"Ciclo '{self.nombre}' creado con éxito."

    def modificar_ciclo(
        self, nombre=None, numero=None, fecha_inicio=None, fecha_fin=None
    ):
        if nombre:
            self.nombre = nombre
        if numero:
            self.numero = numero
        if fecha_inicio:
            self.fecha_inicio = fecha_inicio
        if fecha_fin:
            self.fecha_fin = fecha_fin
        return f"Ciclo '{self.nombre}' modificado con éxito."

    def eliminar_ciclo(self):
        nombre = self.nombre
        self.nombre = None
        self.numero = None
        self.fecha_inicio = None
        self.fecha_fin = None
        return f"Ciclo '{nombre}' eliminado con éxito."

    def buscar_ciclo(self, nombre):
        if self.nombre == nombre:
            return f"Ciclo encontrado: {self.nombre}, Número: {self.numero}, Fecha de Inicio: {self.fecha_inicio}, Fecha de Fin: {self.fecha_fin}"
        else:
            return "Ciclo no encontrado."

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_numero(self):
        return self.numero

    def set_numero(self, numero):
        self.numero = numero

    def get_fecha_inicio(self):
        return self.fecha_inicio

    def set_fecha_inicio(self, fecha_inicio):
        self.fecha_inicio = fecha_inicio

    def get_fecha_fin(self):
        return self.fecha_fin

    def set_fecha_fin(self, fecha_fin):
        self.fecha_fin = fecha_fin
