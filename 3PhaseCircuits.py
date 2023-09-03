import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
from PIL import Image
from functions import *
import streamlit as st


st.title('Simulador circuitos trifasicos')

option = st.selectbox(
    'Ingrese el circuito trifasico a resolver: ',
    ('Delta-Delta', 'Estrella-Estrella 4 hilos', 'Estrella-Estrella 3 hilos', 'Delta-Estrella', 'Estrella-Delta'))


if option == 'Delta-Delta':

    image = Image.open("DistribucionDeltaDelta.png")
    st.image(image, caption='Circuito trifasico Delta - Delta')

    "## Selección voltajes:"

    col1, col2, col3, col4= st.columns(4)

    with col1:
        v_ab_n = st.number_input('Magnitud $V_{ab}$', value=100)

    with col2:
        v_ab_a = st.number_input('Angulo $V_{ab}$', value=0)

    with col3:
        v_bc_n = st.number_input('Magnitud $V_{bc}$', value=100)

    with col4:
        v_bc_a = st.number_input('Angulo $V_{bc}$', value=-120)

    col1, col2 = st.columns(2)

    with col1:
        v_ca_n = st.number_input('Magnitud $V_{ca}$', value=100)

    with col2:
        v_ca_a = st.number_input('Angulo de $V_{ca}$', value=-240)

    "## Selección Impedancias:"

    col1, col2, col3, col4= st.columns(4)

    with col1:
        z_ab_r = st.number_input('Parte real de $Z_{ab}$', value=40)

    with col2:
        z_ab_i = st.number_input('Parte imaginaria de $Z_{ab}$', value=15)

    with col3:
        z_bc_r = st.number_input('Parte real de $Z_{bc}$', value=35)

    with col4:
        z_bc_i = st.number_input('Parte imaginaria de $Z_{bc}$', value=-15)

    col1, col2 = st.columns(2)

    with col1:
        z_ca_r = st.number_input('Parte real de $Z_{ca}$', value=10)

    with col2:
        z_ca_i = st.number_input('Parte imaginaria de $Z_{ca}$', value=30)

    
    v_ab: tuple = (v_ab_n, v_ab_a)
    v_bc: tuple = (v_bc_n, v_bc_a)
    v_ca: tuple = (v_ca_n, v_ca_a)

    v: tuple = (v_ab, v_bc, v_ca)

    z_ab: complex = complex(z_ab_r, z_ab_i)
    z_bc: complex = complex(z_bc_r, z_bc_i)
    z_ca: complex = complex(z_ca_r, z_ca_i)

    z: tuple = (z_ab, z_bc, z_ca)

    i_fase, i_linea, v_fase, v_linea, s = delta_delta(v, z)

    "----------------------------------------------------------------------------"


    col1, col2 = st.columns(2)


    with col1:
        "### Corrientes de fase:"
        st.markdown("$Iab$ = {:.3f} ∡ {:.3f}".format(i_fase[0][0], i_fase[0][1]))
        st.markdown("$Ibc$ = {:.3f} ∡ {:.3f}".format(i_fase[1][0], i_fase[1][1]))
        st.markdown("$Ica$ = {:.3f} ∡ {:.3f}".format(i_fase[2][0], i_fase[2][1]))

        "### Corrientes de linea:"
        st.markdown("$IAa$ = {:.3f} ∡ {:.3f}".format(i_linea[0][0], i_linea[0][1]))
        st.markdown("$IBb$ = {:.3f} ∡ {:.3f}".format(i_linea[1][0], i_linea[1][1]))
        st.markdown("$ICc$ = {:.3f} ∡ {:.3f}".format(i_linea[2][0], i_linea[2][1]))

        st.markdown("$S$ = {:.3f} + i {:.3f}".format(s.real, s.imag))

    with col2:
        "### Tensiones de fase:"
        st.markdown("$Vab$ = {:.3f} ∡ {:.3f}".format(v_fase[0][0], v_fase[0][1]))
        st.markdown("$Vbc$ = {:.3f} ∡ {:.3f}".format(v_fase[1][0], v_fase[1][1]))
        st.markdown("$Vca$ = {:.3f} ∡ {:.3f}".format(v_fase[2][0], v_fase[2][1]))

        "### Tensiones de linea:"
        st.markdown("$VAB$ = {:.3f} ∡ {:.3f}".format(v_linea[0][0], v_linea[0][1]))
        st.markdown("$VBC$ = {:.3f} ∡ {:.3f}".format(v_linea[1][0], v_linea[1][1]))
        st.markdown("$VCA$ = {:.3f} ∡ {:.3f}".format(v_linea[2][0], v_linea[2][1]))

    "----------------------------------------------------------------------------"
    graphs = st.selectbox(
    'Graficns: ',
    ('Corrientes de fase', 'Corrientes de linea', 'Tensiones de fase', 'Tensiones de linea'))

    if graphs == 'Corrientes de fase':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        corriente_ab = lambda x: i_fase[0][0] * math.cos(math.radians(frecuency * x + i_fase[0][1]))
        corriente_bc = lambda x: i_fase[1][0] * math.cos(math.radians(frecuency * x + i_fase[1][1]))
        corriente_ca = lambda x: i_fase[2][0] * math.cos(math.radians(frecuency * x + i_fase[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        i_ab_x = np.arange(0, rango, step)
        i_ab_y = [corriente_ab(i) for i in i_ab_x]

        i_bc_x = np.arange(0, rango, step)
        i_bc_y = [corriente_bc(i) for i in i_bc_x]

        i_ca_x = np.arange(0, rango, step)
        i_ca_y = [corriente_ca(i) for i in i_ca_x]

        fig, ax = plt.subplots()
        ax.plot(i_ab_x, i_ab_y)
        ax.plot(i_bc_x, i_bc_y)
        ax.plot(i_ca_x, i_ca_y)
        
        plt.title('Corrientes de fase')
        plt.legend(['Iab', 'Ibc', 'Ica'])
        plt.grid(True)

        st.pyplot(fig)

    elif graphs == 'Corrientes de linea':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        corriente_aa = lambda x: i_linea[0][0] * math.cos(math.radians(frecuency * x + i_linea[0][1]))
        corriente_bb = lambda x: i_linea[1][0] * math.cos(math.radians(frecuency * x + i_linea[1][1]))
        corriente_cc = lambda x: i_linea[2][0] * math.cos(math.radians(frecuency * x + i_linea[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        i_aa_x = np.arange(0, rango, step)
        i_aa_y = [corriente_aa(i) for i in i_aa_x]

        i_bb_x = np.arange(0, rango, step)
        i_bb_y = [corriente_bb(i) for i in i_bb_x]

        i_cc_x = np.arange(0, rango, step)
        i_cc_y = [corriente_cc(i) for i in i_cc_x]

        fig, ax = plt.subplots()
        ax.plot(i_aa_x, i_aa_y)
        ax.plot(i_bb_x, i_bb_y)
        ax.plot(i_cc_x, i_cc_y)

        plt.title('Corrientes de linea')
        plt.legend(['IAa', 'IBb', 'ICc'])
        plt.grid(True)

        st.pyplot(fig)

    elif graphs == 'Tensiones de fase':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        tension_ab = lambda x: v_fase[0][0] * math.cos(math.radians(frecuency * x + v_fase[0][1]))
        tension_bc = lambda x: v_fase[1][0] * math.cos(math.radians(frecuency * x + v_fase[1][1]))
        tension_ca = lambda x: v_fase[2][0] * math.cos(math.radians(frecuency * x + v_fase[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        v_ab_x = np.arange(0, rango, step)
        v_ab_y = [tension_ab(i) for i in v_ab_x]

        v_bc_x = np.arange(0, rango, step)
        v_bc_y = [tension_bc(i) for i in v_bc_x]

        v_ca_x = np.arange(0, rango, step)
        v_ca_y = [tension_ca(i) for i in v_ca_x]

        fig, ax = plt.subplots()
        ax.plot(v_ab_x, v_ab_y)
        ax.plot(v_bc_x, v_bc_y)
        ax.plot(v_ca_x, v_ca_y)

        plt.title('Tensiones de fase')
        plt.legend(['Vab', 'Vbc', 'Vca'])
        plt.grid(True)

        st.pyplot(fig)

    else:

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        tension_ab = lambda x: v_linea[0][0] * math.cos(math.radians(frecuency * x + v_linea[0][1]))
        tension_bc = lambda x: v_linea[1][0] * math.cos(math.radians(frecuency * x + v_linea[1][1]))
        tension_ca = lambda x: v_linea[2][0] * math.cos(math.radians(frecuency * x + v_linea[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        v_ab_x = np.arange(0, rango, step)
        v_ab_y = [tension_ab(i) for i in v_ab_x]

        v_bc_x = np.arange(0, rango, step)
        v_bc_y = [tension_bc(i) for i in v_bc_x]

        v_ca_x = np.arange(0, rango, step)
        v_ca_y = [tension_ca(i) for i in v_ca_x]

        fig, ax = plt.subplots()
        ax.plot(v_ab_x, v_ab_y)
        ax.plot(v_bc_x, v_bc_y)
        ax.plot(v_ca_x, v_ca_y)

        plt.title('Tensiones de linea')
        plt.legend(['VAB', 'VBC', 'VCA'])
        plt.grid(True)

        st.pyplot(fig)


elif option == 'Estrella-Estrella 4 hilos':

    image = Image.open("DistribucionEstrellaEstrella4Hilos.png")
    st.image(image, caption='Circuito trifasico Estrella - Estrella 4 hilos')
    
    "## Selección voltajes:"

    col1, col2, col3, col4= st.columns(4)

    with col1:
        v_an_n = st.number_input('Magnitud $V_{an}$', value=100)

    with col2:
        v_an_a = st.number_input('Angulo $V_{an}$', value=0)

    with col3:
        v_bn_n = st.number_input('Magnitud $V_{bn}$', value=100)

    with col4:
        v_bn_a = st.number_input('Angulo $V_{bn}$', value=-120)

    col1, col2 = st.columns(2)

    with col1:
        v_cn_n = st.number_input('Magnitud $V_{cn}$', value=100)

    with col2:
        v_cn_a = st.number_input('Angulo de $V_{cn}$', value=-240)

    "## Selección Impedancias:"

    col1, col2, col3, col4= st.columns(4)

    with col1:
        z_an_r = st.number_input('Parte real de $Z_{an}$', value=40)

    with col2:
        z_an_i = st.number_input('Parte imaginaria de $Z_{an}$', value=15)

    with col3:
        z_bn_r = st.number_input('Parte real de $Z_{bn}$', value=35)

    with col4:
        z_bn_i = st.number_input('Parte imaginaria de $Z_{bn}$', value=-15)

    col1, col2 = st.columns(2)

    with col1:
        z_cn_r = st.number_input('Parte real de $Z_{cn}$', value=10)

    with col2:
        z_cn_i = st.number_input('Parte imaginaria de $Z_{cn}$', value=30)

    
    v_an: tuple = (v_an_n, v_an_a)
    v_bn: tuple = (v_bn_n, v_bn_a)
    v_cn: tuple = (v_cn_n, v_cn_a)

    v: tuple = (v_an, v_bn, v_cn)

    z_an: complex = complex(z_an_r, z_an_i)
    z_bn: complex = complex(z_bn_r, z_bn_i)
    z_cn: complex = complex(z_cn_r, z_cn_i)

    z: tuple = (z_an, z_bn, z_cn)

    i_fase, i_linea, v_fase, v_linea, n_corrimiento, s = estrella_estrella(v, z)

    "----------------------------------------------------------------------------"


    col1, col2 = st.columns(2)


    with col1:
        "### Corrientes de fase:"
        st.markdown("$Ian$ = {:.3f} ∡ {:.3f}".format(i_fase[0][0], i_fase[0][1]))
        st.markdown("$Ibn$ = {:.3f} ∡ {:.3f}".format(i_fase[1][0], i_fase[1][1]))
        st.markdown("$Icn$ = {:.3f} ∡ {:.3f}".format(i_fase[2][0], i_fase[2][1]))

        "### Corrientes de linea:"
        st.markdown("$IAa$ = {:.3f} ∡ {:.3f}".format(i_linea[0][0], i_linea[0][1]))
        st.markdown("$IBb$ = {:.3f} ∡ {:.3f}".format(i_linea[1][0], i_linea[1][1]))
        st.markdown("$ICc$ = {:.3f} ∡ {:.3f}".format(i_linea[2][0], i_linea[2][1]))

        st.markdown("Corrimiento del neutro: {:.3f} ∡ {:.3f}".format(n_corrimiento[0], n_corrimiento[1]))

    with col2:
        "### Tensiones de fase:"
        st.markdown("$Van$ = {:.3f} ∡ {:.3f}".format(v_fase[0][0], v_fase[0][1]))
        st.markdown("$Vbn$ = {:.3f} ∡ {:.3f}".format(v_fase[1][0], v_fase[1][1]))
        st.markdown("$Vcn$ = {:.3f} ∡ {:.3f}".format(v_fase[2][0], v_fase[2][1]))

        "### Tensiones de linea:"
        st.markdown("$VAB$ = {:.3f} ∡ {:.3f}".format(v_linea[0][0], v_linea[0][1]))
        st.markdown("$VBC$ = {:.3f} ∡ {:.3f}".format(v_linea[1][0], v_linea[1][1]))
        st.markdown("$VCA$ = {:.3f} ∡ {:.3f}".format(v_linea[2][0], v_linea[2][1]))

        st.markdown("$S$ = {:.3f} + i {:.3f}".format(s.real, s.imag))


    "----------------------------------------------------------------------------"
    graphs = st.selectbox(
    'Graficns: ',
    ('Corrientes de fase', 'Corrientes de linea', 'Tensiones de fase', 'Tensiones de linea'))

    if graphs == 'Corrientes de fase':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        corriente_an = lambda x: i_fase[0][0] * math.cos(math.radians(frecuency * x + i_fase[0][1]))
        corriente_bn = lambda x: i_fase[1][0] * math.cos(math.radians(frecuency * x + i_fase[1][1]))
        corriente_cn = lambda x: i_fase[2][0] * math.cos(math.radians(frecuency * x + i_fase[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        i_an_x = np.arange(0, rango, step)
        i_an_y = [corriente_an(i) for i in i_an_x]

        i_bn_x = np.arange(0, rango, step)
        i_bn_y = [corriente_bn(i) for i in i_bn_x]

        i_cn_x = np.arange(0, rango, step)
        i_cn_y = [corriente_cn(i) for i in i_cn_x]

        fig, ax = plt.subplots()
        ax.plot(i_an_x, i_an_y)
        ax.plot(i_bn_x, i_bn_y)
        ax.plot(i_cn_x, i_cn_y)
        
        plt.title('Corrientes de fase')
        plt.legend(['Ian', 'Ibn', 'Icn'])
        plt.grid(True)

        st.pyplot(fig)

    elif graphs == 'Corrientes de linea':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        corriente_aa = lambda x: i_linea[0][0] * math.cos(math.radians(frecuency * x + i_linea[0][1]))
        corriente_bb = lambda x: i_linea[1][0] * math.cos(math.radians(frecuency * x + i_linea[1][1]))
        corriente_cc = lambda x: i_linea[2][0] * math.cos(math.radians(frecuency * x + i_linea[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        i_aa_x = np.arange(0, rango, step)
        i_aa_y = [corriente_aa(i) for i in i_aa_x]

        i_bb_x = np.arange(0, rango, step)
        i_bb_y = [corriente_bb(i) for i in i_bb_x]

        i_cc_x = np.arange(0, rango, step)
        i_cc_y = [corriente_cc(i) for i in i_cc_x]

        fig, ax = plt.subplots()
        ax.plot(i_aa_x, i_aa_y)
        ax.plot(i_bb_x, i_bb_y)
        ax.plot(i_cc_x, i_cc_y)

        plt.title('Corrientes de linea')
        plt.legend(['IAa', 'IBb', 'ICc'])
        plt.grid(True)

        st.pyplot(fig)

    elif graphs == 'Tensiones de fase':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        tension_an = lambda x: v_fase[0][0] * math.cos(math.radians(frecuency * x + v_fase[0][1]))
        tension_bn = lambda x: v_fase[1][0] * math.cos(math.radians(frecuency * x + v_fase[1][1]))
        tension_cn = lambda x: v_fase[2][0] * math.cos(math.radians(frecuency * x + v_fase[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        v_an_x = np.arange(0, rango, step)
        v_an_y = [tension_an(i) for i in v_an_x]

        v_bn_x = np.arange(0, rango, step)
        v_bn_y = [tension_bn(i) for i in v_bn_x]

        v_cn_x = np.arange(0, rango, step)
        v_cn_y = [tension_cn(i) for i in v_cn_x]

        fig, ax = plt.subplots()
        ax.plot(v_an_x, v_an_y)
        ax.plot(v_bn_x, v_bn_y)
        ax.plot(v_cn_x, v_cn_y)

        plt.title('Tensiones de fase')
        plt.legend(['Van', 'Vbn', 'Vcn'])
        plt.grid(True)

        st.pyplot(fig)

    else:

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        tension_an = lambda x: v_linea[0][0] * math.cos(math.radians(frecuency * x + v_linea[0][1]))
        tension_bn = lambda x: v_linea[1][0] * math.cos(math.radians(frecuency * x + v_linea[1][1]))
        tension_cn = lambda x: v_linea[2][0] * math.cos(math.radians(frecuency * x + v_linea[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        v_an_x = np.arange(0, rango, step)
        v_an_y = [tension_an(i) for i in v_an_x]

        v_bn_x = np.arange(0, rango, step)
        v_bn_y = [tension_bn(i) for i in v_bn_x]

        v_cn_x = np.arange(0, rango, step)
        v_cn_y = [tension_cn(i) for i in v_cn_x]

        fig, ax = plt.subplots()
        ax.plot(v_an_x, v_an_y)
        ax.plot(v_bn_x, v_bn_y)
        ax.plot(v_cn_x, v_cn_y)

        plt.title('Tensiones de linea')
        plt.legend(['VAB', 'VBC', 'VCA'])
        plt.grid(True)

        st.pyplot(fig)


elif option == 'Delta-Estrella':

    image = Image.open("DistribucionDeltaEstrella.png")
    st.image(image, caption='Circuito trifasico Delta - Estrella')
    
    "## Selección voltajes:"

    col1, col2, col3, col4= st.columns(4)

    with col1:
        v_ab_n = st.number_input('Magnitud $V_{ab}$', value=100)

    with col2:
        v_ab_a = st.number_input('Angulo $V_{ab}$', value=0)

    with col3:
        v_bc_n = st.number_input('Magnitud $V_{bc}$', value=100)

    with col4:
        v_bc_a = st.number_input('Angulo $V_{bc}$', value=-120)

    col1, col2 = st.columns(2)

    with col1:
        v_ca_n = st.number_input('Magnitud $V_{ca}$', value=100)

    with col2:
        v_ca_a = st.number_input('Angulo de $V_{ca}$', value=-240)

    "## Selección Impedancias:"

    col1, col2, col3, col4= st.columns(4)

    with col1:
        z_an_r = st.number_input('Parte real de $Z_{an}$', value=40)

    with col2:
        z_an_i = st.number_input('Parte imaginaria de $Z_{an}$', value=15)

    with col3:
        z_bn_r = st.number_input('Parte real de $Z_{bn}$', value=35)

    with col4:
        z_bn_i = st.number_input('Parte imaginaria de $Z_{bn}$', value=-15)

    col1, col2 = st.columns(2)

    with col1:
        z_cn_r = st.number_input('Parte real de $Z_{cn}$', value=10)

    with col2:
        z_cn_i = st.number_input('Parte imaginaria de $Z_{cn}$', value=30)

    
    v_ab: tuple = (v_ab_n, v_ab_a)
    v_bc: tuple = (v_bc_n, v_bc_a)
    v_ca: tuple = (v_ca_n, v_ca_a)

    v: tuple = (v_ab, v_bc, v_ca)

    z_an: complex = complex(z_an_r, z_an_i)
    z_bn: complex = complex(z_bn_r, z_bn_i)
    z_cn: complex = complex(z_cn_r, z_cn_i)

    z: tuple = (z_an, z_bn, z_cn)

    i_fase, i_linea, v_fase, v_linea, n_corrimiento, s = delta_estrella(v, z)

    "----------------------------------------------------------------------------"


    col1, col2 = st.columns(2)


    with col1:
        "### Corrientes de fase:"
        st.markdown("$Ian$ = {:.3f} ∡ {:.3f}".format(i_fase[0][0], i_fase[0][1]))
        st.markdown("$Ibn$ = {:.3f} ∡ {:.3f}".format(i_fase[1][0], i_fase[1][1]))
        st.markdown("$Icn$ = {:.3f} ∡ {:.3f}".format(i_fase[2][0], i_fase[2][1]))

        "### Corrientes de linea:"
        st.markdown("$IAa$ = {:.3f} ∡ {:.3f}".format(i_linea[0][0], i_linea[0][1]))
        st.markdown("$IBb$ = {:.3f} ∡ {:.3f}".format(i_linea[1][0], i_linea[1][1]))
        st.markdown("$ICc$ = {:.3f} ∡ {:.3f}".format(i_linea[2][0], i_linea[2][1]))

        st.markdown("Corrimiento del neutro: {:.3f} ∡ {:.3f}".format(n_corrimiento[0], n_corrimiento[1]))


    with col2:
        "### Tensiones de fase:"
        st.markdown("$Van$ = {:.3f} ∡ {:.3f}".format(v_fase[0][0], v_fase[0][1]))
        st.markdown("$Vbn$ = {:.3f} ∡ {:.3f}".format(v_fase[1][0], v_fase[1][1]))
        st.markdown("$Vcn$ = {:.3f} ∡ {:.3f}".format(v_fase[2][0], v_fase[2][1]))

        "### Tensiones de linea:"
        st.markdown("$VAB$ = {:.3f} ∡ {:.3f}".format(v_linea[0][0], v_linea[0][1]))
        st.markdown("$VBC$ = {:.3f} ∡ {:.3f}".format(v_linea[1][0], v_linea[1][1]))
        st.markdown("$VCA$ = {:.3f} ∡ {:.3f}".format(v_linea[2][0], v_linea[2][1]))

        st.markdown("$S$ = {:.3f} + i {:.3f}".format(s.real, s.imag))

    "----------------------------------------------------------------------------"
    graphs = st.selectbox(
    'Graficns: ',
    ('Corrientes de fase', 'Corrientes de linea', 'Tensiones de fase', 'Tensiones de linea'))

    if graphs == 'Corrientes de fase':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        corriente_an = lambda x: i_fase[0][0] * math.cos(math.radians(frecuency * x + i_fase[0][1]))
        corriente_bn = lambda x: i_fase[1][0] * math.cos(math.radians(frecuency * x + i_fase[1][1]))
        corriente_cn = lambda x: i_fase[2][0] * math.cos(math.radians(frecuency * x + i_fase[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        i_an_x = np.arange(0, rango, step)
        i_an_y = [corriente_an(i) for i in i_an_x]

        i_bn_x = np.arange(0, rango, step)
        i_bn_y = [corriente_bn(i) for i in i_bn_x]

        i_cn_x = np.arange(0, rango, step)
        i_cn_y = [corriente_cn(i) for i in i_cn_x]

        fig, ax = plt.subplots()
        ax.plot(i_an_x, i_an_y)
        ax.plot(i_bn_x, i_bn_y)
        ax.plot(i_cn_x, i_cn_y)
        
        plt.title('Corrientes de fase')
        plt.legend(['Ian', 'Ibn', 'Icn'])
        plt.grid(True)

        st.pyplot(fig)

    elif graphs == 'Corrientes de linea':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        corriente_aa = lambda x: i_linea[0][0] * math.cos(math.radians(frecuency * x + i_linea[0][1]))
        corriente_bb = lambda x: i_linea[1][0] * math.cos(math.radians(frecuency * x + i_linea[1][1]))
        corriente_cc = lambda x: i_linea[2][0] * math.cos(math.radians(frecuency * x + i_linea[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        i_aa_x = np.arange(0, rango, step)
        i_aa_y = [corriente_aa(i) for i in i_aa_x]

        i_bb_x = np.arange(0, rango, step)
        i_bb_y = [corriente_bb(i) for i in i_bb_x]

        i_cc_x = np.arange(0, rango, step)
        i_cc_y = [corriente_cc(i) for i in i_cc_x]

        fig, ax = plt.subplots()
        ax.plot(i_aa_x, i_aa_y)
        ax.plot(i_bb_x, i_bb_y)
        ax.plot(i_cc_x, i_cc_y)

        plt.title('Corrientes de linea')
        plt.legend(['IAa', 'IBb', 'ICc'])
        plt.grid(True)

        st.pyplot(fig)

    elif graphs == 'Tensiones de fase':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        tension_an = lambda x: v_fase[0][0] * math.cos(math.radians(frecuency * x + v_fase[0][1]))
        tension_bn = lambda x: v_fase[1][0] * math.cos(math.radians(frecuency * x + v_fase[1][1]))
        tension_cn = lambda x: v_fase[2][0] * math.cos(math.radians(frecuency * x + v_fase[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        v_an_x = np.arange(0, rango, step)
        v_an_y = [tension_an(i) for i in v_an_x]

        v_bn_x = np.arange(0, rango, step)
        v_bn_y = [tension_bn(i) for i in v_bn_x]

        v_cn_x = np.arange(0, rango, step)
        v_cn_y = [tension_cn(i) for i in v_cn_x]

        fig, ax = plt.subplots()
        ax.plot(v_an_x, v_an_y)
        ax.plot(v_bn_x, v_bn_y)
        ax.plot(v_cn_x, v_cn_y)

        plt.title('Tensiones de fase')
        plt.legend(['Van', 'Vbn', 'Vcn'])
        plt.grid(True)

        st.pyplot(fig)

    else:

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        tension_an = lambda x: v_linea[0][0] * math.cos(math.radians(frecuency * x + v_linea[0][1]))
        tension_bn = lambda x: v_linea[1][0] * math.cos(math.radians(frecuency * x + v_linea[1][1]))
        tension_cn = lambda x: v_linea[2][0] * math.cos(math.radians(frecuency * x + v_linea[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        v_an_x = np.arange(0, rango, step)
        v_an_y = [tension_an(i) for i in v_an_x]

        v_bn_x = np.arange(0, rango, step)
        v_bn_y = [tension_bn(i) for i in v_bn_x]

        v_cn_x = np.arange(0, rango, step)
        v_cn_y = [tension_cn(i) for i in v_cn_x]

        fig, ax = plt.subplots()
        ax.plot(v_an_x, v_an_y)
        ax.plot(v_bn_x, v_bn_y)
        ax.plot(v_cn_x, v_cn_y)

        plt.title('Tensiones de linea')
        plt.legend(['VAB', 'VBC', 'VCA'])
        plt.grid(True)

        st.pyplot(fig)


elif option == 'Estrella-Delta':

    image = Image.open("DistribucionEstrellaDelta.png")
    st.image(image, caption='Circuito trifasico Estrella - Delta')

    "## Selección voltajes:"

    col1, col2, col3, col4= st.columns(4)

    with col1:
        v_an_n = st.number_input('Magnitud $V_{an}$', value=100)

    with col2:
        v_an_a = st.number_input('Angulo $V_{an}$', value=0)

    with col3:
        v_bn_n = st.number_input('Magnitud $V_{bn}$', value=100)

    with col4:
        v_bn_a = st.number_input('Angulo $V_{bn}$', value=-120)

    col1, col2 = st.columns(2)

    with col1:
        v_cn_n = st.number_input('Magnitud $V_{cn}$', value=100)

    with col2:
        v_cn_a = st.number_input('Angulo de $V_{cn}$', value=-240)

    "## Selección Impedancias:"

    col1, col2, col3, col4= st.columns(4)

    with col1:
        z_ab_r = st.number_input('Parte real de $Z_{ab}$', value=40)

    with col2:
        z_ab_i = st.number_input('Parte imaginaria de $Z_{ab}$', value=15)

    with col3:
        z_bc_r = st.number_input('Parte real de $Z_{bc}$', value=35)

    with col4:
        z_bc_i = st.number_input('Parte imaginaria de $Z_{bc}$', value=-15)

    col1, col2 = st.columns(2)

    with col1:
        z_ca_r = st.number_input('Parte real de $Z_{ca}$', value=10)

    with col2:
        z_ca_i = st.number_input('Parte imaginaria de $Z_{c}$', value=30)


    v_an: tuple = (v_an_n, v_an_a)
    v_bn: tuple = (v_bn_n, v_bn_a)
    v_cn: tuple = (v_cn_n, v_cn_a)

    v: tuple = (v_an, v_bn, v_cn)

    z_ab: complex = complex(z_ab_r, z_ab_i)
    z_bc: complex = complex(z_bc_r, z_bc_i)
    z_ca: complex = complex(z_ca_r, z_ca_i)

    z: tuple = (z_ab, z_bc, z_ca)

    i_fase, i_linea, v_fase, v_linea, s = estrella_delta(v, z)

    "----------------------------------------------------------------------------"


    col1, col2 = st.columns(2)


    with col1:
        "### Corrientes de fase:"
        st.markdown("$Ian$ = {:.3f} ∡ {:.3f}".format(i_fase[0][0], i_fase[0][1]))
        st.markdown("$Ibn$ = {:.3f} ∡ {:.3f}".format(i_fase[1][0], i_fase[1][1]))
        st.markdown("$Icn$ = {:.3f} ∡ {:.3f}".format(i_fase[2][0], i_fase[2][1]))

        "### Corrientes de linea:"
        st.markdown("$IAa$ = {:.3f} ∡ {:.3f}".format(i_linea[0][0], i_linea[0][1]))
        st.markdown("$IBb$ = {:.3f} ∡ {:.3f}".format(i_linea[1][0], i_linea[1][1]))
        st.markdown("$ICc$ = {:.3f} ∡ {:.3f}".format(i_linea[2][0], i_linea[2][1]))

        st.markdown("$S$ = {:.3f} + i {:.3f}".format(s.real, s.imag))

    with col2:
        "### Tensiones de fase:"
        st.markdown("$Van$ = {:.3f} ∡ {:.3f}".format(v_fase[0][0], v_fase[0][1]))
        st.markdown("$Vbn$ = {:.3f} ∡ {:.3f}".format(v_fase[1][0], v_fase[1][1]))
        st.markdown("$Vcn$ = {:.3f} ∡ {:.3f}".format(v_fase[2][0], v_fase[2][1]))

        "### Tensiones de linea:"
        st.markdown("$VAB$ = {:.3f} ∡ {:.3f}".format(v_linea[0][0], v_linea[0][1]))
        st.markdown("$VBC$ = {:.3f} ∡ {:.3f}".format(v_linea[1][0], v_linea[1][1]))
        st.markdown("$VCA$ = {:.3f} ∡ {:.3f}".format(v_linea[2][0], v_linea[2][1]))

    "----------------------------------------------------------------------------"
    graphs = st.selectbox(
    'Graficns: ',
    ('Corrientes de fase', 'Corrientes de linea', 'Tensiones de fase', 'Tensiones de linea'))

    if graphs == 'Corrientes de fase':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        corriente_an = lambda x: i_fase[0][0] * math.cos(math.radians(frecuency * x + i_fase[0][1]))
        corriente_bn = lambda x: i_fase[1][0] * math.cos(math.radians(frecuency * x + i_fase[1][1]))
        corriente_cn = lambda x: i_fase[2][0] * math.cos(math.radians(frecuency * x + i_fase[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        i_an_x = np.arange(0, rango, step)
        i_an_y = [corriente_an(i) for i in i_an_x]

        i_bn_x = np.arange(0, rango, step)
        i_bn_y = [corriente_bn(i) for i in i_bn_x]

        i_cn_x = np.arange(0, rango, step)
        i_cn_y = [corriente_cn(i) for i in i_cn_x]

        fig, ax = plt.subplots()
        ax.plot(i_an_x, i_an_y)
        ax.plot(i_bn_x, i_bn_y)
        ax.plot(i_cn_x, i_cn_y)
        
        plt.title('Corrientes de fase')
        plt.legend(['Ian', 'Ibn', 'Icn'])
        plt.grid(True)

        st.pyplot(fig)

    elif graphs == 'Corrientes de linea':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        corriente_aa = lambda x: i_linea[0][0] * math.cos(math.radians(frecuency * x + i_linea[0][1]))
        corriente_bb = lambda x: i_linea[1][0] * math.cos(math.radians(frecuency * x + i_linea[1][1]))
        corriente_cc = lambda x: i_linea[2][0] * math.cos(math.radians(frecuency * x + i_linea[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        i_aa_x = np.arange(0, rango, step)
        i_aa_y = [corriente_aa(i) for i in i_aa_x]

        i_bb_x = np.arange(0, rango, step)
        i_bb_y = [corriente_bb(i) for i in i_bb_x]

        i_cc_x = np.arange(0, rango, step)
        i_cc_y = [corriente_cc(i) for i in i_cc_x]

        fig, ax = plt.subplots()
        ax.plot(i_aa_x, i_aa_y)
        ax.plot(i_bb_x, i_bb_y)
        ax.plot(i_cc_x, i_cc_y)

        plt.title('Corrientes de linea')
        plt.legend(['IAa', 'IBb', 'ICc'])
        plt.grid(True)

        st.pyplot(fig)

    elif graphs == 'Tensiones de fase':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        tension_an = lambda x: v_fase[0][0] * math.cos(math.radians(frecuency * x + v_fase[0][1]))
        tension_bn = lambda x: v_fase[1][0] * math.cos(math.radians(frecuency * x + v_fase[1][1]))
        tension_cn = lambda x: v_fase[2][0] * math.cos(math.radians(frecuency * x + v_fase[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        v_an_x = np.arange(0, rango, step)
        v_an_y = [tension_an(i) for i in v_an_x]

        v_bn_x = np.arange(0, rango, step)
        v_bn_y = [tension_bn(i) for i in v_bn_x]

        v_cn_x = np.arange(0, rango, step)
        v_cn_y = [tension_cn(i) for i in v_cn_x]

        fig, ax = plt.subplots()
        ax.plot(v_an_x, v_an_y)
        ax.plot(v_bn_x, v_bn_y)
        ax.plot(v_cn_x, v_cn_y)

        plt.title('Tensiones de fase')
        plt.legend(['Van', 'Vbn', 'Vcn'])
        plt.grid(True)

        st.pyplot(fig)

    else:

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        tension_an = lambda x: v_linea[0][0] * math.cos(math.radians(frecuency * x + v_linea[0][1]))
        tension_bn = lambda x: v_linea[1][0] * math.cos(math.radians(frecuency * x + v_linea[1][1]))
        tension_cn = lambda x: v_linea[2][0] * math.cos(math.radians(frecuency * x + v_linea[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        v_an_x = np.arange(0, rango, step)
        v_an_y = [tension_an(i) for i in v_an_x]

        v_bn_x = np.arange(0, rango, step)
        v_bn_y = [tension_bn(i) for i in v_bn_x]

        v_cn_x = np.arange(0, rango, step)
        v_cn_y = [tension_cn(i) for i in v_cn_x]

        fig, ax = plt.subplots()
        ax.plot(v_an_x, v_an_y)
        ax.plot(v_bn_x, v_bn_y)
        ax.plot(v_cn_x, v_cn_y)

        plt.title('Tensiones de linea')
        plt.legend(['VAB', 'VBC', 'VCA'])
        plt.grid(True)

        st.pyplot(fig)


else:

    image = Image.open("DistribucionEstrellaEstrella3Hilos.png")
    st.image(image, caption='Circuito trifasico Estrella - Estrella 3 hilos')
    
    "## Selección voltajes:"

    col1, col2, col3, col4= st.columns(4)

    with col1:
        v_an_n = st.number_input('Magnitud $V_{an}$', value=100)

    with col2:
        v_an_a = st.number_input('Angulo $V_{an}$', value=0)

    with col3:
        v_bn_n = st.number_input('Magnitud $V_{bn}$', value=100)

    with col4:
        v_bn_a = st.number_input('Angulo $V_{bn}$', value=-120)

    col1, col2 = st.columns(2)

    with col1:
        v_cn_n = st.number_input('Magnitud $V_{cn}$', value=100)

    with col2:
        v_cn_a = st.number_input('Angulo de $V_{cn}$', value=-240)

    "## Selección Impedancias:"

    col1, col2, col3, col4= st.columns(4)

    with col1:
        z_an_r = st.number_input('Parte real de $Z_{an}$', value=40)

    with col2:
        z_an_i = st.number_input('Parte imaginaria de $Z_{an}$', value=15)

    with col3:
        z_bn_r = st.number_input('Parte real de $Z_{bn}$', value=35)

    with col4:
        z_bn_i = st.number_input('Parte imaginaria de $Z_{bn}$', value=-15)

    col1, col2 = st.columns(2)

    with col1:
        z_cn_r = st.number_input('Parte real de $Z_{cn}$', value=10)

    with col2:
        z_cn_i = st.number_input('Parte imaginaria de $Z_{cn}$', value=30)

    
    v_an: tuple = (v_an_n, v_an_a)
    v_bn: tuple = (v_bn_n, v_bn_a)
    v_cn: tuple = (v_cn_n, v_cn_a)

    v: tuple = (v_an, v_bn, v_cn)

    z_an: complex = complex(z_an_r, z_an_i)
    z_bn: complex = complex(z_bn_r, z_bn_i)
    z_cn: complex = complex(z_cn_r, z_cn_i)

    z: tuple = (z_an, z_bn, z_cn)

    i_fase, i_linea, v_fase, v_linea, n_corrimiento, s = estrella_estrella_3hilos(v, z)

    "----------------------------------------------------------------------------"


    col1, col2 = st.columns(2)


    with col1:
        "### Corrientes de fase:"
        st.markdown("$Ian$ = {:.3f} ∡ {:.3f}".format(i_fase[0][0], i_fase[0][1]))
        st.markdown("$Ibn$ = {:.3f} ∡ {:.3f}".format(i_fase[1][0], i_fase[1][1]))
        st.markdown("$Icn$ = {:.3f} ∡ {:.3f}".format(i_fase[2][0], i_fase[2][1]))

        "### Corrientes de linea:"
        st.markdown("$IAa$ = {:.3f} ∡ {:.3f}".format(i_linea[0][0], i_linea[0][1]))
        st.markdown("$IBb$ = {:.3f} ∡ {:.3f}".format(i_linea[1][0], i_linea[1][1]))
        st.markdown("$ICc$ = {:.3f} ∡ {:.3f}".format(i_linea[2][0], i_linea[2][1]))

        st.markdown("Corrimiento del neutro: {:.3f} ∡ {:.3f}".format(n_corrimiento[0], n_corrimiento[1]))


    with col2:
        "### Tensiones de fase:"
        st.markdown("$Van$ = {:.3f} ∡ {:.3f}".format(v_fase[0][0], v_fase[0][1]))
        st.markdown("$Vbn$ = {:.3f} ∡ {:.3f}".format(v_fase[1][0], v_fase[1][1]))
        st.markdown("$Vcn$ = {:.3f} ∡ {:.3f}".format(v_fase[2][0], v_fase[2][1]))

        "### Tensiones de linea:"
        st.markdown("$VAB$ = {:.3f} ∡ {:.3f}".format(v_linea[0][0], v_linea[0][1]))
        st.markdown("$VBC$ = {:.3f} ∡ {:.3f}".format(v_linea[1][0], v_linea[1][1]))
        st.markdown("$VCA$ = {:.3f} ∡ {:.3f}".format(v_linea[2][0], v_linea[2][1]))

        st.markdown("$S$ = {:.3f} + i {:.3f}".format(s.real, s.imag))

    "----------------------------------------------------------------------------"
    graphs = st.selectbox(
    'Graficns: ',
    ('Corrientes de fase', 'Corrientes de linea', 'Tensiones de fase', 'Tensiones de linea'))

    if graphs == 'Corrientes de fase':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        corriente_an = lambda x: i_fase[0][0] * math.cos(math.radians(frecuency * x + i_fase[0][1]))
        corriente_bn = lambda x: i_fase[1][0] * math.cos(math.radians(frecuency * x + i_fase[1][1]))
        corriente_cn = lambda x: i_fase[2][0] * math.cos(math.radians(frecuency * x + i_fase[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        i_an_x = np.arange(0, rango, step)
        i_an_y = [corriente_an(i) for i in i_an_x]

        i_bn_x = np.arange(0, rango, step)
        i_bn_y = [corriente_bn(i) for i in i_bn_x]

        i_cn_x = np.arange(0, rango, step)
        i_cn_y = [corriente_cn(i) for i in i_cn_x]

        fig, ax = plt.subplots()
        ax.plot(i_an_x, i_an_y)
        ax.plot(i_bn_x, i_bn_y)
        ax.plot(i_cn_x, i_cn_y)
        
        plt.title('Corrientes de fase')
        plt.legend(['Ian', 'Ibn', 'Icn'])
        plt.grid(True)

        st.pyplot(fig)

    elif graphs == 'Corrientes de linea':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        corriente_aa = lambda x: i_linea[0][0] * math.cos(math.radians(frecuency * x + i_linea[0][1]))
        corriente_bb = lambda x: i_linea[1][0] * math.cos(math.radians(frecuency * x + i_linea[1][1]))
        corriente_cc = lambda x: i_linea[2][0] * math.cos(math.radians(frecuency * x + i_linea[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        i_aa_x = np.arange(0, rango, step)
        i_aa_y = [corriente_aa(i) for i in i_aa_x]

        i_bb_x = np.arange(0, rango, step)
        i_bb_y = [corriente_bb(i) for i in i_bb_x]

        i_cc_x = np.arange(0, rango, step)
        i_cc_y = [corriente_cc(i) for i in i_cc_x]

        fig, ax = plt.subplots()
        ax.plot(i_aa_x, i_aa_y)
        ax.plot(i_bb_x, i_bb_y)
        ax.plot(i_cc_x, i_cc_y)

        plt.title('Corrientes de linea')
        plt.legend(['IAa', 'IBb', 'ICc'])
        plt.grid(True)

        st.pyplot(fig)

    elif graphs == 'Tensiones de fase':

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        tension_an = lambda x: v_fase[0][0] * math.cos(math.radians(frecuency * x + v_fase[0][1]))
        tension_bn = lambda x: v_fase[1][0] * math.cos(math.radians(frecuency * x + v_fase[1][1]))
        tension_cn = lambda x: v_fase[2][0] * math.cos(math.radians(frecuency * x + v_fase[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        v_an_x = np.arange(0, rango, step)
        v_an_y = [tension_an(i) for i in v_an_x]

        v_bn_x = np.arange(0, rango, step)
        v_bn_y = [tension_bn(i) for i in v_bn_x]

        v_cn_x = np.arange(0, rango, step)
        v_cn_y = [tension_cn(i) for i in v_cn_x]

        fig, ax = plt.subplots()
        ax.plot(v_an_x, v_an_y)
        ax.plot(v_bn_x, v_bn_y)
        ax.plot(v_cn_x, v_cn_y)

        plt.title('Tensiones de fase')
        plt.legend(['Van', 'Vbn', 'Vcn'])
        plt.grid(True)

        st.pyplot(fig)

    else:

        frecuency = st.slider('Seleccione la frecuencia: ', 0.00, 100.00, 50.00)

        tension_an = lambda x: v_linea[0][0] * math.cos(math.radians(frecuency * x + v_linea[0][1]))
        tension_bn = lambda x: v_linea[1][0] * math.cos(math.radians(frecuency * x + v_linea[1][1]))
        tension_cn = lambda x: v_linea[2][0] * math.cos(math.radians(frecuency * x + v_linea[2][1]))

        rango = st.slider('Seleccione el valor maximo de x: ', 0.00, 100.00, 50.00)
        step = 0.001

        v_an_x = np.arange(0, rango, step)
        v_an_y = [tension_an(i) for i in v_an_x]

        v_bn_x = np.arange(0, rango, step)
        v_bn_y = [tension_bn(i) for i in v_bn_x]

        v_cn_x = np.arange(0, rango, step)
        v_cn_y = [tension_cn(i) for i in v_cn_x]

        fig, ax = plt.subplots()
        ax.plot(v_an_x, v_an_y)
        ax.plot(v_bn_x, v_bn_y)
        ax.plot(v_cn_x, v_cn_y)

        plt.title('Tensiones de linea')
        plt.legend(['VAB', 'VBC', 'VCA'])
        plt.grid(True)

        st.pyplot(fig)