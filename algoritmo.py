#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#######################################
# Script que procesa la información del WRF
# para generar el pronóstico de las estaciones
# del Estado de Chihuahua
# Author: Jorge Mauricio
# Email: jorge.ernesto.mauricio@gmail.com
# Date: Created on Thu Sep 28 08:38:15 2017
# Version: 1.0
#######################################
"""

# librerías
import os
import pandas as pd
import numpy as np
import requests
import time
from time import gmtime, strftime

# class datos
class Punto:
    def __init__(self, tx1, tn1, tx2, tn2, tx3, tn3, tx4, tn4, tx5, tn5, distancia):
        # v1
        self.tx1 = tx1
        self.tn1 = tn1

        # v2
        self.tx2 = tx2
        self.tn2 = tn2

        # v3
        self.tx3 = tx3
        self.tn3 = tn3

        # v4
        self.tx4 = tx4
        self.tn4 = tn4

        # v5
        self.tx5 = tx5
        self.tn5 = tn5

        self.distancia = distancia

# funciones
# función interpolación
def generar_interpolacion(punto1, punto2, punto3):
    """
    Generar el valor de inteporlación de los tres puntos más
    cercanos a la posición de la estación
    param: punto1: objeto del primer punto encontrado
    param: punto2: objeto del primer punto encontrado
    param: punto3: objeto del primer punto encontrado
    """
    # valor de la constante k
    k = 2.0

    print(repr(punto1.distancia))
    print(repr(punto2.distancia))
    print(repr(punto3.distancia))

    # calcular la suma inversa
    suma_inversa =  (1 / punto1.distancia) ** k + (1 / punto2.distancia) ** k + (1 / punto3.distancia) ** k

    # calcular los valores para w1, w2, w3
    w1 = 1 / (punto1.distancia ** k) / suma_inversa
    w2 = 1 / (punto2.distancia ** k) / suma_inversa
    w3 = 1 / (punto3.distancia ** k) / suma_inversa

    # calcular valor de z_tmax1 y z_tmin1
    z_tmax1 = (w1 * punto1.tx1) + (w2 * punto2.tx1) + (w3 * punto3.tx1)
    z_tmin1 = (w1 * punto1.tn1) + (w2 * punto2.tn1) + (w3 * punto3.tn2)

    # calcular valor de z_tmax2 y z_tmin2
    z_tmax2 = (w1 * punto1.tx2) + (w2 * punto2.tx2) + (w3 * punto3.tx2)
    z_tmin2 = (w1 * punto1.tn2) + (w2 * punto2.tn2) + (w3 * punto3.tn2)

    # calcular valor de z_tmax3 y z_tmin3
    z_tmax3 = (w1 * punto1.tx3) + (w2 * punto2.tx3) + (w3 * punto3.tx3)
    z_tmin3 = (w1 * punto1.tn3) + (w2 * punto2.tn3) + (w3 * punto3.tn3)

    # calcular valor de z_tmax4 y z_tmin4
    z_tmax4 = (w1 * punto1.tx4) + (w2 * punto2.tx4) + (w3 * punto3.tx4)
    z_tmin4 = (w1 * punto1.tn4) + (w2 * punto2.tn4) + (w3 * punto3.tn4)

    # calcular valor de z_tmax5 y z_tmin5
    z_tmax5 = (w1 * punto1.tx5) + (w2 * punto2.tx5) + (w3 * punto3.tx5)
    z_tmin5 = (w1 * punto1.tn5) + (w2 * punto2.tn5) + (w3 * punto3.tn5)

    return z_tmax1, z_tmin1, z_tmax2, z_tmin2, z_tmax3, z_tmin3, z_tmax4, z_tmin4, z_tmax5, z_tmin5

def calcular_distancia_entre_puntos(x1, x2, y1, y2):
    """
    Calcular la distancia entre dos puntos
    param: x1: longitud punto 1
    param: x2: longitud punto 2
    param: y1: latitud punto 1
    param: y2: latitud punto 2
    """
    xi = (x2 - x1) ** 2
    yi = (y2 - y1) ** 2
    return (xi + yi) ** (1/2)

# límites Chihuahua
LONG_MAX = -102.77
LONG_MIN = -109.52
LAT_MAX  = 32.02
LAT_MIN  = 25.48

# path
PATH = '/home/jorge/Documents/Research/procesamiento_chihuahua'

# fecha pronóstico
fechaPronostico = strftime("%Y-%m-%d")

# cambiar de folder
os.chdir("{}/data/{}".format(PATH, fechaPronostico))

# crear el data frame
df = pd.DataFrame()

# ciclo de procesamiento tmax y tmin
for i in range(1,6):
    dfTemp = pd.read_csv("d{}.txt".format(i))
    df["Tmax{}".format(i)] = dfTemp["Tmax"]
    df["Tmin{}".format(i)] = dfTemp["Tmin"]

# adquirir las lats y lons
df["lats"] = dfTemp["Lat"]
df["lons"] = dfTemp["Long"]

print(df.head())

# determinar el área de Chihuahua
df = df.where((df["lats"] > LAT_MIN) & \
              (df["lats"] < LAT_MAX) & \
              (df["lons"] > LONG_MIN) & \
              (df["lons"] < LONG_MAX)).dropna()

# leer csv de estaciones Chihuahua
df_estaciones = pd.read_csv("/home/jorge/Documents/Research/procesamiento_chihuahua/data/estaciones.csv")

isPrimerDistancia = True

# ciclo de estaciones
for index, row in df_estaciones.iterrows():
    # ciclo de información para datos WRF
    for indexWRF, rowWRF in df.iterrows():
        if isPrimerDistancia:
            # iniciar los puntos
            p1 = Punto(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
            p2 = Punto(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
            p3 = Punto(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
            # actualizar distancia
            p1.distancia = calcular_distancia_entre_puntos(row["Longitud"],
                                                           rowWRF["lons"],
                                                           row["Latitud"],
                                                           rowWRF["lats"])

            p2.distancia = calcular_distancia_entre_puntos(row["Longitud"],
                                                           rowWRF["lons"],
                                                           row["Latitud"],
                                                           rowWRF["lats"])

            p3.distancia = calcular_distancia_entre_puntos(row["Longitud"],
                                                           rowWRF["lons"],
                                                           row["Latitud"],
                                                           rowWRF["lats"])

            print("***** latitudes y longitudes",row["Longitud"], rowWRF["lons"], row["Latitud"], rowWRF["lats"])

            # actualizar temperatura max y min
            p1.temperatura_max = rowWRF["Tmax1"]
            p1.temperatura_min = rowWRF["Tmin1"]

            isPrimerDistancia = False

        else:
            dTemp = calcular_distancia_entre_puntos(row["Longitud"],
                                                    rowWRF["lons"],
                                                    row["Latitud"],
                                                    rowWRF["lats"])

            # comparar
            if dTemp < p1.distancia:
                # actualizar distancia
                p3.distancia = p2.distancia
                p2.distancia = p1.distancia
                p1.distancia = dTemp

                # actualizar temperatura max1 y min1
                p3.tx1 = p2.tx1
                p2.tx1 = p1.tx1
                p1.tx1 = rowWRF["Tmax1"]

                p3.tn1 = p2.tn1
                p2.tn1 = p1.tn1
                p1.tn1 = rowWRF["Tmin1"]

                # actualizar temperatura max2 y min2
                p3.tx2 = p2.tx2
                p2.tx2 = p1.tx2
                p1.tx2 = rowWRF["Tmax2"]

                p3.tn2 = p2.tn2
                p2.tn2 = p1.tn2
                p1.tn2 = rowWRF["Tmin2"]

                # actualizar temperatura max3 y min3
                p3.tx3 = p2.tx3
                p2.tx3 = p1.tx3
                p1.tx3 = rowWRF["Tmax3"]

                p3.tn3 = p2.tn3
                p2.tn3 = p1.tn3
                p1.tn3 = rowWRF["Tmin3"]

                # actualizar temperatura max4 y min4
                p3.tx4 = p2.tx4
                p2.tx4 = p1.tx4
                p1.tx4 = rowWRF["Tmax4"]

                p3.tn4 = p2.tn4
                p2.tn4 = p1.tn4
                p1.tn4 = rowWRF["Tmin4"]

                # actualizar temperatura max1 y min1
                p3.tx5 = p2.tx5
                p2.tx5 = p1.tx5
                p1.tx5 = rowWRF["Tmax5"]

                p3.tn5 = p2.tn5
                p2.tn5 = p1.tn5
                p1.tn5 = rowWRF["Tmin5"]

            elif dTemp > p2.distancia and dTemp < p3.distancia:
                # actualizar distancia
                p3.distancia = p2.distancia
                p2.distancia = dTemp

                # actualizar temperatura max1 y min1
                p3.tx1 = p2.tx1
                p2.tx1 = rowWRF["Tmax1"]

                p3.tn1 = p2.tn1
                p2.tn1 =rowWRF["Tmin1"]

                # actualizar temperatura max2 y min2
                p3.tx2 = p2.tx2
                p2.tx2 = rowWRF["Tmax2"]

                p3.tn2 = p2.tn2
                p2.tn2 =rowWRF["Tmin2"]

                # actualizar temperatura max3 y min3
                p3.tx3 = p2.tx3
                p2.tx3 = rowWRF["Tmax3"]

                p3.tn3 = p2.tn3
                p2.tn3 =rowWRF["Tmin3"]

                # actualizar temperatura max4 y min4
                p3.tx4 = p2.tx4
                p2.tx4 = rowWRF["Tmax4"]

                p3.tn4 = p2.tn4
                p2.tn4 =rowWRF["Tmin4"]

                # actualizar temperatura max5 y min5
                p3.tx5 = p2.tx5
                p2.tx5 = rowWRF["Tmax5"]

                p3.tn5 = p2.tn5
                p2.tn5 =rowWRF["Tmin5"]

            elif dTemp < p3.distancia:
                # actualizar distancia
                p3.distancia = dTemp

                # actualizar temperatura 1 max y min
                p3.tx1 = rowWRF["Tmax1"]
                p3.tn1 =rowWRF["Tmin1"]

                # actualizar temperatura 2 max y min
                p3.tx2 = rowWRF["Tmax2"]
                p3.tn2 =rowWRF["Tmin2"]

                # actualizar temperatura 3 max y min
                p3.tx3 = rowWRF["Tmax3"]
                p3.tn3 =rowWRF["Tmin3"]

                # actualizar temperatura 4 max y min
                p3.tx4 = rowWRF["Tmax4"]
                p3.tn4 =rowWRF["Tmin4"]

                # actualizar temperatura 5 max y min
                p3.tx5 = rowWRF["Tmax5"]
                p3.tn5 =rowWRF["Tmin5"]

            else:
                pass

    # reiniciar isPrimerDistancia
    isPrimerDistancia = True

    # calcular intepolación a la estación
    z_tx1, z_tn1,z_tx2, z_tn2,z_tx3, z_tn3,z_tx4, z_tn4,z_tx5, z_tn5 = generar_interpolacion(p1, p2, p3)
    print("Estacion: ", row["Nombre"])
    print("Latutid: {}\nLongitud: {}".format(row["Latitud"], row["Longitud"]))
    print("Tmax1: ", z_tx1)
    print("Tmin1: ", z_tn1)
    print("Tmax2: ", z_tx2)
    print("Tmin2: ", z_tn2)
    print("Tmax3: ", z_tx3)
    print("Tmin3: ", z_tn3)
    print("Tmax4: ", z_tx4)
    print("Tmin4: ", z_tn4)
    print("Tmax5: ", z_tx5)
    print("Tmin5: ", z_tn5)
    print("Distancia1: ", p1.distancia)
    print("Distancia2: ", p2.distancia)
    print("Distancia3: ", p3.distancia)
    print("\n")
