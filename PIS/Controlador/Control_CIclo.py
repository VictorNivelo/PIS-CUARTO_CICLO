from PIS.Modelo import Ciclo


class CicloControlador:
    def __init__(self):
        self.ciclos = []

    def crear_ciclo(self, nombre, numero, fecha_inicio, fecha_fin):
        ciclo = Ciclo(nombre, numero, fecha_inicio, fecha_fin)
        self.ciclos.append(ciclo)
        return ciclo.crear_ciclo()

    def modificar_ciclo(
        self,
        nombre,
        nuevo_nombre=None,
        nuevo_numero=None,
        nueva_fecha_inicio=None,
        nueva_fecha_fin=None,
    ):
        for ciclo in self.ciclos:
            if ciclo.nombre == nombre:
                return ciclo.modificar_ciclo(
                    nuevo_nombre, nuevo_numero, nueva_fecha_inicio, nueva_fecha_fin
                )
        return "Ciclo no encontrado."

    def eliminar_ciclo(self, nombre):
        for ciclo in self.ciclos:
            if ciclo.nombre == nombre:
                self.ciclos.remove(ciclo)
                return ciclo.eliminar_ciclo()
        return "Ciclo no encontrado."

    def buscar_ciclo(self, nombre):
        for ciclo in self.ciclos:
            if ciclo.nombre == nombre:
                return ciclo.buscar_ciclo(nombre)
        return "Ciclo no encontrado."
