class InformeAcademico:
    def __init__(self, id_estudiante, ciclo_academico, asignaturas_aprobadas=None, asignaturas_reprobadas=None, promedio_ciclo=None):
        self.id_estudiante = id_estudiante
        self.ciclo_academico = ciclo_academico
        self.asignaturas_aprobadas = asignaturas_aprobadas or []
        self.asignaturas_reprobadas = asignaturas_reprobadas or []
        self.promedio_ciclo = promedio_ciclo
    
    def agregar_asignatura_aprobada(self, asignatura):
        self.asignaturas_aprobadas.append(asignatura)
    
    def agregar_asignatura_reprobada(self, asignatura):
        self.asignaturas_reprobadas.append(asignatura)
    
    def calcular_promedio_ciclo(self):
        if self.asignaturas_aprobadas:
            total_calificaciones = sum(self.asignaturas_aprobadas)
            self.promedio_ciclo = total_calificaciones / len(self.asignaturas_aprobadas)
        else:
            self.promedio_ciclo = 0.0
    
    def mostrar_informe(self):
        print(f"Informe Académico - Ciclo {self.ciclo_academico}")
        print(f"ID Estudiante: {self.id_estudiante}")
        print("Asignaturas Aprobadas:")
        for asignatura in self.asignaturas_aprobadas:
            print(f" - {asignatura}")
        print("Asignaturas Reprobadas:")
        for asignatura in self.asignaturas_reprobadas:
            print(f" - {asignatura}")
        if self.promedio_ciclo is not None:
            print(f"Promedio del Ciclo: {self.promedio_ciclo}")

# Ejemplo de uso
informe_estudiante = InformeAcademico(id_estudiante="2024001", ciclo_academico=1)
informe_estudiante.agregar_asignatura_aprobada("Matemáticas I")
informe_estudiante.agregar_asignatura_aprobada("Física I")
informe_estudiante.agregar_asignatura_reprobada("Programación I")
informe_estudiante.calcular_promedio_ciclo()

informe_estudiante.mostrar_informe()
