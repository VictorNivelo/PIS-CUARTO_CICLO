class Carrera:
    def __init__(self, nombre, codigo, duracion, facultad, plan_estudios, creditos_totales, titulo, modalidad, costo, requisitos_ingreso, descripcion, url):
        self.nombre = nombre
        self.codigo = codigo
        self.duracion = duracion
        self.facultad = facultad
        self.plan_estudios = plan_estudios
        self.creditos_totales = creditos_totales
        self.titulo = titulo
        self.modalidad = modalidad
        self.costo = costo
        self.requisitos_ingreso = requisitos_ingreso
        self.descripcion = descripcion
        self.url = url
    
    def mostrar_informacion(self):
        info = f"""
        Nombre de la carrera: {self.nombre}
        Código: {self.codigo}
        Duración: {self.duracion} años
        Facultad: {self.facultad}
        Créditos Totales: {self.creditos_totales}
        Título: {self.titulo}
        Modalidad: {self.modalidad}
        Costo: {self.costo}
        Requisitos de Ingreso: {self.requisitos_ingreso}
        Descripción: {self.descripcion}
        URL: {self.url}
        """
        print(info)

# Ejemplo de uso para la carrera de Ingeniería Electromecánica
plan_estudios_electromecanica = [
    "Matemáticas I", "Física I", "Circuitos Eléctricos I", "Mecánica I", 
    "Electrónica I", "Termodinámica", "Máquinas Eléctricas", 
    "Sistemas de Control", "Automatización Industrial"
]
requisitos_ingreso_electromecanica = ["Certificado de bachillerato", "Examen de admisión"]

carrera_electromecanica = Carrera(
    nombre="Ingeniería Electromecánica",
    codigo="EM2024",
    duracion=5,
    facultad="Facultad de Ingeniería",
    plan_estudios=plan_estudios_electromecanica,
    creditos_totales=250,
    titulo="Ingeniero Electromecánico",
    modalidad="Presencial",
    costo=60000,
    requisitos_ingreso=requisitos_ingreso_electromecanica,
    descripcion="Formación de profesionales en el diseño, desarrollo y mantenimiento de sistemas electromecánicos.",
    url="http://www.universidad.edu/programas/ingenieria_electromecanica"
)

carrera_electromecanica.mostrar_informacion()
