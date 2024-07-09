from PIS.Modelo import Universidad


class UniversidadControlador:
    def __init__(self):
        self.universidades = []

    def crear_universidad(self, nombre, direccion, telefono, fecha_fundacion, correo):
        universidad = Universidad(nombre, direccion, telefono, fecha_fundacion, correo)
        self.universidades.append(universidad)
        return universidad.crear_universidad()

    def modificar_universidad(
        self,
        nombre,
        nuevo_nombre=None,
        nueva_direccion=None,
        nuevo_telefono=None,
        nueva_fecha_fundacion=None,
        nuevo_correo=None,
    ):
        for universidad in self.universidades:
            if universidad.nombre == nombre:
                return universidad.modificar_universidad(
                    nuevo_nombre,
                    nueva_direccion,
                    nuevo_telefono,
                    nueva_fecha_fundacion,
                    nuevo_correo,
                )
        return "Universidad no encontrada."

    def eliminar_universidad(self, nombre):
        for universidad in self.universidades:
            if universidad.nombre == nombre:
                self.universidades.remove(universidad)
                return universidad.eliminar_universidad()
        return "Universidad no encontrada."

    def buscar_universidad(self, nombre):
        for universidad in self.universidades:
            if universidad.nombre == nombre:
                return universidad.buscar_universidad(nombre)
        return "Universidad no encontrada."
