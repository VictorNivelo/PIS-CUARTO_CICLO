class Cuenta:
    def __init__(self, id, nombre, email, tipo, estado='activo'):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.tipo = tipo
        self.estado = estado

    def actualizar_email(self, nuevo_email):
        self.email = nuevo_email
        print(f"Email actualizado a: {self.email}")

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        print(f"Estado actualizado a: {self.estado}")

    def mostrar_informacion(self):
        print(f"ID: {self.id}")
        print(f"Nombre: {self.nombre}")
        print(f"Email: {self.email}")
        print(f"Tipo: {self.tipo}")
        print(f"Estado: {self.estado}")

# Ejemplo de uso
if __name__ == "__main__":
    # Crear una nueva cuenta de estudiante
    cuenta_estudiante = Cuenta(id="2024001", nombre="Ana López", email="ana.lopez@example.com", tipo="estudiante")

    # Mostrar información de la cuenta
    cuenta_estudiante.mostrar_informacion()

    # Actualizar el email de la cuenta
    cuenta_estudiante.actualizar_email("ana.lopez123@example.com")

    # Actualizar el estado de la cuenta
    cuenta_estudiante.actualizar_estado("inactivo")

    # Mostrar información de la cuenta nuevamente
    cuenta_estudiante.mostrar_informacion()
