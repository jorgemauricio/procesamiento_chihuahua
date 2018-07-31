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
import schedule

# límites Chihuahua
LONG_MAX = -102.77
LONG_MIN = -109.52
LAT_MAX  = 32.02
LAT_MIN  = 25.48

# path
PATH = 'home/jorge/Documents/Research/procesamiento_chihuahua/'

# fecha pronóstico
fechaPronostico = strftime("%Y-%m-%d")

# cambiar de folder
os.chdir("{}/data/{}".format(PATH, fechaPronostico))

# crear el data frame
df = pd.DataFrame()

# ciclo de procesamiento tmax y tmin
for i in range(1,6):
    dfTemp = pd.read_csv("data/d{}.txt".format(i))
    df["Tmax{}".format(i)] = dfTemp["Tmax"]
    df["Tmin{}".format(i)] = dfTemp["Tmin"]

# adquirir las lats y lons
df["lats"] = dfTemp["Lat"]
df["lons"] = dfTemp["Long"]

# determinar el área de Chihuahua
df = df.where((df["lats"] > LAT_MIN) & \
              (df["lats"] < LAT_MAX) & \
              (df["lons"] > LONG_MIN) & \
              (df["lons"] < LONG_MAX)).dropna()

# leer csv de estaciones Chihuahua
df_estaciones = pd.read_csv("data/estaciones.csv")

# ciclo de verificación
x_1 = 0.0
x_2 = 0.0
x_3 = 0.0

# Y
y_1 = 0.0
y_2 = 0.0
y_3 = 0.0

# distancia
d1 = 0.0
d2 = 0.0
d3 = 0.0
isPrimerDistancia = True

# ciclo de estaciones
for index, row in df_estaciones.iterrows():
        for indexWRF, rowWRF in df.iterrows():
            if isPrimerDistancia:
                d1 = distancia(row["Longitud"],
                               rowWRF["lons"],
                               row["Latitud"],
                               row["lats"])
                d2 = d1
                d3 = d1
            else:
                dTemp = distancia(row["Longitud"],
                               rowWRF["lons"],
                               row["Latitud"],
                               rowWRF["lats"])

                # comparar
                if dTemp < d1:
                    d3 = d2
                    d2 = d1
                    d1 = dTemp
                elif dTemp > d2 and dTemp < d3:
                    d3 = d2
                    d2 = dTemp
                else:
                    d3 = dTemp

        # calcular intepolación a la estación
        
# función interpolación
def generar_interpolacion(x1, x2, x3, y1, y2i, y3, t1, t2, t3, xi, yi):
    """
    Generar el valor de inteporlación de los tres puntos más
    cercanos a la posición de la estación
    param: x1: longitud 1
    param: x2: longitud 2
    param: x3: longitud 3
    param: y1: latitud 1
    param: y2: latitud 2
    param: y3: latitud 3
    param: t1: temperatura 1
    param: t2: temperatura 2
    param: t3: temperatura 3
    """
    pass

def distancia(x1, x2, y1, y2):
    """
    Calcular la distancia entre dos puntos
    param: x1: longitud punto 1
    param: x2: longitud punto 2
    param: y1: latitud punto 1
    param: y2: latitud punto 2
    """
    xi = (x2 - x1) ** 2
    yi = (y2 - y1) ** 2
    return (xi * yi) ** (1/2)
