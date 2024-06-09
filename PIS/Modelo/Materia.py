class Materia:
    def __init__(self, nombre, codigo, creditos, descripcion, prerrequisitos=None, profesor=None, horario=None):
        self.nombre = nombre
        self.codigo = codigo
        self.creditos = creditos
        self.descripcion = descripcion
        self.prerrequisitos = prerrequisitos or []
        self.profesor = profesor
        self.horario = horario
    
    def agregar_prerrequisito(self, prerrequisito):
        self.prerrequisitos.append(prerrequisito)
    
    def mostrar_informacion(self):
        info = f"""
        Nombre: {self.nombre}
        Código: {self.codigo}
        Créditos: {self.creditos}
        Descripción: {self.descripcion}
        Profesor: {self.profesor}
        Horario: {self.horario}
        Prerrequisitos: {', '.join(self.prerrequisitos)}
        """
        print(info)

# Ejemplo de uso
materia_ejemplo = Materia(
    nombre="Programación I",
    codigo="PROG101",
    creditos=4,
    descripcion="Introducción a la programación con Python",
    profesor="Dr. Juan Pérez",
    horario="Lunes y Miércoles de 8:00 a 10:00",
)
materia_ejemplo.agregar_prerrequisito("Introducción a la Informática")
materia_ejemplo.agregar_prerrequisito("Matemáticas Básicas")

materia_ejemplo.mostrar_informacion()
