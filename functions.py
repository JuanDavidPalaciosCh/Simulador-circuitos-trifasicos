import math
import cmath

# Funciones necesarias

def transform_to_polar(x: tuple) -> tuple:
    y: list = []
    for i in x:
        polar: tuple = cmath.polar(i)
        polar: tuple = (polar[0], (polar[1] * 180 / math.pi))

        y.append(polar)

    y: tuple = tuple(y)
    return y


def transform_to_rect(x: tuple) -> tuple:
    y: list = []
    for i in x:
        rect: complex = cmath.rect(i[0], (i[1] * math.pi / 180))

        y.append(rect)

    y: tuple = tuple(y)
    return y


def impedances_d_to_y(z: tuple) -> tuple:
    z_ab: complex = z[0]
    z_bc: complex = z[1]
    z_ca: complex = z[2]

    z_an: complex = z_ab * z_ca / (z_ab + z_bc + z_ca)
    z_bn: complex = z_ab * z_bc / (z_ab + z_bc + z_ca)
    z_cn: complex = z_bc * z_ca / (z_ab + z_bc + z_ca)

    return (z_an, z_bn, z_cn)


def impedances_y_to_d(z: tuple) -> tuple:
    z_an: complex = z[0]
    z_bn: complex = z[1]
    z_cn: complex = z[2]

    z_ab: complex = ((z_an * z_bn) + (z_bn * z_cn) + (z_cn * z_an)) / z_cn
    z_bc: complex = ((z_an * z_bn) + (z_bn * z_cn) + (z_cn * z_an)) / z_an
    z_ca: complex = ((z_an * z_bn) + (z_bn * z_cn) + (z_cn * z_an)) / z_bn

    return (z_ab, z_bc, z_ca)


def voltages_d_to_y(v: tuple) -> tuple:
    v_ab = v[0]
    v_bc = v[1]
    v_ca = v[2]

    v_an = (v_ab[0]/math.sqrt(3), v_ab[1] - 30)
    v_bn = (v_bc[0]/math.sqrt(3), v_bc[1] - 30)
    v_cn = (v_ca[0]/math.sqrt(3), v_ca[1] - 30)

    return (v_an, v_bn, v_cn)


def voltages_y_to_d(v: tuple) -> tuple:
    v_an = v[0]
    v_bn = v[1]
    v_cn = v[2]

    v_ab = (math.sqrt(3)*v_an[0], v_an[1] + 30)
    v_bc = (math.sqrt(3)*v_bn[0], v_bn[1] + 30)
    v_ca = (math.sqrt(3)*v_cn[0], v_cn[1] + 30)

    return (v_ab, v_bc, v_ca)


def potencia_compleja(v_f: tuple, i_f:tuple) -> complex:
    v_f: tuple = transform_to_rect(v_f)
    i_f: tuple = transform_to_rect(i_f)

    potencia_compleja: complex = 0

    for j in range(len(v_f)):
        potencia_compleja += (v_f[j] * np.conjugate(i_f[j]))

    return potencia_compleja


def z_eq_paralelo(z: tuple) -> complex:
    #Calcula la impedancia equivalente de un circuito en paralelo.
    z_eq: complex = 0
    for i in z:
        z_eq += (1 / i)
    
    z_eq = 1 / z_eq

    return z_eq


# Simulador casos circuitos trifasicos:



# Delta - Delta

def delta_delta(v: tuple, z: tuple, z_l: tuple = (0, 0, 0)):
    # Fuentes / Tensiones de linea - fase
    f_ab: tuple = v[0]
    f_bc: tuple = v[1]
    f_ca: tuple = v[2]

    f_pol: tuple = (f_ab, f_bc, f_ca)
    f_rect: tuple = transform_to_rect(f_pol)

    # Impedancias
    z_ab: complex = z[0]
    z_bc: complex = z[1]
    z_ca: complex = z[2]

    z_rect: tuple = (z_ab, z_bc, z_ca)
    z_pol: tuple = transform_to_polar(z_rect)

    # Corrientes de fase
    i_ab: tuple = transform_to_polar((f_rect[0] / z_rect[0], ))[0]
    i_bc: tuple = transform_to_polar((f_rect[1] / z_rect[1], ))[0]
    i_ca: tuple = transform_to_polar((f_rect[2] / z_rect[2], ))[0]

    i_ab_rect: complex = transform_to_rect(((i_ab[0], i_ab[1]), ))[0]
    i_bc_rect: complex = transform_to_rect(((i_bc[0], i_bc[1]), ))[0]
    i_ca_rect: complex = transform_to_rect(((i_ca[0], i_ca[1]), ))[0]

    i_f: tuple = (i_ab, i_bc, i_ca)

    # Corrientes de linea
    i_aa: tuple = transform_to_polar((i_ab_rect - i_ca_rect, ))[0]
    i_bb: tuple = transform_to_polar((i_bc_rect - i_ab_rect, ))[0]
    i_cc: tuple = transform_to_polar((i_ca_rect - i_bc_rect, ))[0]

    # Potencia compleja
    s: complex = potencia_compleja(f_pol, i_f)

    return (i_ab, i_bc, i_ca), (i_aa, i_bb, i_cc), (f_ab, f_bc, f_ca), (f_ab, f_bc, f_ca), s


# Estrella - Estrella 4 hilos


def estrella_estrella(v: tuple, z: tuple, z_l: tuple = (0, 0, 0)):
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
    z_pol: tuple = transform_to_polar(z_rect)

    # Corrientes de fase / linea
    i_an: tuple = transform_to_polar((f_rect[0] / (z_rect[0] + z_l[0]), ))[0]
    i_bn: tuple = transform_to_polar((f_rect[1] / (z_rect[1] + z_l[1]), ))[0]
    i_cn: tuple = transform_to_polar((f_rect[2] / (z_rect[2] + z_l[2]), ))[0]

    i_f: tuple = (i_an, i_bn, i_cn)

    # Tensiones de linea
    f_ab : tuple = transform_to_polar((f_rect[0] - f_rect[1], ))[0]
    f_bc : tuple = transform_to_polar((f_rect[1] - f_rect[2], ))[0]
    f_ca : tuple = transform_to_polar((f_rect[2] - f_rect[0], ))[0]

    # Tensiones de fase
    v_an = transform_to_polar((transform_to_rect((i_an, ))[0] * z_rect[0], ))[0]
    v_bn = transform_to_polar((transform_to_rect((i_bn, ))[0] * z_rect[1], ))[0]
    v_cn = transform_to_polar((transform_to_rect((i_cn, ))[0] * z_rect[2], ))[0]

    v_f = (v_an, v_bn, v_cn)

    # Potencia compleja
    s: tuple = potencia_compleja(v_f, i_f)

    return (i_an, i_bn, i_cn), (i_an, i_bn, i_cn), (v_an, v_bn, v_cn), (f_ab, f_bc, f_ca), (0,0), s


# Delta - Estrella

def delta_estrella(v: tuple, z: tuple, z_l: tuple = (0, 0, 0)):
    # Fuentes
    f_ab: tuple = v[0]
    f_bc: tuple = v[1]
    f_ca: tuple = v[2]

    f_pol: tuple = (f_ab, f_bc, f_ca)
    f_rect: tuple = transform_to_rect(f_pol)

    # Fasores
    z_an: complex = z[0]
    z_bn: complex = z[1]
    z_cn: complex = z[2]

    z_rect: tuple = (z_an, z_bn, z_cn)
    z_pol: tuple = transform_to_polar(z_rect)

    z_rect_d: tuple = impedances_y_to_d(z_rect) # Transforma los fasores a distribución delta para enccontrar las corrientes de linea.

    # Corrientes de linea / fase
    v_pol_y = voltages_d_to_y(f_pol)
    i_a, i_linea, v_a, v_b, n_a, s_a = estrella_estrella_3hilos(v_pol_y, z_rect, z_l) # Recibe Corrientes de linea del caso estrella estrella.


    i_aa = i_linea[0]
    i_bb = i_linea[1]
    i_cc = i_linea[2]

    i_an: tuple = i_aa
    i_bn: tuple = i_bb
    i_cn: tuple = i_cc

    i_f: tuple = (i_an, i_bn, i_cn)

    # Tensiones de linea
    f_ab : tuple = f_pol[0]
    f_bc : tuple = f_pol[1]
    f_ca : tuple = f_pol[2]

    # Tensiones de fase
    v_an = transform_to_polar((transform_to_rect((i_an, ))[0] * z_rect[0], ))[0]
    v_bn = transform_to_polar((transform_to_rect((i_bn, ))[0] * z_rect[1], ))[0]
    v_cn = transform_to_polar((transform_to_rect((i_cn, ))[0] * z_rect[2], ))[0]

    v_f = (v_an, v_bn, v_cn)

    # Corrimiento del neutro
    voltages_y_y = voltages_d_to_y(f_pol)
    i_a, i_b, v_a, v_b, n_corrimiento, s_a = estrella_estrella_3hilos(voltages_y_y, z_rect) # Recibe corrimiento del neutro del caso estrella estrella.

    # Potencia compleja
    s: tuple = potencia_compleja(v_f, i_f)

    return (i_an, i_bn, i_cn), (i_aa, i_bb, i_cc), (v_an, v_bn, v_cn), (f_ab, f_bc, f_ca), n_corrimiento, s


#  Estrella - Delta

def estrella_delta(v: tuple, z: tuple, z_l: tuple = (0, 0, 0)):
    # Fuentes
    f_an: tuple = v[0]
    f_bn: tuple = v[1]
    f_cn: tuple = v[2]

    f_pol: tuple = (f_an, f_bn, f_cn)
    f_rect: tuple = transform_to_rect(f_pol)

    f_pol_d: tuple = voltages_y_to_d(f_pol)
    f_rect_d: tuple = transform_to_rect(f_pol_d)

    # Impedancias
    z_ab: complex = z[0]
    z_bc: complex = z[1]
    z_ca: complex = z[2]

    z_rect: tuple = (z_ab, z_bc, z_ca)
    z_pol: tuple = transform_to_polar(z_rect)

    # Corrientes de linea
    z_rect_y: tuple = impedances_d_to_y(z_rect)
    i_a, i_linea, v_a, v_b, n_a, s_a = estrella_estrella_3hilos(f_pol, z_rect_y, z_l) # Recibe Corrientes de linea del caso estrella estrella.

    i_aa = i_linea[0]
    i_bb = i_linea[1]
    i_cc = i_linea[2]

    # Tensiones de linea
    f_AB : tuple = transform_to_polar((f_rect[0] - f_rect[1], ))[0]
    f_BC : tuple = transform_to_polar((f_rect[1] - f_rect[2], ))[0]
    f_CA : tuple = transform_to_polar((f_rect[2] - f_rect[0], ))[0]

    # Tensiones de fase
    f_ab: tuple = f_AB
    f_bc: tuple = f_BC 
    f_ca: tuple = f_CA

    v_f = (f_ab, f_bc, f_ca)

    # Corrientes de fase

    v_z_l1 = transform_to_rect((i_aa, ))[0] * z_l[0]
    v_z_l2 = transform_to_rect((i_bb, ))[0] * z_l[1]
    v_z_l3 = transform_to_rect((i_cc, ))[0] * z_l[2]

    i_ab: tuple = transform_to_polar(((transform_to_rect((f_AB, ))[0] - v_z_l1 + v_z_l2) / z_rect[0], ))[0]
    i_bc: tuple = transform_to_polar(((transform_to_rect((f_BC, ))[0] - v_z_l2 + v_z_l3) / z_rect[1], ))[0]
    i_ca: tuple = transform_to_polar(((transform_to_rect((f_CA, ))[0] - v_z_l1 + v_z_l3) / z_rect[2], ))[0]

    i_f = (i_ab, i_bc, i_ca)

    # Potencia compleja
    s: tuple = potencia_compleja(v_f, i_f)

    return (i_ab, i_bc, i_ca), (i_aa, i_bb, i_cc), (f_ab, f_bc, f_ca), (f_AB, f_BC, f_CA), s


# Estrella - Estrella 3 hilos

import numpy as np

def estrella_estrella_3hilos(v: tuple, z: tuple, z_l: tuple = (0, 0, 0)):    
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
    z_pol: tuple = transform_to_polar(z_rect)

    # Corrientes necesarias para hallar corrientes de linea
    eq_matrix = np.array([[z_rect[0] + z_rect[1] + z_l[0] + z_l[1], -z_rect[1] - z_l[1]], [-z_rect[1] - z_l[1], z_rect[1] + z_rect[2] + z_l[1] + z_l[2]]])
    v_matrix = np.array([[f_rect[0] - f_rect[1]], [f_rect[1] - f_rect[2]]])

    sol_matrix = np.dot(np.linalg.inv(eq_matrix), v_matrix)

    i_1 = sol_matrix[0][0]
    i_2 = sol_matrix[1][0]

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
    v_an = transform_to_polar((transform_to_rect((i_an, ))[0] * z_rect[0], ))[0]
    v_bn = transform_to_polar((transform_to_rect((i_bn, ))[0] * z_rect[1], ))[0]
    v_cn = transform_to_polar((transform_to_rect((i_cn, ))[0] * z_rect[2], ))[0]

    v_f = (v_an, v_bn, v_cn)

    # Corrimiento del neutro
    n_corrimiento: tuple = transform_to_polar((f_rect[0] - transform_to_rect((v_an, ))[0], ))[0]

    # Potencia compleja
    s: tuple = potencia_compleja(v_f, i_f)

    return (i_an, i_bn, i_cn), (i_an, i_bn, i_cn), (v_an, v_bn, v_cn), (f_ab, f_bc, f_ca), n_corrimiento, s