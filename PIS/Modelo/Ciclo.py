class Ciclo:
    def __init__(self, numero_ciclo, anio_academico, asignaturas, fecha_inicio, fecha_fin, horario, profesorado):
        self.numero_ciclo = numero_ciclo
        self.anio_academico = anio_academico
        self.asignaturas = asignaturas
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.horario = horario
        self.profesorado = profesorado

    def mostrar_informacion(self):
        info = f"""
        Número de Ciclo: {self.numero_ciclo}
        Año Académico: {self.anio_academico}
        Fecha de Inicio: {self.fecha_inicio}
        Fecha de Fin: {self.fecha_fin}
        Horario: {self.horario}
        Profesorado: {', '.join(self.profesorado)}
        Asignaturas:
        """
        for asignatura in self.asignaturas:
            info += f"    - {asignatura}\n"
        print(info)

# Ejemplo de uso para un ciclo académico
asignaturas_ciclo1 = ["Matemáticas I", "Física I", "Introducción a la Programación", "Álgebra"]
profesorado_ciclo1 = ["Dr. Juan Pérez", "Ing. María García", "Dr. Ana López"]

ciclo1 = Ciclo(
    numero_ciclo=1,
    anio_academico=2024,
    asignaturas=asignaturas_ciclo1,
    fecha_inicio="01-02-2024",
    fecha_fin="30-06-2024",
    horario="Lunes a Viernes de 8:00 a 14:00",
    profesorado=profesorado_ciclo1
)

ciclo1.mostrar_informacion()
