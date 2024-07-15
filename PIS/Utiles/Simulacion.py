import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Utiles"))
)

from MetodoDesercion import get_datos_historicos, simular_ciclos
import matplotlib.pyplot as plt

facultad = input("Ingrese la facultad: ")
carrera = input("Ingrese la carrera: ")
ciclo = input("Ingrese el ciclo: ")
materia = input("Ingrese la materia: ")
periodo = input("Ingrese el periodo académico: ")
periodos = int(input("Ingrese el número de periodos académicos para la simulación: "))

numero_estudiantes, porcentaje_reprobados, porcentaje_desertores, unidades = (
    get_datos_historicos(facultad, carrera, ciclo, materia, periodo)
)

estudiantes, reprobados, desertores, aprobados = simular_ciclos(
    numero_estudiantes, porcentaje_reprobados, porcentaje_desertores, periodos, unidades
)

ciclos = list(range(periodos + 1))

plt.figure(figsize=(15, 8))
plt.plot(ciclos, estudiantes, marker="o", label="Matriculados")
plt.plot(ciclos[1:], reprobados, marker="x", linestyle="--", label="Reprobados")
plt.plot(ciclos[1:], desertores, marker="s", linestyle="--", label="Desertores")
plt.plot(ciclos[1:], aprobados, marker="d", linestyle="--", label="Aprobados")

plt.xlabel("Unidades")
plt.ylabel("Número de Estudiantes")
plt.title(
    f"Simulación de Estudiantes para {facultad} - {carrera} - {ciclo} - {materia} ({periodo})"
)
plt.grid(True)
plt.legend()

for i, est in enumerate(estudiantes):
    plt.annotate(
        f"{est}", (i, est), textcoords="offset points", xytext=(0, 10), ha="center"
    )

plt.tight_layout()
plt.show()

print("\nResultados detallados:")
print(f"Inicio del periodo: {estudiantes[0]} estudiantes")

for i in range(1, len(estudiantes)):
    periodo_actual = i

    inicio_periodo = estudiantes[i - 1]
    reprobados_periodo = reprobados[i - 1]
    desertados_periodo = desertores[i - 1]
    aprobados_periodo = aprobados[i - 1]
    fin_periodo = estudiantes[i]

    print(f"\nPeriodo {periodo_actual}:")
    print(f"  Inicio del periodo: {inicio_periodo} estudiantes")
    print(f"  Reprobados: {reprobados_periodo} estudiantes")
    print(f"  Desertaron: {desertados_periodo} estudiantes")
    print(f"  Aprobados: {aprobados_periodo} estudiantes")
    print(f"  Fin del periodo: {fin_periodo} estudiantes")
    print(f"  Cambio neto: {fin_periodo - inicio_periodo} estudiantes")

    print(
        f"  Porcentaje de Reprobados: {100 * reprobados_periodo / inicio_periodo:.2f}%"
    )
    print(
        f"  Porcentaje de Desertores: {100 * desertados_periodo / inicio_periodo:.2f}%"
    )
    print(f"  Porcentaje de Aprobados: {100 * aprobados_periodo / inicio_periodo:.2f}%")


# import sys
# import os

# sys.path.append(
#     os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Utiles"))
# )

# from MetodoDesercion import get_datos_from_db, simular_ciclos
# import matplotlib.pyplot as plt

# alpha = 0.20
# beta = 0.8
# gamma = 0.10

# facultad = input("Ingrese la facultad: ")
# carrera = input("Ingrese la carrera: ")
# ciclo = input("Ingrese el ciclo: ")
# materia = input("Ingrese la materia: ")
# periodo = input("Ingrese el periodo académico: ")
# periodos = int(input("Ingrese el número de periodos académicos para la simulación: "))

# estudiantes_inicial, unidades = get_datos_from_db(
#     facultad, carrera, ciclo, materia, periodo
# )

# estudiantes, nuevos_ingresos, desertores, reprobados, aprobados = simular_ciclos(
#     estudiantes_inicial, periodos, unidades, alpha, beta, gamma
# )

# ciclos = list(range(periodos * 2 + 1))

# plt.figure(figsize=(15, 8))
# plt.plot(ciclos, estudiantes, marker="o", label="Matriculados")
# plt.plot(ciclos[1::2], reprobados, marker="x", linestyle="--", label="Reprobados")
# plt.plot(ciclos[1::2], desertores, marker="s", linestyle="--", label="Desertores")
# plt.plot(ciclos[1::2], aprobados, marker="d", linestyle="--", label="Aprobados")

# plt.xlabel("Unidades")
# plt.ylabel("Número de Estudiantes")
# plt.title(
#     f"Simulación de Estudiantes para {facultad} - {carrera} - {ciclo} - {materia} ({periodo})"
# )
# plt.grid(True)
# plt.legend()

# for i, est in enumerate(estudiantes):
#     plt.annotate(
#         f"{est}", (i, est), textcoords="offset points", xytext=(0, 10), ha="center"
#     )

# plt.tight_layout()
# plt.show()

# print("\nResultados detallados:")
# print(f"Inicio del periodo: {estudiantes[0]} estudiantes")

# for i in range(1, len(estudiantes), 2):
#     periodo_actual = (i + 1) // 2

#     inicio_periodo = estudiantes[i - 1]
#     ingresados = nuevos_ingresos[(i - 1) // 2]
#     desertados = desertores[(i - 1) // 2]
#     reprobados_periodo = reprobados[(i - 1) // 2]
#     aprobados_periodo = aprobados[(i - 1) // 2]
#     fin_periodo = estudiantes[i]

#     print(f"\nPeriodo {periodo_actual}:")
#     print(f"  Inicio del periodo: {inicio_periodo} estudiantes")
#     print(f"  Ingresaron: {ingresados} estudiantes")
#     print(f"  Reprobados: {reprobados_periodo} estudiantes")
#     print(f"  Desertaron: {desertados} estudiantes")
#     print(f"  Aprobados: {aprobados_periodo} estudiantes")
#     print(f"  Fin del periodo: {fin_periodo} estudiantes")
#     print(f"  Cambio neto: {fin_periodo - inicio_periodo} estudiantes")

#     print(
#         f"  Porcentaje de Reprobados: {100 * reprobados_periodo / inicio_periodo:.2f}%"
#     )
#     print(f"  Porcentaje de Desertores: {100 * desertados / inicio_periodo:.2f}%")
#     print(f"  Porcentaje de Aprobados: {100 * aprobados_periodo / inicio_periodo:.2f}%")


# import matplotlib.pyplot as plt
# from models import get_datos_from_db, simular_ciclos

# alpha = 0.20
# beta = 0.8
# gamma = 0.10

# facultad = input("Ingrese la facultad: ")
# carrera = input("Ingrese la carrera: ")
# ciclo = input("Ingrese el ciclo: ")
# materia = input("Ingrese la materia: ")
# periodo = input("Ingrese el periodo académico: ")
# periodos = int(input("Ingrese el número de periodos académicos para la simulación: "))

# estudiantes_inicial, unidades = get_datos_from_db(
#     facultad, carrera, ciclo, materia, periodo
# )

# estudiantes, nuevos_ingresos, desertores, reprobados, aprobados = simular_ciclos(
#     estudiantes_inicial, periodos, unidades, alpha, beta, gamma
# )

# ciclos = list(range(periodos * 2 + 1))

# plt.figure(figsize=(15, 8))
# plt.plot(ciclos, estudiantes, marker="o", label="Matriculados")
# plt.plot(ciclos[1::2], reprobados, marker="x", linestyle="--", label="Reprobados")
# plt.plot(ciclos[1::2], desertores, marker="s", linestyle="--", label="Desertores")
# plt.plot(ciclos[1::2], aprobados, marker="d", linestyle="--", label="Aprobados")

# plt.xlabel("Unidades")
# plt.ylabel("Número de Estudiantes")
# plt.title(
#     f"Simulación de Estudiantes para {facultad} - {carrera} - {ciclo} - {materia} ({periodo})"
# )
# plt.grid(True)
# plt.legend()

# for i, est in enumerate(estudiantes):
#     plt.annotate(
#         f"{est}", (i, est), textcoords="offset points", xytext=(0, 10), ha="center"
#     )

# plt.tight_layout()
# plt.show()

# print("\nResultados detallados:")
# print(f"Inicio del periodo: {estudiantes[0]} estudiantes")

# for i in range(1, len(estudiantes), 2):
#     periodo_actual = (i + 1) // 2

#     inicio_periodo = estudiantes[i - 1]
#     ingresados = nuevos_ingresos[(i - 1) // 2]
#     desertados = desertores[(i - 1) // 2]
#     reprobados_periodo = reprobados[(i - 1) // 2]
#     aprobados_periodo = aprobados[(i - 1) // 2]
#     fin_periodo = estudiantes[i]

#     print(f"\nPeriodo {periodo_actual}:")
#     print(f"  Inicio del periodo: {inicio_periodo} estudiantes")
#     print(f"  Ingresaron: {ingresados} estudiantes")
#     print(f"  Reprobados: {reprobados_periodo} estudiantes")
#     print(f"  Desertaron: {desertados} estudiantes")
#     print(f"  Aprobados: {aprobados_periodo} estudiantes")
#     print(f"  Fin del periodo: {fin_periodo} estudiantes")
#     print(f"  Cambio neto: {fin_periodo - inicio_periodo} estudiantes")

#     print(
#         f"  Porcentaje de Reprobados: {100 * reprobados_periodo / inicio_periodo:.2f}%"
#     )
#     print(f"  Porcentaje de Desertores: {100 * desertados / inicio_periodo:.2f}%")
#     print(f"  Porcentaje de Aprobados: {100 * aprobados_periodo / inicio_periodo:.2f}%")


# import numpy as np
# import matplotlib.pyplot as plt

# alpha = 0.20
# beta = 0.8
# gamma = 0.10


# def simular_ciclos(estudiantes_inicial, año_inicio, año_fin):
#     años_simular = año_fin - año_inicio + 1
#     ciclos = años_simular * 2

#     estudiantes = [estudiantes_inicial]
#     nuevos_ingresos_lista = []
#     desertores_lista = []

#     for año in range(año_inicio, año_fin + 1):
#         for ciclo in [1, 2]:
#             nuevos_ingresos = int(estudiantes[-1] * gamma)
#             estudiantes.append(estudiantes[-1] + nuevos_ingresos)
#             nuevos_ingresos_lista.append(nuevos_ingresos)

#             total = estudiantes[-1]
#             reprobados = int(total * alpha)
#             desertores = int(reprobados * (1 - beta))
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
