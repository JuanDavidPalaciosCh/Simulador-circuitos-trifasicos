import math
import cmath
import streamlit as st

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


def fasors_d_to_y(z: tuple) -> tuple:
    pass


def fasors_y_to_d(z: tuple) -> tuple:
    pass


def voltages_d_to_y(v: tuple) -> tuple:
    pass


def voltages_y_to_d(v: tuple) -> tuple:
    pass


# Simulador casos circuitos trifasicos:



# Delta - Delta

def delta_delta(v: tuple, z: tuple) -> None:
    # Fuentes / Tensiones de linea - fase
    f_ab: tuple = v[0]
    f_bc: tuple = v[1]
    f_ca: tuple = v[2]

    f_pol: tuple = (f_ab, f_bc, f_ca)
    f_rect: tuple = transform_to_rect(f_pol)

    # Fasores
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

    # Corrientes de linea
    i_aa: tuple = transform_to_polar((i_ab_rect - i_ca_rect, ))[0]
    i_bb: tuple = transform_to_polar((i_bc_rect - i_ab_rect, ))[0]
    i_cc: tuple = transform_to_polar((i_ca_rect - i_bc_rect, ))[0]

    # Print solution
    print("Corrientes de fase:")
    print("Iab = {:.3f} ∡ {:.3f}".format(i_ab[0], i_ab[1]))
    print("Ibc = {:.3f} ∡ {:.3f}".format(i_bc[0], i_bc[1]))
    print("Ica = {:.3f} ∡ {:.3f}".format(i_ca[0], i_ca[1]))

    print("")

    print("Corrientes de linea:")
    print("Iaa = {:.3f} ∡ {:.3f}".format(i_aa[0], i_aa[1]))
    print("Ibb = {:.3f} ∡ {:.3f}".format(i_bb[0], i_bb[1]))
    print("Icc = {:.3f} ∡ {:.3f}".format(i_cc[0], i_cc[1]))

    print("")

    print("Tensiones de fase:")
    print("Vab = {:.3f} ∡ {:.3f}".format(f_ab[0], f_ab[1]))
    print("Vbc = {:.3f} ∡ {:.3f}".format(f_bc[0], f_bc[1]))
    print("Vca = {:.3f} ∡ {:.3f}".format(f_ca[0], f_ca[1]))

    print("")

    print("Tensiones de linea:")
    print("VAB = {:.3f} ∡ {:.3f}".format(f_ab[0], f_ab[1]))
    print("VBC = {:.3f} ∡ {:.3f}".format(f_bc[0], f_bc[1]))
    print("VCA = {:.3f} ∡ {:.3f}".format(f_ca[0], f_ca[1]))

    return (i_ab, i_bc, i_ca), (i_aa, i_bb, i_cc), (f_ab, f_bc, f_ca), (f_ab, f_bc, f_ca)


# Estrella - Estrella 4 hilos


def estrella_estrella(v: tuple, z: tuple) -> None:
    # Fuentes / Tensiones fase
    f_an: tuple = v[0]
    f_bn: tuple = v[1]
    f_cn: tuple = v[2]

    f_pol: tuple = (f_an, f_bn, f_cn)
    f_rect: tuple = transform_to_rect(f_pol)

    # Fasores
    z_an: complex = z[0]
    z_bn: complex = z[1]
    z_cn: complex = z[2]

    z_rect: tuple = (z_an, z_bn, z_cn)
    z_pol: tuple = transform_to_polar(z_rect)

    # Corrientes de fase / linea
    i_an: tuple = transform_to_polar((f_rect[0] / z_rect[0], ))[0]
    i_bn: tuple = transform_to_polar((f_rect[1] / z_rect[1], ))[0]
    i_cn: tuple = transform_to_polar((f_rect[2] / z_rect[2], ))[0]

    # Tensiones de linea
    f_ab : tuple = transform_to_polar((f_rect[0] - f_rect[1], ))[0]
    f_bc : tuple = transform_to_polar((f_rect[1] - f_rect[2], ))[0]
    f_ca : tuple = transform_to_polar((f_rect[2] - f_rect[0], ))[0]


    # Print solution
    print("Corrientes de fase:")
    print("Ian = {:.3f} ∡ {:.3f}".format(i_an[0], i_an[1]))
    print("Ibn = {:.3f} ∡ {:.3f}".format(i_bn[0], i_bn[1]))
    print("Icn = {:.3f} ∡ {:.3f}".format(i_cn[0], i_cn[1]))

    print("")

    print("Corrientes de linea:")
    print("IAa = {:.3f} ∡ {:.3f}".format(i_an[0], i_an[1]))
    print("IBb = {:.3f} ∡ {:.3f}".format(i_bn[0], i_bn[1]))
    print("ICc = {:.3f} ∡ {:.3f}".format(i_cn[0], i_cn[1]))

    print("")

    print("Tensiones de fase:")
    print("Van = {:.3f} ∡ {:.3f}".format(f_an[0], f_an[1]))
    print("Vbn = {:.3f} ∡ {:.3f}".format(f_bn[0], f_bn[1]))
    print("Vcn = {:.3f} ∡ {:.3f}".format(f_cn[0], f_cn[1]))

    print("")

    print("Tensiones de linea:")
    print("VAB = {:.3f} ∡ {:.3f}".format(f_ab[0], f_ab[1]))
    print("VBC = {:.3f} ∡ {:.3f}".format(f_bc[0], f_bc[1]))
    print("VCA = {:.3f} ∡ {:.3f}".format(f_ca[0], f_ca[1]))

    return (i_an, i_bn, i_cn), (i_an, i_bn, i_cn), (f_an, f_bn, f_cn), (f_ab, f_bc, f_ca)
