from PIS.Modelo import DatosHistoricos


class DatosHistoricosController:
    def __init__(self):
        self.datos_historicos = []

    def agregar_datos_historicos(
        self, no_matriculados, no_aprobados, no_reprobados, no_desertores
    ):
        datos_historicos = DatosHistoricos(
            no_matriculados, no_aprobados, no_reprobados, no_desertores
        )
        self.datos_historicos.append(datos_historicos)
        return f"Datos históricos agregados con éxito."

    def modificar_datos_historicos(
        self,
        index,
        nuevo_no_matriculados=None,
        nuevo_no_aprobados=None,
        nuevo_no_reprobados=None,
        nuevo_no_desertores=None,
    ):
        if 0 <= index < len(self.datos_historicos):
            datos_historicos = self.datos_historicos[index]
            datos_historicos.set_no_matriculados(
                nuevo_no_matriculados
                if nuevo_no_matriculados
                else datos_historicos.get_no_matriculados()
            )
            datos_historicos.set_no_aprobados(
                nuevo_no_aprobados
                if nuevo_no_aprobados
                else datos_historicos.get_no_aprobados()
            )
            datos_historicos.set_no_reprobados(
                nuevo_no_reprobados
                if nuevo_no_reprobados
                else datos_historicos.get_no_reprobados()
            )
            datos_historicos.set_no_desertores(
                nuevo_no_desertores
                if nuevo_no_desertores
                else datos_historicos.get_no_desertores()
            )
            return f"Datos históricos modificados con éxito."
        return "Índice fuera de rango."

    def eliminar_datos_historicos(self, index):
        if 0 <= index < len(self.datos_historicos):
            self.datos_historicos.pop(index)
            return f"Datos históricos eliminados con éxito."
        return "Índice fuera de rango."

    def buscar_datos_historicos(self, index):
        if 0 <= index < len(self.datos_historicos):
            datos_historicos = self.datos_historicos[index]
            return f"Datos históricos encontrados: No. Matriculados: {datos_historicos.no_matriculados}, No. Aprobados: {datos_historicos.no_aprobados}, No. Reprobados: {datos_historicos.no_reprobados}, No. Desertores: {datos_historicos.no_desertores}"
        return "Índice fuera de rango."

    def importar_datos(self, index):
        if 0 <= index < len(self.datos_historicos):
            return self.datos_historicos[index].importar_datos()
        return "Índice fuera de rango."

    def exportar_datos(self, index):
        if 0 <= index < len(self.datos_historicos):
            return self.datos_historicos[index].exportar_datos()
        return "Índice fuera de rango."
