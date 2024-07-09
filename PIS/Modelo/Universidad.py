class Universidad:
    def __init__(self, nombre, direccion, telefono, fecha_fundacion, correo):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.fecha_fundacion = fecha_fundacion
        self.correo = correo

    def crear_universidad(self):
        return f"Universidad '{self.nombre}' creada con éxito."

    def modificar_universidad(
        self,
        nombre=None,
        direccion=None,
        telefono=None,
        fecha_fundacion=None,
        correo=None,
    ):
        if nombre:
            self.nombre = nombre
        if direccion:
            self.direccion = direccion
        if telefono:
            self.telefono = telefono
        if fecha_fundacion:
            self.fecha_fundacion = fecha_fundacion
        if correo:
            self.correo = correo
        return f"Universidad '{self.nombre}' modificada con éxito."

    def eliminar_universidad(self):
        nombre = self.nombre
        self.nombre = None
        self.direccion = None
        self.telefono = None
        self.fecha_fundacion = None
        self.correo = None
        return f"Universidad '{nombre}' eliminada con éxito."

    def buscar_universidad(self, nombre):
        if self.nombre == nombre:
            return f"Universidad encontrada: {self.nombre}, Dirección: {self.direccion}, Teléfono: {self.telefono}, Fecha de Fundación: {self.fecha_fundacion}, Correo: {self.correo}"
        else:
            return "Universidad no encontrada."

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_direccion(self):
        return self.direccion

    def set_direccion(self, direccion):
        self.direccion = direccion

    def get_telefono(self):
        return self.telefono

    def set_telefono(self, telefono):
        self.telefono = telefono

    def get_fecha_fundacion(self):
        return self.fecha_fundacion

    def set_fecha_fundacion(self, fecha_fundacion):
        self.fecha_fundacion = fecha_fundacion

    def get_correo(self):
        return self.correo

    def set_correo(self, correo):
        self.correo = correo
