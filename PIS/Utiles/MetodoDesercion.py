import sqlite3


def get_datos_historicos(facultad, carrera, ciclo, materia, periodo):
    conn = sqlite3.connect("db.sqlite3.db")
    cursor = conn.cursor()

    query = """
    SELECT numero_estudiantes, porcentaje_reprobados, porcentaje_desertores, unidades
    FROM DatosHistoricos
    WHERE facultad = ? AND carrera = ? AND ciclo = ? AND materia = ? AND periodo = ?
    """
    cursor.execute(query, (facultad, carrera, ciclo, materia, periodo))
    result = cursor.fetchone()
    conn.close()

    if result:
        numero_estudiantes, porcentaje_reprobados, porcentaje_desertores, unidades = (
            result
        )
        return (
            numero_estudiantes,
            porcentaje_reprobados,
            porcentaje_desertores,
            unidades,
        )
    else:
        raise ValueError("No se encontraron datos para los criterios especificados.")


def desertores_runge_kutta(reprobados_inicial, t0, t_final, h, alpha, beta):
    desertores_lista = []
    reprobados = reprobados_inicial
    t = t0

    while t < t_final:
        desertores_lista.append(int(reprobados * (1 - beta)))

        k1 = h * (-alpha * reprobados)
        k2 = h * (-alpha * (reprobados + k1 / 2))
        k3 = h * (-alpha * (reprobados + k2 / 2))
        k4 = h * (-alpha * (reprobados + k3))

        reprobados = reprobados + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t = t + h

    return desertores_lista


def simular_ciclos(
    numero_estudiantes, porcentaje_reprobados, porcentaje_desertores, periodos, unidades
):
    estudiantes = [numero_estudiantes]
    reprobados_lista = []
    desertores_lista = []
    aprobados_lista = []

    for periodo in range(periodos):
        reprobados = int(estudiantes[-1] * porcentaje_reprobados)
        desertores = desertores_runge_kutta(
            reprobados, 0, unidades, 0.1, porcentaje_reprobados, porcentaje_desertores
        )[-1]
        aprobados = estudiantes[-1] - reprobados
        estudiantes.append(estudiantes[-1] - desertores)
        reprobados_lista.append(reprobados)
        desertores_lista.append(desertores)
        aprobados_lista.append(aprobados)

    return estudiantes, reprobados_lista, desertores_lista, aprobados_lista


# import sqlite3
# import numpy as np


# def get_datos_from_db(facultad, carrera, ciclo, materia, periodo):
#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()

#     query = """
#     SELECT e.numero_estudiantes, m.unidades
#     FROM Estudiantes e
#     JOIN Materia m ON e.materia_id = m.id
#     JOIN Ciclo c ON m.ciclo_id = c.id
#     JOIN Carrera ca ON c.carrera_id = ca.id
#     JOIN Facultad f ON ca.facultad_id = f.id
#     JOIN Periodo_Academico p ON e.periodo_academico_id = p.id
#     WHERE m.nombre = ? AND c.nombre = ? AND ca.nombre = ? AND f.nombre = ? AND p.nombre = ?
#     """
#     cursor.execute(query, (materia, ciclo, carrera, facultad, periodo))
#     result = cursor.fetchone()
#     conn.close()

#     if result:
#         numero_estudiantes, unidades = result
#         return numero_estudiantes, unidades
#     else:
#         raise ValueError("No se encontraron datos para los criterios especificados.")


# def desertores_runge_kutta(reprobados_inicial, t0, t_final, h, alpha, beta):
#     desertores_lista = []
#     reprobados = reprobados_inicial
#     t = t0

#     while t < t_final:
#         desertores_lista.append(int(reprobados * (1 - beta)))

#         k1 = h * (-alpha * reprobados)
#         k2 = h * (-alpha * (reprobados + k1 / 2))
#         k3 = h * (-alpha * (reprobados + k2 / 2))
#         k4 = h * (-alpha * (reprobados + k3))

#         reprobados = reprobados + (k1 + 2 * k2 + 2 * k3 + k4) / 6
#         t = t + h

#     return desertores_lista


# def simular_ciclos(estudiantes_inicial, periodos, unidades, alpha, beta, gamma):
#     estudiantes = [estudiantes_inicial]
#     nuevos_ingresos_lista = []
#     desertores_lista = []
#     reprobados_lista = []
#     aprobados_lista = []

#     for periodo in range(periodos):
#         nuevos_ingresos = int(estudiantes[-1] * gamma)
#         estudiantes.append(estudiantes[-1] + nuevos_ingresos)
#         nuevos_ingresos_lista.append(nuevos_ingresos)

#         total = estudiantes[-1]
#         reprobados = int(total * alpha)
#         reprobados_lista.append(reprobados)

#         aprobados = total - reprobados
#         aprobados_lista.append(aprobados)

#         desertores = desertores_runge_kutta(reprobados, 0, unidades, 0.1, alpha, beta)[
#             -1
#         ]
#         estudiantes.append(total - desertores)
#         desertores_lista.append(desertores)

#     return (
#         estudiantes,
#         nuevos_ingresos_lista,
#         desertores_lista,
#         reprobados_lista,
#         aprobados_lista,
#     )


# import sqlite3
# import numpy as np


# def get_datos_from_db(facultad, carrera, ciclo, materia, periodo):
#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()

#     query = """
#     SELECT e.numero_estudiantes, m.unidades
#     FROM Estudiantes e
#     JOIN Materia m ON e.materia_id = m.id
#     JOIN Ciclo c ON m.ciclo_id = c.id
#     JOIN Carrera ca ON c.carrera_id = ca.id
#     JOIN Facultad f ON ca.facultad_id = f.id
#     JOIN Periodo_Academico p ON e.periodo_academico_id = p.id
#     WHERE m.nombre = ? AND c.nombre = ? AND ca.nombre = ? AND f.nombre = ? AND p.nombre = ?
#     """
#     cursor.execute(query, (materia, ciclo, carrera, facultad, periodo))
#     result = cursor.fetchone()
#     conn.close()

#     if result:
#         numero_estudiantes, unidades = result
#         return numero_estudiantes, unidades
#     else:
#         raise ValueError("No se encontraron datos para los criterios especificados.")


# def desertores_runge_kutta(reprobados_inicial, t0, t_final, h, alpha, beta):
#     desertores_lista = []
#     reprobados = reprobados_inicial
#     t = t0

#     while t < t_final:
#         desertores_lista.append(int(reprobados * (1 - beta)))

#         k1 = h * (-alpha * reprobados)
#         k2 = h * (-alpha * (reprobados + k1 / 2))
#         k3 = h * (-alpha * (reprobados + k2 / 2))
#         k4 = h * (-alpha * (reprobados + k3))

#         reprobados = reprobados + (k1 + 2 * k2 + 2 * k3 + k4) / 6
#         t = t + h

#     return desertores_lista


# def simular_ciclos(estudiantes_inicial, periodos, unidades, alpha, beta, gamma):
#     estudiantes = [estudiantes_inicial]
#     nuevos_ingresos_lista = []
#     desertores_lista = []
#     reprobados_lista = []
#     aprobados_lista = []

#     for periodo in range(periodos):
#         nuevos_ingresos = int(estudiantes[-1] * gamma)
#         estudiantes.append(estudiantes[-1] + nuevos_ingresos)
#         nuevos_ingresos_lista.append(nuevos_ingresos)

#         total = estudiantes[-1]
#         reprobados = int(total * alpha)
#         reprobados_lista.append(reprobados)

#         aprobados = total - reprobados
#         aprobados_lista.append(aprobados)

#         desertores = desertores_runge_kutta(reprobados, 0, unidades, 0.1, alpha, beta)[
#             -1
#         ]
#         estudiantes.append(total - desertores)
#         desertores_lista.append(desertores)

#     return (
#         estudiantes,
#         nuevos_ingresos_lista,
#         desertores_lista,
#         reprobados_lista,
#         aprobados_lista,
#     )


# import numpy as np
# import matplotlib.pyplot as plt

# alpha = 0.20
# beta = 0.8
# gamma = 0.10


# def desertores_runge_kutta(reprobados_inicial, t0, t_final, h):

#     desertores_lista = []
#     reprobados = reprobados_inicial
#     t = t0

#     while t < t_final:
#         desertores_lista.append(int(reprobados * (1 - beta)))

#         k1 = h * (-alpha * reprobados)
#         k2 = h * (-alpha * (reprobados + k1 / 2))
#         k3 = h * (-alpha * (reprobados + k2 / 2))
#         k4 = h * (-alpha * (reprobados + k3))

#         reprobados = reprobados + (k1 + 2 * k2 + 2 * k3 + k4) / 6
#         t = t + h

#     return desertores_lista


# def simular_ciclos(estudiantes_inicial, año_inicio, año_fin):
#     años_simular = año_fin - año_inicio + 1
#     ciclos = años_simular * 2

#     estudiantes = [estudiantes_inicial]
#     nuevos_ingresos_lista = []
#     desertores_lista = []

#     reprobados = 0

#     for año in range(año_inicio, año_fin + 1):
#         for ciclo in [1, 2]:
#             nuevos_ingresos = int(estudiantes[-1] * gamma)
#             estudiantes.append(estudiantes[-1] + nuevos_ingresos)
#             nuevos_ingresos_lista.append(nuevos_ingresos)

#             total = estudiantes[-1]
#             aprobados = int(total * (1 - alpha))

#             reprobados = int(total * alpha)

#             desertores = desertores_runge_kutta(reprobados, 0, 1, 0.1)[-1]
#             estudiantes.append(total - desertores)
#             desertores_lista.append(desertores)

#     return estudiantes, nuevos_ingresos_lista, desertores_lista


# estudiantes_inicial = int(input("Ingrese el número inicial de estudiantes: "))
# año_inicio = int(input("Ingrese el año de inicio de la simulación: "))
# año_fin = int(input("Ingrese el año final de la simulación: "))

# estudiantes, nuevos_ingresos, desertores = simular_ciclos(
#     estudiantes_inicial, año_inicio, año_fin
# )

# plt.figure(figsize=(15, 8))
# plt.plot(range(len(estudiantes)), estudiantes, marker="o")
# plt.xlabel("Ciclo")
# plt.ylabel("Número de Estudiantes")
# plt.title(f"Simulación de Estudiantes ({año_inicio}-{año_fin})")
# plt.grid(True)

# for i, est in enumerate(estudiantes):
#     plt.annotate(
#         f"{est}", (i, est), textcoords="offset points", xytext=(0, 10), ha="center"
#     )

# plt.tight_layout()
# plt.show()

# print("\nResultados detallados:")
# print(f"{año_inicio}-1 Inicio: {estudiantes[0]} estudiantes")

# for i in range(1, len(estudiantes), 2):
#     año = año_inicio + (i - 1) // 4
#     ciclo = 2 if (i - 1) % 4 >= 2 else 1

#     inicio_ciclo = estudiantes[i - 1]
#     ingresados = nuevos_ingresos[i // 2]
#     desertados = desertores[i // 2]
#     fin_ciclo = estudiantes[i + 1]

#     print(f"\n{año}-{ciclo}:")
#     print(f"  Inicio del ciclo: {inicio_ciclo} estudiantes")
#     print(f"  Ingresaron: {ingresados} estudiantes")
#     print(f"  Desertaron: {desertados} estudiantes")
#     print(f"  Fin del ciclo: {fin_ciclo} estudiantes")
#     print(f"  Cambio neto: {fin_ciclo - inicio_ciclo} estudiantes")
