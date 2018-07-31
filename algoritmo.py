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

# path
PATH = 'home/jorge/Documents/Research/procesamiento_chihuahua/'

# fecha pronóstico
fechaPronostico = strftime("%Y-%m-%d")

# cambiar de folder
os.chdir("{}/data/{}".format(PATH, fechaPronostico))

# ciclo de procesamiento
for i in range(1,6):
