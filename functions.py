import math
import cmath

# Funciones necesarias

def transform_to_polar(x: tuple) -> tuple:
    """
    La función `transform_to_polar` toma una tupla de números complejos como entrada y devuelve una tupla de
    coordenadas polares para cada número complejo.
    
    :param x: tupla - una tupla que contiene números complejos
    :type x: tupla
    :return: La función `transform_to_polar` devuelve una tupla que contiene las coordenadas polares de cada
    elemento en la tupla de entrada `x`.
    """
    y: list = []
    for i in x:
        polar: tuple = cmath.polar(i)
        polar: tuple = (polar[0], (polar[1] * 180 / math.pi))

        y.append(polar)

    y: tuple = tuple(y)
    return y


def transform_to_rect(x: tuple) -> tuple:
    """
    La función `transform_to_rect` toma una tupla de coordenadas polares y devuelve una tupla de
    coordenadas rectangulares correspondientes.
    
    :param x: El parámetro `x` es una tupla que contiene elementos que también son tuplas. Cada tupla interna
    representa una coordinada polar y consta de dos valores: la magnitud (radio) y el ángulo (en
    grados)
    :type x:tupla
    :return: una tupla de números complejos.
    """
    y: list = []
    for i in x:
        rect: complex = cmath.rect(i[0], (i[1] * math.pi / 180))

        y.append(rect)

    y: tuple = tuple(y)
    return y


def impedances_d_to_y(z: tuple) -> tuple:
    """
    La función `impedances_d_to_y` convierte impedancias delta (D) en impedancias Y (estrella).
    
    :param z: El parámetro `z` es una tupla que contiene tres números complejos que representan impedancias.
    Cada número complejo representa la impedancia entre dos puntos de un circuito. Los tres elementos de
    la tupla representa las impedancias entre los puntos A y B, los puntos B y C, y los puntos C y A,
    respectivamente
    :type z: tupla
    :return: La función `impedances_d_to_y` devuelve una tupla que contiene los valores de `z_an`, `z_bn`,
    y `z_cn`.
    """
    z_ab: complex = z[0]
    z_bc: complex = z[1]
    z_ca: complex = z[2]

    z_an: complex = z_ab * z_ca / (z_ab + z_bc + z_ca)
    z_bn: complex = z_ab * z_bc / (z_ab + z_bc + z_ca)
    z_cn: complex = z_bc * z_ca / (z_ab + z_bc + z_ca)

    return (z_an, z_bn, z_cn)


def impedances_y_to_d(z: tuple) -> tuple:
    """
    La función `impedances_y_to_d` toma una tupla de tres números complejos que representan impedancias
    y devuelve una tupla de tres números complejos que representan las impedancias delta equivalentes.
    
    :param z: El parámetro `z` es una tupla que contiene tres números complejos que representan las impedancias
    de tres fases en un sistema trifásico. Los tres elementos de la tupla representan las impedancias de
    fase A, fase B y fase C respectivamente
    :type z: tupla
    :return: La función `impedances_y_to_d` devuelve una tupla que contiene los valores de `z_ab`, `z_bc`,
    y `z_ca`.
    """
    z_an: complex = z[0]
    z_bn: complex = z[1]
    z_cn: complex = z[2]

    z_ab: complex = ((z_an * z_bn) + (z_bn * z_cn) + (z_cn * z_an)) / z_cn
    z_bc: complex = ((z_an * z_bn) + (z_bn * z_cn) + (z_cn * z_an)) / z_an
    z_ca: complex = ((z_an * z_bn) + (z_bn * z_cn) + (z_cn * z_an)) / z_bn

    return (z_ab, z_bc, z_ca)


def voltages_d_to_y(v: tuple) -> tuple:
    """
    La función `voltages_d_to_y` convierte voltajes trifásicos de delta (D) a estrella (Y)
    configuración.
    
    :param v: El parámetro `v` es una tupla que contiene tres elementos. Cada elemento representa un voltaje.
    en un sistema trifásico. Cada voltaje se representa como una tupla con dos elementos: la magnitud y
    el ángulo de fase en grados
    :type v: tupla
    :return: La función `voltages_d_to_y` devuelve una tupla que contiene tres tuplas. Cada tupla interna
    representa el voltaje en una fase diferente de un sistema trifásico. El voltaje en cada fase es
    representado como un número complejo, donde la parte real representa la magnitud y la imaginaria
    parte que representa el ángulo de fase.
    """
    v_ab = v[0]
    v_bc = v[1]
    v_ca = v[2]

    v_an = (v_ab[0]/math.sqrt(3), v_ab[1] - 30)
    v_bn = (v_bc[0]/math.sqrt(3), v_bc[1] - 30)
    v_cn = (v_ca[0]/math.sqrt(3), v_ca[1] - 30)

    return (v_an, v_bn, v_cn)


def voltages_y_to_d(v: tuple) -> tuple:
    """
    La función `voltages_y_to_d` convierte los voltajes dados de una configuración Y a una Delta
    configuración.
    
    :param v: El parámetro `v` es una tupla que contiene tres elementos. Cada elemento representa el
    Medición de tensión para una fase específica en un sistema trifásico. El formato de cada elemento es un
    tupla también, donde el primer elemento es la magnitud del voltaje y el segundo elemento es la
    ángulo de fase en grados
    :type v: tupla
    :return: La función `voltages_y_to_d` devuelve una tupla que contiene tres tuplas. Cada tupla interna
    representa un voltaje en una fase diferente. El primer elemento de cada tupla interna representa el
    magnitud del voltaje, y el segundo elemento representa el ángulo de fase en grados.
    """
    v_an = v[0]
    v_bn = v[1]
    v_cn = v[2]

    v_ab = (math.sqrt(3)*v_an[0], v_an[1] + 30)
    v_bc = (math.sqrt(3)*v_bn[0], v_bn[1] + 30)
    v_ca = (math.sqrt(3)*v_cn[0], v_cn[1] + 30)

    return (v_ab, v_bc, v_ca)


def potencia_compleja(v_f: tuple, i_f:tuple) -> complex:
    """
    La función calcula la potencia compleja multiplicando el voltaje complejo y el voltaje complejo.
    conjugado de la corriente.
    
    :param v_f: El parámetro `v_f` representa una tupla de números complejos que representa el voltaje
    de fase en forma polar. Cada elemento de la tupla representa la magnitud y el ángulo de un voltaje.
    :type v_f: tupla
    :param i_f: El parámetro `i_f` representa la corriente de fase de forma fasorial
    :type i_f: tupla
    :return: la potencia compleja, que es la suma del producto del voltaje de fase y el complejo
    conjugado de la corriente de fase.
    """
    v_f: tuple = transform_to_rect(v_f)
    i_f: tuple = transform_to_rect(i_f)

    potencia_compleja: complex = 0

    for j in range(len(v_f)):
        potencia_compleja += (v_f[j] * np.conjugate(i_f[j]))

    return potencia_compleja


def z_eq_paralelo(z: tuple) -> complex:
    """
    La función calcula la impedancia equivalente de un circuito en paralelo.
    
    :param z: El parámetro `z` es una tupla que representa las impedancias de los componentes del circuito.
    conectados en paralelo. Cada elemento de la tupla representa la impedancia de un componente.
    :type z: tupla
    :return: la impedancia equivalente de un circuito paralelo, que es un número complejo.
    """
    z_eq: complex = 0
    for i in z:
        z_eq += (1 / i)
    
    z_eq = 1 / z_eq

    return z_eq


# Simulador casos circuitos trifasicos:



# Delta - Delta

def delta_delta(v: tuple, z: tuple, z_l: tuple = (0, 0, 0)):
    """
    La función `delta_delta` calcula las corrientes, voltajes y potencia compleja en un sistema trifásico delta-delta.
    
    :param v: El parámetro `v` es una tupla que contiene los voltajes línea a neutro de un sistema trifásico.
    sistema. Tiene el formato `(f_ab, f_bc, f_ca)`, donde `f_ab`, `f_bc` y `f_ca` son complejos en representación polar.
    :type v: tupla
    :param z: El parámetro `z` representa las impedancias de carga en un sistema trifásico.
    Es una tupla que contiene tres números complejos, donde cada número complejo representa la impedancia
    de una fase.
    :type z: tupla
    :param z_l: El parámetro `z_l` representa la impedancia de linea en un sistema de energía trifásico. Es un
    tupla de tres números complejos, donde cada número representa la impedancia de la linea conectada a
    cada fase. El valor predeterminado es `(0, 0, 0)`, lo que indica que la linea es perfecta.
    :type z_l: tupla
    :return: La función `delta_delta` devuelve una tupla que contiene los siguientes valores:
    - Tupla de corrientes de fase (i_ab, i_bc, i_ca)
    - Tupla de corrientes de línea (i_aa, i_bb, i_cc)
    - Tupla de tensiones de fase (v_ab, v_bc, v_ca)
    - Tupla de tensiones línea a línea (f_ab, f_bc, f_ca)
    - Complejo que representa la potencia compleja (s)
    """

    # Fuentes / Tensiones de linea
    f_ab: tuple = v[0]
    f_bc: tuple = v[1]
    f_ca: tuple = v[2]

    f_pol: tuple = (f_ab, f_bc, f_ca)

    # Impedancias
    z_ab: complex = z[0]
    z_bc: complex = z[1]
    z_ca: complex = z[2]

    z_rect: tuple = (z_ab, z_bc, z_ca)

    # Corrientes de linea
    v_pol_y: tuple = voltages_d_to_y(f_pol)
    z_rect_y: tuple = impedances_d_to_y(z_rect)

    i_a, i_linea, v_a, v_b, n_a, s_a = estrella_estrella_3hilos(v_pol_y, z_rect_y, z_l) # Recibe Corrientes de linea del caso estrella estrella.

    i_aa: tuple = i_linea[0]
    i_bb: tuple = i_linea[1]
    i_cc: tuple = i_linea[2]

    # Tensiones de fase
    v_zl_1: complex = transform_to_rect((i_aa, ))[0] * z_l[0]
    v_zl_2: complex = transform_to_rect((i_bb, ))[0] * z_l[1]
    v_zl_3: complex = transform_to_rect((i_cc, ))[0] * z_l[2]

    v_ab: tuple = transform_to_polar((transform_to_rect((f_ab, ))[0] - v_zl_1 + v_zl_2, ))[0]
    v_bc: tuple = transform_to_polar((transform_to_rect((f_bc, ))[0] - v_zl_2 + v_zl_3, ))[0]
    v_ca: tuple = transform_to_polar((transform_to_rect((f_ca, ))[0] - v_zl_1 + v_zl_3, ))[0]

    v_f: tuple = (v_ab, v_bc, v_ca)
    v_f_rect: tuple = transform_to_rect(v_f)

    # Corrientes de fase
    i_ab: tuple = transform_to_polar((v_f_rect[0] / z_rect[0], ))[0]
    i_bc: tuple = transform_to_polar((v_f_rect[1] / z_rect[1], ))[0]
    i_ca: tuple = transform_to_polar((v_f_rect[2] / z_rect[2], ))[0]

    i_f: tuple = (i_ab, i_bc, i_ca)

    # Potencia compleja
    s: complex = potencia_compleja(v_f, i_f)

    return (i_ab, i_bc, i_ca), (i_aa, i_bb, i_cc), (v_ab, v_bc, v_ca), (f_ab, f_bc, f_ca), s


# Estrella - Estrella 4 hilos


def estrella_estrella(v: tuple, z: tuple, z_l: tuple = (0, 0, 0)):
    """
    La función `estrella_estrella` calcula varios parámetros eléctricos como corrientes,
    voltajes, potencia y corrimiento de neutro en un sistema eléctrico trifásico (estrella-estrella).
    
    :param v: El parámetro `v` es una tupla que contiene los voltajes de tres fases en forma polar. Cada
    El elemento de la tupla representa la magnitud del voltaje y el ángulo en grados.
    :type v: tupla
    :param z: El parámetro `z` es una tupla que representa las impedancias de carga de las tres fases de un
    sistema trifásico. Cada elemento de la tupla corresponde a la impedancia de una fase.
    :type z: tupla
    :param z_l: El parámetro `z_l` representa la impedancia de la línea. Es una tupla que contiene tres.
    valores, que representan la impedancia de cada fase de la línea
    :type z_l: tupla
    :return: una tupla que contiene los siguientes valores:
    - Tupla de corrientes de fase (i_an, i_bn, i_cn)
    - Tupla de corrientes de línea (i_aa, i_bb, i_cc)
    - Tupla de tensiones de fase (v_an, v_bn, v_cn)
    - Tupla de tensiones línea a línea (f_ab, f_bc, f_ca)
    - Tupla que representa el desplazamiento del neutro (n_corrimiento)
    - Complejo que representa la potencia compleja (s)
    """
    # Fuentes
    f_an: tuple = v[0]
    f_bn: tuple = v[1]
    f_cn: tuple = v[2]

    f_pol: tuple = (f_an, f_bn, f_cn)
    f_rect: tuple = transform_to_rect(f_pol)

    # Impedancias
    z_an: complex = z[0]
    z_bn: complex = z[1]
    z_cn: complex = z[2]

    z_rect: tuple = (z_an, z_bn, z_cn)

    # Corrientes de fase / linea
    i_an: tuple = transform_to_polar((f_rect[0] / (z_rect[0] + z_l[0]), ))[0]
    i_bn: tuple = transform_to_polar((f_rect[1] / (z_rect[1] + z_l[1]), ))[0]
    i_cn: tuple = transform_to_polar((f_rect[2] / (z_rect[2] + z_l[2]), ))[0]

    i_f: tuple = (i_an, i_bn, i_cn)
    i_f_rect: tuple = transform_to_rect(i_f)

    # Tensiones de linea
    f_ab : tuple = transform_to_polar((f_rect[0] - f_rect[1], ))[0]
    f_bc : tuple = transform_to_polar((f_rect[1] - f_rect[2], ))[0]
    f_ca : tuple = transform_to_polar((f_rect[2] - f_rect[0], ))[0]

    # Tensiones de fase
    v_an: tuple = transform_to_polar((transform_to_rect((i_an, ))[0] * z_rect[0], ))[0]
    v_bn: tuple = transform_to_polar((transform_to_rect((i_bn, ))[0] * z_rect[1], ))[0]
    v_cn: tuple = transform_to_polar((transform_to_rect((i_cn, ))[0] * z_rect[2], ))[0]

    v_f: tuple = (v_an, v_bn, v_cn)

    # Corrimiento del neutro
    n_corrimiento: tuple = transform_to_polar((-1 * (i_f_rect[0] + i_f_rect[1] + i_f_rect[2]), ))[0]

    # Potencia compleja
    s: tuple = potencia_compleja(v_f, i_f)

    return (i_an, i_bn, i_cn), (i_an, i_bn, i_cn), (v_an, v_bn, v_cn), (f_ab, f_bc, f_ca), n_corrimiento, s


# Delta - Estrella

def delta_estrella(v: tuple, z: tuple, z_l: tuple = (0, 0, 0)):
    """
    La función `delta_estrella` calcula las corrientes, voltajes, potencia y cambio de neutro en un
    Sistema trifásico estrella delta (estrella).
    
    :param v: El parámetro `v` es una tupla que contiene los voltajes de tres fases en forma polar.
    El voltaje se representa como una tupla que contiene la magnitud y el ángulo en grados.
    :type v: tupla
    :param z: El parámetro `z` es una tupla que representa los valores de impedancia de carga de las tres fases en
    forma rectangular. Cada elemento de la tupla corresponde a la impedancia de una fase.
    :type z: tupla
    :param z_l: El parámetro `z_l` representa la impedancia de la linea conectada al sistema. Es
    una tupla de tres números complejos, que representa las impedancias de la linea conectada a las fases A, B,
    y C respectivamente
    :type z_l: tupla
    :return: La función `delta_estrella` devuelve una tupla que contiene los siguientes valores:
    - Tupla de corrientes de fase (i_an, i_bn, i_cn)
    - Tupla de corrientes de línea (i_aa, i_bb, i_cc)
    - Tupla de tensiones de fase (v_an, v_bn, v_cn)
    - Tupla de tensiones línea a línea (f_ab, f_bc, f_ca)
    - Tupla que representa el desplazamiento del neutro (n_corrimiento)
    - Complejo que representa la potencia compleja (s)
    """
    # Fuentes
    f_ab: tuple = v[0]
    f_bc: tuple = v[1]
    f_ca: tuple = v[2]

    f_pol: tuple = (f_ab, f_bc, f_ca)

    # Fasores
    z_an: complex = z[0]
    z_bn: complex = z[1]
    z_cn: complex = z[2]

    z_rect: tuple = (z_an, z_bn, z_cn)

    # Corrientes de linea / fase
    v_pol_y: tuple = voltages_d_to_y(f_pol)
    i_a, i_linea, v_a, v_b, n_a, s_a = estrella_estrella_3hilos(v_pol_y, z_rect, z_l) # Recibe Corrientes de linea del caso estrella estrella.


    i_aa: tuple = i_linea[0]
    i_bb: tuple = i_linea[1]
    i_cc: tuple = i_linea[2]

    i_an: tuple = i_aa
    i_bn: tuple = i_bb
    i_cn: tuple = i_cc

    i_f: tuple = (i_an, i_bn, i_cn)

    # Tensiones de linea
    f_ab : tuple = f_pol[0]
    f_bc : tuple = f_pol[1]
    f_ca : tuple = f_pol[2]

    # Tensiones de fase
    v_an: tuple = transform_to_polar((transform_to_rect((i_an, ))[0] * z_rect[0], ))[0]
    v_bn: tuple = transform_to_polar((transform_to_rect((i_bn, ))[0] * z_rect[1], ))[0]
    v_cn: tuple = transform_to_polar((transform_to_rect((i_cn, ))[0] * z_rect[2], ))[0]

    v_f: tuple = (v_an, v_bn, v_cn)

    # Corrimiento del neutro
    voltages_y_y: tuple = voltages_d_to_y(f_pol)
    i_a, i_b, v_a, v_b, n_corrimiento, s_a = estrella_estrella_3hilos(voltages_y_y, z_rect) # Recibe corrimiento del neutro del caso estrella estrella.

    # Potencia compleja
    s: tuple = potencia_compleja(v_f, i_f)

    return (i_an, i_bn, i_cn), (i_aa, i_bb, i_cc), (v_an, v_bn, v_cn), (f_ab, f_bc, f_ca), n_corrimiento, s


#  Estrella - Delta

def estrella_delta(v: tuple, z: tuple, z_l: tuple = (0, 0, 0)):
    """
    La función `estrella_delta` calcula las corrientes y voltajes en un sistema eléctrico estrella-triángulo
    y devuelve los resultados.
    
    :param v: El parámetro `v` es una tupla que contiene los voltajes de tres fases en forma polar.
    El voltaje se representa como una tupla con dos elementos: la magnitud y el ángulo en grados.
    :tipo v: tupla
    :param z: El parámetro `z` es una tupla que representa las impedancias de carga de las tres fases en un
    sistema trifásico. 
    :tipo z: tupla
    :param z_l: El parámetro `z_l` representa las impedancias de linea en el circuito.
    :tipo z_l: tupla
    :return: una tupla que contiene los siguientes valores:
    - Tupla de corrientes de fase (i_ab, i_bc, i_ca)
    - Tupla de corrientes de línea (i_aa, i_bb, i_cc)
    - Tupla de tensiones de fase (f_ab, f_bc, f_ca)
    - Tupla de tensiones línea a línea (f_AB, f_BC, f_CA)
    - Complejo que representa la potencia compleja (s)
    """
    # Fuentes
    f_an: tuple = v[0]
    f_bn: tuple = v[1]
    f_cn: tuple = v[2]

    f_pol: tuple = (f_an, f_bn, f_cn)
    f_rect: tuple = transform_to_rect(f_pol)

    f_pol_d: tuple = voltages_y_to_d(f_pol)

    # Impedancias
    z_ab: complex = z[0]
    z_bc: complex = z[1]
    z_ca: complex = z[2]

    z_rect: tuple = (z_ab, z_bc, z_ca)

    # Corrientes de linea
    z_rect_y: tuple = impedances_d_to_y(z_rect)
    i_a, i_linea, v_a, v_b, n_a, s_a = estrella_estrella_3hilos(f_pol, z_rect_y, z_l) # Recibe Corrientes de linea del caso estrella estrella.

    i_aa: tuple = i_linea[0]
    i_bb: tuple = i_linea[1]
    i_cc: tuple = i_linea[2]

    # Tensiones de linea
    f_AB: tuple = transform_to_polar((f_rect[0] - f_rect[1], ))[0]
    f_BC: tuple = transform_to_polar((f_rect[1] - f_rect[2], ))[0]
    f_CA: tuple = transform_to_polar((f_rect[2] - f_rect[0], ))[0]

    # Corrientes de fase

    v_z_l1 = transform_to_rect((i_aa, ))[0] * z_l[0]
    v_z_l2 = transform_to_rect((i_bb, ))[0] * z_l[1]
    v_z_l3 = transform_to_rect((i_cc, ))[0] * z_l[2]

    i_ab: tuple = transform_to_polar(((transform_to_rect((f_AB, ))[0] - v_z_l1 + v_z_l2) / z_rect[0], ))[0]
    i_bc: tuple = transform_to_polar(((transform_to_rect((f_BC, ))[0] - v_z_l2 + v_z_l3) / z_rect[1], ))[0]
    i_ca: tuple = transform_to_polar(((transform_to_rect((f_CA, ))[0] - v_z_l1 + v_z_l3) / z_rect[2], ))[0]

    i_f = (i_ab, i_bc, i_ca)

    #  Tensiones de fase
    f_ab: tuple = transform_to_polar((transform_to_rect((f_AB, ))[0] - v_z_l1 + v_z_l2, ))[0]
    f_bc: tuple = transform_to_polar((transform_to_rect((f_BC, ))[0] - v_z_l2 + v_z_l3, ))[0]
    f_ca: tuple = transform_to_polar((transform_to_rect((f_CA, ))[0] - v_z_l1 + v_z_l3, ))[0]

    v_f = (f_ab, f_bc, f_ca)

    # Potencia compleja
    s: tuple = potencia_compleja(v_f, i_f)

    return (i_ab, i_bc, i_ca), (i_aa, i_bb, i_cc), (f_ab, f_bc, f_ca), (f_AB, f_BC, f_CA), s


# Estrella - Estrella 3 hilos

import numpy as np

def estrella_estrella_3hilos(v: tuple, z: tuple, z_l: tuple = (0, 0, 0)):    
    """
    La función `estrella_estrella_3hilos` calcula las corrientes, voltajes, potencia y cambio de neutro.
    en un sistema eléctrico trifásico (estrella-estrella).
    
    :param v: El parámetro `v` es una tupla que contiene los voltajes de tres fases en forma polar.
    El voltaje se representa como una tupla que contiene la magnitud y el ángulo en grados.
    :type v: tupla
    :param z: El parámetro `z` es una tupla que representa los valores de impedancia de carga de las tres fases en
    forma rectangular. Cada elemento de la tupla corresponde a la impedancia de una fase.
    :type z: tupla
    :param z_l: El parámetro `z_l` representa la impedancia de la linea conectada al sistema. Es
    una tupla de tres números complejos, que representa las impedancias de la linea conectada a las fases A, B,
    y C respectivamente
    :type z_l: tupla
    :return: una tupla que contiene los siguientes valores:
    - Tupla de corrientes de fase (i_an, i_bn, i_cn)
    - Tupla de corrientes de línea (i_aa, i_bb, i_cc)
    - Tupla de tensiones de fase (v_an, v_bn, v_cn)
    - Tupla de tensiones línea a línea (f_ab, f_bc, f_ca)
    - Tupla que representa el desplazamiento del neutro (n_corrimiento)
    - Complejo que representa la potencia compleja (s)
    """
    # Fuentes
    f_an: tuple = v[0]
    f_bn: tuple = v[1]
    f_cn: tuple = v[2]

    f_pol: tuple = (f_an, f_bn, f_cn)
    f_rect: tuple = transform_to_rect(f_pol)

    # Impedancias
    z_an: complex = z[0]
    z_bn: complex = z[1]
    z_cn: complex = z[2]

    z_rect: tuple = (z_an, z_bn, z_cn)

    # Corrientes necesarias para hallar corrientes de linea
    eq_matrix = np.array([[z_rect[0] + z_rect[1] + z_l[0] + z_l[1], -z_rect[1] - z_l[1]], [-z_rect[1] - z_l[1], z_rect[1] + z_rect[2] + z_l[1] + z_l[2]]])
    v_matrix = np.array([[f_rect[0] - f_rect[1]], [f_rect[1] - f_rect[2]]])

    sol_matrix: np.array = np.dot(np.linalg.inv(eq_matrix), v_matrix)

    i_1: complex = sol_matrix[0][0]
    i_2: complex = sol_matrix[1][0]

    # Corrientes de fase / linea
    i_an: tuple = transform_to_polar((i_1, ))[0]
    i_bn: tuple = transform_to_polar((i_2 - i_1, ))[0]
    i_cn: tuple = transform_to_polar((-1 * i_2, ))[0]

    i_f: tuple = (i_an, i_bn, i_cn)

    # Tensiones de linea
    f_ab : tuple = transform_to_polar((f_rect[0] - f_rect[1], ))[0]
    f_bc : tuple = transform_to_polar((f_rect[1] - f_rect[2], ))[0]
    f_ca : tuple = transform_to_polar((f_rect[2] - f_rect[0], ))[0]

    # Tensiones de fase
    v_an: tuple = transform_to_polar((transform_to_rect((i_an, ))[0] * z_rect[0], ))[0]
    v_bn: tuple = transform_to_polar((transform_to_rect((i_bn, ))[0] * z_rect[1], ))[0]
    v_cn: tuple = transform_to_polar((transform_to_rect((i_cn, ))[0] * z_rect[2], ))[0]

    v_f: tuple = (v_an, v_bn, v_cn)

    # Corrimiento del neutro
    n_corrimiento: tuple = transform_to_polar((f_rect[0] - transform_to_rect((v_an, ))[0], ))[0]

    # Potencia compleja
    s: tuple = potencia_compleja(v_f, i_f)

    return (i_an, i_bn, i_cn), (i_an, i_bn, i_cn), (v_an, v_bn, v_cn), (f_ab, f_bc, f_ca), n_corrimiento, s