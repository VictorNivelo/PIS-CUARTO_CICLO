from PIS.Modelo import Usuario


class UsuarioControlador:
    def __init__(self):
        self.usuarios = []

    def crear_usuario(
        self, tipo_dni, numero_dni, nombre, apellido, telefono, fecha_nacimiento, genero
    ):
        usuario = Usuario(
            tipo_dni, numero_dni, nombre, apellido, telefono, fecha_nacimiento, genero
        )
        self.usuarios.append(usuario)
        return f"Usuario '{nombre} {apellido}' creado con éxito."

    def modificar_usuario(
        self,
        numero_dni,
        nuevo_tipo_dni=None,
        nuevo_numero_dni=None,
        nuevo_nombre=None,
        nuevo_apellido=None,
        nuevo_telefono=None,
        nueva_fecha_nacimiento=None,
        nuevo_genero=None,
    ):
        for usuario in self.usuarios:
            if usuario.numero_dni == numero_dni:
                usuario.set_tipo_dni(
                    nuevo_tipo_dni if nuevo_tipo_dni else usuario.get_tipo_dni()
                )
                usuario.set_numero_dni(
                    nuevo_numero_dni if nuevo_numero_dni else usuario.get_numero_dni()
                )
                usuario.set_nombre(
                    nuevo_nombre if nuevo_nombre else usuario.get_nombre()
                )
                usuario.set_apellido(
                    nuevo_apellido if nuevo_apellido else usuario.get_apellido()
                )
                usuario.set_telefono(
                    nuevo_telefono if nuevo_telefono else usuario.get_telefono()
                )
                usuario.set_fecha_nacimiento(
                    nueva_fecha_nacimiento
                    if nueva_fecha_nacimiento
                    else usuario.get_fecha_nacimiento()
                )
                usuario.set_genero(
                    nuevo_genero if nuevo_genero else usuario.get_genero()
                )
                return f"Usuario '{usuario.nombre} {usuario.apellido}' modificado con éxito."
        return "Usuario no encontrado."

    def eliminar_usuario(self, numero_dni):
        for usuario in self.usuarios:
            if usuario.numero_dni == numero_dni:
                self.usuarios.remove(usuario)
                return f"Usuario con DNI '{numero_dni}' eliminado con éxito."
        return "Usuario no encontrado."

    def buscar_usuario(self, numero_dni):
        for usuario in self.usuarios:
            if usuario.numero_dni == numero_dni:
                return f"Usuario encontrado: {usuario.nombre} {usuario.apellido}, DNI: {usuario.numero_dni}, Teléfono: {usuario.telefono}, Fecha de Nacimiento: {usuario.fecha_nacimiento}, Género: {usuario.genero}"
        return "Usuario no encontrado."
