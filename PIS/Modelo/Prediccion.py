
class Predicciones:
    def __init__(self, modelo):
        self.modelo = modelo
        self.predicciones = []

    def predecir(self, datos):
        self.predicciones = self.modelo.predict(datos)
        return self.predicciones

    def obtener_predicciones(self):
        return self.predicciones

    def obtener_modelo(self):
        return self.modelo


# if __name__ == "__main__":
#     # Crear un nuevo modelo de predicción
#     modelo = RandomForestClassifier()
#     predicciones = Predicciones(modelo)

#     # Crear datos de prueba
#     datos = [[5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2], [6.2, 2.9, 4.3, 1.3]]

#     # Realizar predicciones
#     predicciones.predecir(datos)

#     # Obtener las predicciones
#     print(predicciones.obtener_predicciones())

#     # Obtener el modelo utilizado
#     print(predicciones.obtener_modelo())
