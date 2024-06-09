class FactoresPerdida:
    def __init__(self, id_estudiante, motivos_perdida=None, motivos_desercion=None):
        self.id_estudiante = id_estudiante
        self.motivos_perdida = motivos_perdida or []
        self.motivos_desercion = motivos_desercion or []
    
    def agregar_motivo_perdida(self, motivo):
        self.motivos_perdida.append(motivo)
    
    def agregar_motivo_desercion(self, motivo):
        self.motivos_desercion.append(motivo)
    
    def mostrar_factores(self):
        print(f"ID Estudiante: {self.id_estudiante}")
        print("Motivos de pérdida:")
        for motivo in self.motivos_perdida:
            print(f" - {motivo}")
        print("Motivos de deserción:")
        for motivo in self.motivos_desercion:
            print(f" - {motivo}")

# Ejemplo de uso
factores_estudiante = FactoresPerdida(id_estudiante="2024001")
factores_estudiante.agregar_motivo_perdida("Dificultades económicas")
factores_estudiante.agregar_motivo_desercion("Falta de interés en la carrera")

factores_estudiante.mostrar_factores()
