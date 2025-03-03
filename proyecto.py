import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as skl
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os
import sys
from sys import argv

# Notamos que hay que hacer un preprocesamiento solido, dado que nuestro dataset contiene muchos datos redundantes
def preprocesamiento_gfw(path):
    df = pd.ExcelFile(path)  # leemos el archivo excel
    output_dir = "Dataset_gfw_preprocesado"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for sheet in df.sheet_names:
        print(sheet)
        df = pd.read_excel(path, sheet_name=sheet)  # leemos el archivo excel, nos trasladamremos por cada sheet del archivo y borramos el mismo tipo de datos
        if 'country' in df.columns:
            #please create a function that deletes the first column if it contains no useful information and no name
            if df.columns[0] == 'Unnamed: 0':
                df = df.drop(df.columns[0], axis=1)
            df = df.dropna()  # borramos las filas con datos faltantes, viendo los datos directamente, vemos que no hay datos faltantes, pero siempre inclyo el codigo
            df = df.drop_duplicates()  # borramos los duplicados
            df = df[df['country'] == 'Honduras']  # filtramos los datos para que solo sean de Honduras, este dataset es mundial
            df = df.drop('country', axis=1)  # borramos la columna country porque despues de borrar los datos sabemos que solo es  Honduras
            df.to_excel(os.path.join(output_dir, sheet + ".xlsx"))  # guardamos el dataset limpio
    return df

def AED_country(df):
    years = [f"tc_loss_ha_{year}" for year in range(2001, 2024)]# usamos el for para crear el range de años en los cuales haremos el AED
    existing_years = [year for year in years if year in df.columns]
    df_filtrado = df[existing_years]



    print(df.head())  # aca vamos a ver los 10 primero datos de nuestro dataset
    print(df.describe())  # aca vamos a ver un resumen de los datos de nuestro dataset
    df.info()  # aca vamos a ver la informacion de nuestro dataset

    # Set seaborn style
    sns.set_theme(style="whitegrid")


    # Este boxplot nos ayuda a encontrar valores atipicos
    plt.figure(figsize=(14, 6))
    sns.boxplot(data=df_filtrado)
    plt.xticks(rotation=90)
    plt.title("Boxplot de Tree Cover Loss (2001 - 2023)")
    plt.xlabel("Año")
    plt.ylabel("Tree Cover Loss (hectareas)")
    plt.show()



    # Plot line
    plt.figure(figsize=(12, 6))
    df_filtrado.mean().plot(marker='o', linestyle='-', color='b')
    plt.xticks(rotation=90)
    plt.title("Promedio de Tree Cover Loss Over Time (2001 - 2023)")
    plt.xlabel("Año")
    plt.ylabel("Average Tree Cover Loss (hectarea)")
    plt.grid(True)
    plt.show()

def AED_region(df):
    
    return 0

def main():
    path = "gfw_2023_statistics_summary_v30102024.xlsx"
    preprocesamiento_gfw(path)
    df= pd.read_excel(r"Dataset_gfw_preprocesado\Country tree cover loss.xlsx")# aca miramos  el total de bosque perdido por año
    AED_country(df)


if __name__ == "__main__":
    main()