from PIS.Modelo import Materia


class MateriaControlador:
    def __init__(self):
        self.materias = []

    def crear_materia(self, nombre, num_horas):
        materia = Materia(nombre, num_horas)
        self.materias.append(materia)
        return materia.crear_materia()

    def modificar_materia(self, nombre, nuevo_nombre=None, nuevo_num_horas=None):
        for materia in self.materias:
            if materia.nombre == nombre:
                return materia.modificar_materia(nuevo_nombre, nuevo_num_horas)
        return "Materia no encontrada."

    def eliminar_materia(self, nombre):
        for materia in self.materias:
            if materia.nombre == nombre:
                self.materias.remove(materia)
                return materia.eliminar_materia()
        return "Materia no encontrada."

    def buscar_materia(self, nombre):
        for materia in self.materias:
            if materia.nombre == nombre:
                return materia.buscar_materia(nombre)
        return "Materia no encontrada."
