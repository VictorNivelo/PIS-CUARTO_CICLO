class Carrera:
    def __init__(self, nombre, duracion):
        self.nombre = nombre
        self.duracion = duracion

    def crear_carrera(self):
        return f"Carrera '{self.nombre}' creada con éxito."

    def modificar_carrera(self, nombre=None, duracion=None):
        if nombre:
            self.nombre = nombre
        if duracion:
            self.duracion = duracion
        return f"Carrera '{self.nombre}' modificada con éxito."

    def eliminar_carrera(self):
        nombre = self.nombre
        self.nombre = None
        self.duracion = None
        return f"Carrera '{nombre}' eliminada con éxito."

    def buscar_carrera(self, nombre):
        if self.nombre == nombre:
            return f"Carrera encontrada: {self.nombre}, Duración: {self.duracion}"
        else:
            return "Carrera no encontrada."

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_duracion(self):
        return self.duracion

    def set_duracion(self, duracion):
        self.duracion = duracion
