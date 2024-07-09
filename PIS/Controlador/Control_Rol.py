from PIS.Modelo import Rol


class RolControlador:
    def __init__(self):
        self.roles = []

    def crear_rol(self, nombre, descripcion):
        rol = Rol(nombre, descripcion)
        self.roles.append(rol)
        return f"Rol '{nombre}' creado con éxito."

    def modificar_rol(self, nombre, nuevo_nombre=None, nueva_descripcion=None):
        for rol in self.roles:
            if rol.nombre == nombre:
                rol.set_nombre(nuevo_nombre if nuevo_nombre else rol.get_nombre())
                rol.set_descripcion(nueva_descripcion if nueva_descripcion else rol.get_descripcion())
                return f"Rol '{rol.nombre}' modificado con éxito."
        return "Rol no encontrado."

    def eliminar_rol(self, nombre):
        for rol in self.roles:
            if rol.nombre == nombre:
                self.roles.remove(rol)
                return f"Rol '{nombre}' eliminado con éxito."
        return "Rol no encontrado."

    def buscar_rol(self, nombre):
        for rol in self.roles:
            if rol.nombre == nombre:
                return f"Rol encontrado: Nombre: {rol.nombre}, Descripción: {rol.descripcion}"
        return "Rol no encontrado."
