import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import os
import sklearn as skl
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# Notamos que hay que hacer un preprocesamiento solido, dado que nuestro dataset contiene muchos datos redundantes
def preprocesamiento (path):
  
    df = pd.read_excel(path)# leemos el archivo excel, nos trasladamremos por cada sheet del archivo y borramos el mismo tipo de datos
    df = df.dropna() #borramos las filas con datos faltantes, viendo los datos directamente, vemos que no hay datos faltantes, pero siempre inclyo el codigo
    df = df.drop_duplicates() #borramos los duplicados
    df = df[df['country']== 'Honduras'] #filtramos los datos para que solo sean de Honduras, este dataset es mundial
    df = df.drop('country', axis=1)#borramos la columna country porque despues de borrar los datos sabemos que solo es  Honduras
    return df

def AED (df):
    df.head() #aca vamos a ver los 10 primero datos de nuestro dataset
    df.describe() #aca vamos a ver un resumen de los datos de nuestro dataset
    df.info() #aca vamos a ver la informacion de nuestro dataset

    return df

def main ():
    path = r"C:\Users\pablo\Desktop\Sostenibilidad\gfw_2023_statistics_summary_v30102024.xlsx"
    df = preprocesamiento(path)
    df = AED(df)

if __name__ == "__main__":
    main()