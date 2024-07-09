class Materia:
    def __init__(self, nombre, num_horas):
        self.nombre = nombre
        self.num_horas = num_horas

    def crear_materia(self):
        return f"Materia '{self.nombre}' creada con éxito."

    def modificar_materia(self, nombre=None, num_horas=None):
        if nombre:
            self.nombre = nombre
        if num_horas:
            self.num_horas = num_horas
        return f"Materia '{self.nombre}' modificada con éxito."

    def eliminar_materia(self):
        nombre = self.nombre
        self.nombre = None
        self.num_horas = None
        return f"Materia '{nombre}' eliminada con éxito."

    def buscar_materia(self, nombre):
        if self.nombre == nombre:
            return (
                f"Materia encontrada: {self.nombre}, Número de Horas: {self.num_horas}"
            )
        else:
            return "Materia no encontrada."

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_num_horas(self):
        return self.num_horas

    def set_num_horas(self, num_horas):
        self.num_horas = num_horas
