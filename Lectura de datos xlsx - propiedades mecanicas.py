# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 17:16:49 2022

@author: Luca
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import re

#data=pd.read_excel("S6F3P1.xlsx",skiprows=25,names=['n1','cantidad','tiempo','distancia','carga','n2','n3'])
#plt.plot(data['distancia'], data['carga'])

#%%
'''
#Lectura de datos
#Poner el directorio que contiene las carpetas a leer
archivos = os.listdir("F3")
for i in range (len(archivos)):
    data=pd.read_excel("F3\\"+archivos[i],skiprows=23,names=['n1','cantidad','tiempo','distancia','carga','n2','n3'])
    name=str(archivos[i])
    Name = name.replace('.xlsx', '')
    plt.plot(data['distancia'], data['carga'], label=Name)
    plt.xlabel('Estiramiento (mm)')
    plt.ylabel('Carga (N)')
    plt.title('Sistema 7F3')
    plt.legend()
'''  
#%%
'''
Defino las matrices con los anchos y espesores de cada pieza estudiada. Estas matrices
corresponden a todas las piezas que se estudiaron.
'''  
M6 = [[str('S6F3P1'),6.7,0.32],[str('S6F3P2'),7.3,0.32],[str('S6F3P3'),6.3,0.32],[str('S6F3P4'),6.4,0.32],[str('S6F3P5'),6.5,0.33],[str('S6F3P6'),6.8,0.33],[str('S6F4P7'),6.9,0.35],[str('S6F4P8'),6.5,0.35],[str('S6F4P9'),6.8,0.38],[str('S6F4P10'),6.7,0.34]]
M7 = [[str('S7F3P1'),6.5,0.33],[str('S7F3P2'),6.4,0.33],[str('S7F3P3'),6.5,0.38],[str('S7F2P4'),6.5,0.40],[str('S7F2P5'),6.5,0.40],[str('S7F2P6'),6.3,0.36],[str('S7F2P7'),6.7,0.36],[str('S7F2P8'),6.2,0.34],[str('S7F3P9'),6.5,0.40],[str('S7F3P10'),6.5,0.40],[str('S7F1P11'),6.3,0.46]]
M8 = [[str('S8F2P1'),6.5,0.50],[str('S8F2P2'),6.5,0.50],[str('S8F2P3'),6.5,0.40],[str('S8F3P4'),6.4,0.45],[str('S8F4P5'),6.5,0.54],[str('S8F4P6'),6.4,0.54],[str('S8F4P7'),6.3,0.54],[str('S8F4P8'),6.7,0.40]]

#%%
'''
Acá reescribo las matrices luego de eliminar piezas para favorecer un mejor análisis.
'''
    
M6 = [[str('S6F3P3'),6.3,0.32],[str('S6F3P4'),6.4,0.32],[str('S6F3P5'),6.5,0.33],[str('S6F4P9'),6.8,0.38],[str('S6F4P10'),6.7,0.34]]
M7 = [[str('S7F3P2'),6.4,0.33],[str('S7F3P3'),6.5,0.38],[str('S7F2P8'),6.2,0.34],[str('S7F3P9'),6.5,0.40],[str('S7F1P11'),6.3,0.46]]
M8 = [[str('S8F2P2'),6.5,0.50],[str('S8F2P3'),6.5,0.40],[str('S8F4P5'),6.5,0.54],[str('S8F4P7'),6.3,0.54],[str('S8F4P8'),6.7,0.40]]
MI = [[str('S6F3P4'),6.4,0.32],[str('S7F2P4'),6.5,0.40],[str('S8F2P2'),6.5,0.50]]
#%%
'''
En este bloque vamos a seleccionar los archivos .xlsx de una carpeta en el directorio,
los vamos a reescalear empleando las matrices previas y vamos a extraer, de cada gráfico,
el valor máximo de tensión y el alarg. porcentual que corresponde a dicho valor de tensión.
Para una explicación más detallada del código se puede ver el siguiente bloque, que 
contiene casi todo lo de este y más.
'''
Lo=35
archivos = os.listdir("GI")
M=[]
Est=[]
for i in range (len(archivos)):
    data=pd.read_excel("GI\\"+archivos[i],skiprows=23,names=['n1','cantidad','tiempo','distancia','carga','n2','n3'])
    name=str(archivos[i])
    Name = name.replace('.xlsx', '')
    for j in range(len(archivos)):
        if Name==MI[j][0]:
            sigma=data['carga']/(MI[j][1]*MI[j][2])
    epsilon=data['distancia']*100/Lo
    M.append(np.max(sigma)) #Agregamos en el vector vacío el valor máximo de sigma para cada iteración
    indice=np.where(sigma==np.max(sigma))[0][0] #Buscamos el índice que corresponde
    Est.append(epsilon[indice]) #Agregamos el valor de alarg. porc. que corresponde al valor máximo
    plt.plot(epsilon, sigma,label='Sistema '+Name[1])
    '''
    plt.text(0,1.9, r'Tensión máxima promedio:')
    plt.text(0,1.8, r'$\sigma_{Max}=(1.4\pm0.4) MPa$')
    plt.text(0,1.7, r'Alarg. máx. prom.:')
    plt.text(0,1.6, r'$\epsilon=100\pm50$')
    '''
    plt.xlabel('Estiramiento porcentual')
    plt.ylabel('Tensión (MPa)')
    #plt.title('Sistema 8: 80:20')
    plt.legend()
#print(M)
print(np.mean(M))
print(np.std(M))
#print(Est)
print(np.mean(Est))
print(np.std(Est))
#%%
'''
En este bloque vamos a agarrar los archivos .xlsx de alguna carpeta en el directorio,
vamos a graficar los primeros N puntos y le vamos a realizar un ajuste lineal. Primero,
como en general, vamos a normalizar los datos según queremos, es decir, reescaleamos
la carga en tensión y la distancia en alargamiento porcentual. Para ello empleamos las
matrices previamente definidas.
'''
def Lin(T, a, b): #Definimos el modelo lineal
    return a*T+b
from scipy.optimize import curve_fit,least_squares
x=np.linspace(0,.3,100) #Tira de números para el ajuste
p0=[0,0] #Parámetros iniciales para empezar a ajustar
N=10 #Número de primeros puntos para tomar de las curvas
E=[] #Vector de estiramiento vacío para cargar los primeros puntos
S=[] #Vector de tensión vacío para cargar los primeros puntos
Y=[] #Vector de módulo de Young para tomar media y std
archivos = os.listdir("S7t") #Cargamos los archivos de la carpeta seleccionada
for i in range(len(archivos)): #Barremos tantas veces como archivos hay
    data=pd.read_excel("S7t\\"+archivos[i],skiprows=23,names=['n1','cantidad','tiempo','distancia','carga','n2','n3']) #Usamos pandas para importar los datos de cada archivo
    name=str(archivos[i]) #Definimos el nombre del archivo como el string correspondiente
    Name = name.replace('.xlsx', '') #Sacamos el .xlsx
    for j in range(len(archivos)): #Barremos para todos los archivos
        if Name==M7[j][0]: #Si el nombre coincide con la matriz que corresponda...
            sigma=data['carga']/(M7[j][1]*M7[j][2]) #Reescaleamos la carga en tensión
            epsilon=data['distancia']*100/Lo #Reescaleamos la distancia en alarg. porc.
            for k in range(N): #Y cargamos las cantidades reescaleadas en los vectores vacíos
                E.append(epsilon[k])
                S.append(sigma[k])
            popt, pcov = curve_fit(Lin, E, S) #Hacemos el ajuste con los primeros puntos
            plt.scatter(E, S, label=Name) #Graficamos los puntos
            plt.plot(x, [Lin(i,popt[0], popt[1]) for i in x]) #Graficamos el ajuste
            #plt.text(0,1, r'Módulo de Young promedio:')
            #plt.text(0,0.9, r'$E=(0.3\pm0.2) MPa$')
            plt.xlabel('Estiramiento porcentual')
            plt.ylabel('Tensión (MPa)')
            plt.title('Sistema 7: 90:10')
            plt.legend()
            print(popt[0]) #Printeamos el valor de pendiente
            Y.append(popt[0]) #Cargamos dicho valor en el vector vacío de módulo de Young
            E=[] #Volvemos a cero los vectores para la próxima iteración
            S=[]
                
print(np.mean(Y))
print(np.std(Y))
