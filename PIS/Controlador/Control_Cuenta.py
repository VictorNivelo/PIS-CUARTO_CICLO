from PIS.Modelo import Cuenta


class CuentaControlador:
    def __init__(self):
        self.cuentas = []

    def crear_cuenta(self, correo, contrasena):
        cuenta = Cuenta(correo, contrasena)
        self.cuentas.append(cuenta)
        return cuenta.crear_cuenta()

    def modificar_cuenta(self, correo, nuevo_correo=None, nueva_contrasena=None):
        for cuenta in self.cuentas:
            if cuenta.correo == correo:
                return cuenta.modificar_cuenta(nuevo_correo, nueva_contrasena)
        return "Cuenta no encontrada."

    def eliminar_cuenta(self, correo):
        for cuenta in self.cuentas:
            if cuenta.correo == correo:
                self.cuentas.remove(cuenta)
                return cuenta.eliminar_cuenta()
        return "Cuenta no encontrada."

    def buscar_cuenta(self, correo):
        for cuenta in self.cuentas:
            if cuenta.correo == correo:
                return f"Cuenta encontrada: Correo: {cuenta.correo}"
        return "Cuenta no encontrada."

    def recuperar_contrasena(self, correo):
        for cuenta in self.cuentas:
            if cuenta.correo == correo:
                return cuenta.recuperar_contrasena()
        return "Cuenta no encontrada."
