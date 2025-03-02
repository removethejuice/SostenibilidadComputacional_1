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
    df = pd.read_csv(path)
    df = df.dropna() #borramos las filas con datos faltantes, viendo los datos directamente, vemos que no hay datos faltantes, pero siempre inclyo el codigo
    df = df.drop_duplicates() #borramos los duplicados
    
    return 0