class Reporte:
    def __init__(self, titulo):
        self.titulo = titulo
        self.contenido = []

    def agregar_parrafo(self, parrafo):
        self.contenido.append(parrafo)

    def generar_reporte(self):
        print(f"--- {self.titulo} ---")
        for parrafo in self.contenido:
            print(parrafo)
        print("--------------------")

# Ejemplo de uso
if __name__ == "__main__":
    # Crear un nuevo reporte
    reporte = Reporte("Informe Mensual")

    # Agregar párrafos al reporte
    reporte.agregar_parrafo("En este informe se presenta el resumen mensual de actividades.")
    reporte.agregar_parrafo("Se detallan los ingresos y gastos del mes.")
    reporte.agregar_parrafo("Se incluyen también proyecciones para el próximo trimestre.")

    # Generar el reporte
    reporte.generar_reporte()
