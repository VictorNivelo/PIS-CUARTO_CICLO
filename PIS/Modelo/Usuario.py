class Usuario:
    def __init__(
        self, tipo_dni, numero_dni, nombre, apellido, telefono, fecha_nacimiento, genero, cuenta
    ):
        self.tipo_dni = tipo_dni
        self.numero_dni = numero_dni
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero
        self.cuenta = cuenta

    def subir_informe(self, informe):
        return f"Informe '{informe}' subido con éxito por el usuario {self.nombre} {self.apellido}."

    def get_tipo_dni(self):
        return self.tipo_dni

    def set_tipo_dni(self, tipo_dni):
        self.tipo_dni = tipo_dni

    def get_numero_dni(self):
        return self.numero_dni

    def set_numero_dni(self, numero_dni):
        self.numero_dni = numero_dni

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_apellido(self):
        return self.apellido

    def set_apellido(self, apellido):
        self.apellido = apellido

    def get_telefono(self):
        return self.telefono

    def set_telefono(self, telefono):
        self.telefono = telefono

    def get_fecha_nacimiento(self):
        return self.fecha_nacimiento

    def set_fecha_nacimiento(self, fecha_nacimiento):
        self.fecha_nacimiento = fecha_nacimiento

    def get_genero(self):
        return self.genero

    def set_genero(self, genero):
        self.genero = genero
