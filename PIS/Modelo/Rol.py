class Rol:
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def visualizar_informe(self, informe):
        return f"Informe '{informe}' visualizado por el rol '{self.nombre}'."

    def subir_informe_materia(self, informe):
        return f"Informe de materia '{informe}' subido por el rol '{self.nombre}'."

    def subir_informe_ciclo(self, informe):
        return f"Informe de ciclo '{informe}' subido por el rol '{self.nombre}'."

    def subir_informe_carrera(self, informe):
        return f"Informe de carrera '{informe}' subido por el rol '{self.nombre}'."

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_descripcion(self):
        return self.descripcion

    def set_descripcion(self, descripcion):
        self.descripcion = descripcion
