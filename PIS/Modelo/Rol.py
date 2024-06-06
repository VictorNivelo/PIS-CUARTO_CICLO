class Rol:
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def mostrar_informacion(self):
        print(f"Nombre del rol: {self.nombre}")
        print(f"Descripción del rol: {self.descripcion}")

# Ejemplo de uso
if __name__ == "__main__":
    # Crear una instancia de la clase Rol
    rol_administrador = Rol(nombre="Administrador", descripcion="Tiene acceso completo al sistema y puede realizar cambios en la configuración.")

    # Mostrar información del rol
    rol_administrador.mostrar_informacion()
