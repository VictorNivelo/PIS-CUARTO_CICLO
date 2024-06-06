class Secretaria:
    def __init__(self, nombre, apellido, dni, telefono, email):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.telefono = telefono
        self.email = email

    def mostrar_informacion(self):
        print(f"Nombre: {self.nombre} {self.apellido}")
        print(f"DNI: {self.dni}")
        print(f"Teléfono: {self.telefono}")
        print(f"Email: {self.email}")

# Ejemplo de uso
if __name__ == "__main__":
    # Crear una instancia de la clase Secretaria
    secretaria = Secretaria(nombre="María", apellido="González", dni="12345678A", telefono="987654321", email="maria@example.com")

    # Mostrar información de la secretaria
    secretaria.mostrar_informacion()
