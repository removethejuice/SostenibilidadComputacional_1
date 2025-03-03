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
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error




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
            # Check if the first column is unnamed and contains no useful information
            if df.columns[0] == 'Unnamed: 0' and df[df.columns[0]].isnull().all():
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
    years = [f"primary_loss_ha_{year}" for year in range(2002, 2024) if f"primary_loss_ha_{year}" in df.columns]
    print("Dataset Info:")
    df.info()
    print("\ndescripcion:")
    print(df.describe())
    
    # Distribucion de la perdida de bosque primario por año
    plt.figure(figsize=(12, 6))
    df[years].sum().plot(kind='bar', color='royalblue')
    plt.title("Total Primary Forest Loss per Year")
    plt.xlabel("año")
    plt.ylabel("Primary Loss (hectareas)")
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()
    
    # Heatmap de correlacion
    plt.figure(figsize=(12, 8))
    sns.heatmap(df[years].corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Mapa de correlacion, años vs perdida")
    plt.show()
    return 0

def plot_top_5_loss(df, top=5):
    # Compute total primary loss
    years = [f"primary_loss_ha_{year}" for year in range(2002, 2024) if f"primary_loss_ha_{year}" in df.columns]
    df['total_primary_loss'] = df[years].sum(axis=1)
    top_5 = df.nlargest(top, 'total_primary_loss')
    
    plt.figure(figsize=(10, 6))
    for _, row in top_5.iterrows():
        plt.plot(years, row[years], marker='o', label=row['subnational1'])
    
    plt.title("Top 5 Regions with Highest Primary Forest Loss")
    plt.xlabel("Year")
    plt.ylabel("Primary Loss (ha)")
    plt.xticks(rotation=90)
    plt.legend()
    plt.grid(True)
    plt.show()


    #bar chart comienza aca
    primary_loss_columns = [col for col in df.columns if "primary_loss_ha_" in col]

    # Calcula el top
    df["total_primary_loss"] = df[primary_loss_columns].sum(axis=1)

    # Sumamos el total arriba y aca seleccionamos el top, que determine que sean los 5 primeros
    top5 = df.nlargest(top, "total_primary_loss")

    # Este es el bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(top5["subnational1"], top5["total_primary_loss"], color="royalblue")

    # Labels and title
    plt.xlabel("Regiones", fontsize=12)
    plt.ylabel("Total Primary Forest Loss (hectareas)", fontsize=12)
    plt.title("Top "+str(top) +" Regiones con el top de perdidas (2002-2023)", fontsize=14)
    plt.xticks(rotation=45)

    # Show the plot
    plt.show()



def main():
    path = "gfw_2023_statistics_summary_v30102024.xlsx"
    preprocesamiento_gfw(path)
    df= pd.read_excel(r"Dataset_gfw_preprocesado\Country tree cover loss.xlsx")# aca miramos  el total de bosque perdido por año
    AED_country(df)
    df = pd.read_excel(r"Dataset_gfw_preprocesado\Subnational 1 primary loss.xlsx")# aca miramos  el total de bosque primario perdido por año
    AED_region(df)
    plot_top_5_loss(df, top =5)

if __name__ == "__main__":
    main()