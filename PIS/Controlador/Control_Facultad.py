from PIS.Modelo import Facultad


class FacultadControlador:
    def __init__(self):
        self.facultades = []

    def crear_facultad(self, nombre, fecha_fundacion):
        facultad = Facultad(nombre, fecha_fundacion)
        self.facultades.append(facultad)
        return facultad.crear_facultad()

    def modificar_facultad(self, nombre, nuevo_nombre=None, nueva_fecha_fundacion=None):
        for facultad in self.facultades:
            if facultad.nombre == nombre:
                return facultad.modificar_facultad(nuevo_nombre, nueva_fecha_fundacion)
        return "Facultad no encontrada."

    def eliminar_facultad(self, nombre):
        for facultad in self.facultades:
            if facultad.nombre == nombre:
                self.facultades.remove(facultad)
                return facultad.eliminar_facultad()
        return "Facultad no encontrada."

    def buscar_facultad(self, nombre):
        for facultad in self.facultades:
            if facultad.nombre == nombre:
                return facultad.buscar_facultad(nombre)
        return "Facultad no encontrada."
