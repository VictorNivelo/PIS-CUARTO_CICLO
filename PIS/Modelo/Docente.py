class Estudiante:
    def __init__(self, nombre_completo, id_estudiante, carrera, ciclo_actual, creditos_acumulados, promedio_acumulado, fecha_ingreso):
        self.nombre_completo = nombre_completo
        self.id_estudiante = id_estudiante
        self.carrera = carrera
        self.ciclo_actual = ciclo_actual
        self.creditos_acumulados = creditos_acumulados
        self.promedio_acumulado = promedio_acumulado
        self.fecha_ingreso = fecha_ingreso
    
    def mostrar_informacion(self):
        info = f"""
        Nombre completo: {self.nombre_completo}
        ID Estudiante: {self.id_estudiante}
        Carrera: {self.carrera}
        Ciclo Actual: {self.ciclo_actual}
        Créditos acumulados: {self.creditos_acumulados}
        Promedio acumulado: {self.promedio_acumulado}
        Fecha de ingreso: {self.fecha_ingreso}
        """
        print(info)

# Ejemplo de uso para un estudiante
estudiante_ejemplo = Estudiante(
    nombre_completo="Juan Pérez",
    id_estudiante="2024001",
    carrera="Ingeniería en Sistemas",
    ciclo_actual=5,
    creditos_acumulados=150,
    promedio_acumulado=8.5,
    fecha_ingreso="01-09-2020"
)

estudiante_ejemplo.mostrar_informacion()
