from PIS.Modelo import Carrera


class CarreraControlador:
    def __init__(self):
        self.carreras = []

    def crear_carrera(self, nombre, duracion):
        carrera = Carrera(nombre, duracion)
        self.carreras.append(carrera)
        return carrera.crear_carrera()

    def modificar_carrera(self, nombre, nuevo_nombre=None, nueva_duracion=None):
        for carrera in self.carreras:
            if carrera.nombre == nombre:
                return carrera.modificar_carrera(nuevo_nombre, nueva_duracion)
        return "Carrera no encontrada."

    def eliminar_carrera(self, nombre):
        for carrera in self.carreras:
            if carrera.nombre == nombre:
                self.carreras.remove(carrera)
                return carrera.eliminar_carrera()
        return "Carrera no encontrada."

    def buscar_carrera(self, nombre):
        for carrera in self.carreras:
            if carrera.nombre == nombre:
                return carrera.buscar_carrera(nombre)
        return "Carrera no encontrada."
