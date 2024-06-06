class Usuario:
    def __init__(self, nombre, apellido, correo, edad):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.edad = edad

    def mostrar_informacion(self):
        print("Información del Usuario:")
        print(f"Nombre: {self.nombre}")
        print(f"Apellido: {self.apellido}")
        print(f"Correo: {self.correo}")
        print(f"Edad: {self.edad}")

# Ejemplo de uso
usuario1 = Usuario("Juan", "Pérez", "juan@example.com", 30)
usuario1.mostrar_informacion()
