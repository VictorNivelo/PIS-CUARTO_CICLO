class Cuenta:
    def __init__(self, correo, contrasena):
        self.correo = correo
        self.contrasena = contrasena

    def iniciar_sesion(self):
        return f"Sesión iniciada para el correo '{self.correo}'."

    def cerrar_sesion(self):
        return f"Sesión cerrada para el correo '{self.correo}'."

    def crear_cuenta(self):
        return f"Cuenta con correo '{self.correo}' creada con éxito."

    def modificar_cuenta(self, correo=None, contrasena=None):
        if correo:
            self.correo = correo
        if contrasena:
            self.contrasena = contrasena
        return f"Cuenta con correo '{self.correo}' modificada con éxito."

    def eliminar_cuenta(self):
        correo = self.correo
        self.correo = None
        self.contrasena = None
        return f"Cuenta con correo '{correo}' eliminada con éxito."

    def recuperar_contrasena(self):
        return f"Contraseña para el correo '{self.correo}' recuperada."

    def subir_imagen_perfil(self, imagen):
        return f"Imagen de perfil '{imagen}' subida para la cuenta '{self.correo}'."

    def get_correo(self):
        return self.correo

    def set_correo(self, correo):
        self.correo = correo

    def get_contrasena(self):
        return self.contrasena

    def set_contrasena(self, contrasena):
        self.contrasena = contrasena
