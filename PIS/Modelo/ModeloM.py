import numpy as np
from scipy.integrate import solve_ivp

params_list = [
    {
        "gen": "M",
        "ciclo": 3,
        "for": "Si",
        "trab": "No",
        "disc": "No",
        "edu": "Privada",
        "hijos": "No",
    },
    {
        "gen": "F",
        "ciclo": 2,
        "for": "No",
        "trab": "Si",
        "disc": "No",
        "edu": "Publica",
        "hijos": "Si",
    },
    {
        "gen": "M",
        "ciclo": 3,
        "for": "No",
        "trab": "Si",
        "disc": "Si",
        "edu": "Publica",
        "hijos": "No",
    },
    {
        "gen": "F",
        "ciclo": 2,
        "for": "Si",
        "trab": "No",
        "disc": "Si",
        "edu": "Privada",
        "hijos": "Si",
    },
]


def lambda_S(ciclo, foraneo, trabaja, disc, edu, hijos, gen):
    base = 0.02 if gen == "M" else 0.03
    return base * (
        1
        + 0.01 * ciclo
        - 0.01 * (foraneo == "Si")
        - 0.01 * (trabaja == "Si")
        + 0.01 * (disc == "Si")
        + 0.005 * (edu == "Publica")
        + 0.01 * (hijos == "Si")
    )


def gamma_R(ciclo, foraneo, trabaja, disc, edu, hijos, gen):
    base = 0.01 if gen == "M" else 0.015
    return base * (
        1
        + 0.005 * ciclo
        + 0.01 * (foraneo == "Si")
        - 0.01 * (trabaja == "Si")
        + 0.01 * (disc == "Si")
        + 0.005 * (edu == "Publica")
        + 0.01 * (hijos == "Si")
    )


def beta_A(ciclo, foraneo, trabaja, disc, edu, hijos, gen):
    base = 0.07 if gen == "M" else 0.05
    return base * (
        1
        - 0.005 * ciclo
        + 0.01 * (foraneo == "Si")
        - 0.01 * (trabaja == "Si")
        + 0.01 * (disc == "Si")
        + 0.005 * (edu == "Publica")
        + 0.01 * (hijos == "Si")
    )


def alpha_A(ciclo, foraneo, trabaja, disc, edu, hijos, gen):
    base = 0.03 if gen == "M" else 0.025
    return base * (
        1
        + 0.01 * (foraneo == "Si")
        - 0.01 * (trabaja == "Si")
        + 0.01 * (disc == "Si")
        + 0.005 * (edu == "Publica")
        + 0.01 * (hijos == "Si")
    )


def model(t, y, ciclo, foraneo, trabaja, disc, edu, hijos, gen):
    S, R, D, A = y
    dSdt = (
        -gamma_R(ciclo, foraneo, trabaja, disc, edu, hijos, gen) * S
        - lambda_S(ciclo, foraneo, trabaja, disc, edu, hijos, gen) * S
    )
    dRdt = (
        gamma_R(ciclo, foraneo, trabaja, disc, edu, hijos, gen) * S
        - beta_A(ciclo, foraneo, trabaja, disc, edu, hijos, gen) * R
    )
    dDdt = (
        lambda_S(ciclo, foraneo, trabaja, disc, edu, hijos, gen) * S
        - alpha_A(ciclo, foraneo, trabaja, disc, edu, hijos, gen) * D
    )
    dAdt = beta_A(ciclo, foraneo, trabaja, disc, edu, hijos, gen) * R
    return [dSdt, dRdt, dDdt, dAdt]
