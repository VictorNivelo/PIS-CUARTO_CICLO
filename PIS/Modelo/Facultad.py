class Facultad:
    def __init__(self, nombre, fecha_fundacion):
        self.nombre = nombre
        self.fecha_fundacion = fecha_fundacion

    def crear_facultad(self):
        return f"Facultad '{self.nombre}' creada con éxito."

    def modificar_facultad(self, nombre=None, fecha_fundacion=None):
        if nombre:
            self.nombre = nombre
        if fecha_fundacion:
            self.fecha_fundacion = fecha_fundacion
        return f"Facultad '{self.nombre}' modificada con éxito."

    def eliminar_facultad(self):
        nombre = self.nombre
        self.nombre = None
        self.fecha_fundacion = None
        return f"Facultad '{nombre}' eliminada con éxito."

    def buscar_facultad(self, nombre):
        if self.nombre == nombre:
            return f"Facultad encontrada: {self.nombre}, Fecha de Fundación: {self.fecha_fundacion}"
        else:
            return "Facultad no encontrada."

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_fecha_fundacion(self):
        return self.fecha_fundacion

    def set_fecha_fundacion(self, fecha_fundacion):
        self.fecha_fundacion = fecha_fundacion
