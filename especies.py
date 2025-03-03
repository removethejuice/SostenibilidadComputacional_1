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

def preprocesamiento(path):
    df = pd.read_csv(path)
    df['assessmentDate'] = pd.to_datetime(df['assessmentDate'])
    df['assessmentYear'] = df['assessmentDate'].dt.year

    redlist_order_map = {
        'Data Deficient': 0,
        'Least Concern': 1,
        'Near Threatened': 2,
        'Vulnerable': 3,
        'Endangered': 4,
        'Critically Endangered': 5,
        'Extinct': 6
    }
    df['redlistCategory_ordinal'] = df['redlistCategory'].map(redlist_order_map)
    poptrend_map = {
        'Decreasing': 0,
        'Stable': 1,
        'Increasing': 2,
        'Unknown': 3  
    }

    df['populationTrend_ordinal'] = df['populationTrend'].map(poptrend_map).fillna(3).astype('Int64')

    # Verificar el resultado
    print(df.head())

    # Guardar el resultado
    output_dir = "especies_preprocesado"
    df['systems'] = df['systems'].astype(str).str.split('|')

    def limpiar_sistemas(lista_sistemas):
        sistemas_limpios = set(s.strip() for s in lista_sistemas)
        return list(sistemas_limpios)

    df['systems'] = df['systems'].apply(limpiar_sistemas)

    def normalizar_sistemas(lista_sistemas):
        sistemas_normalizados = []
        for s in lista_sistemas:
            if s == 'Freshwater (=Inland waters)':
                sistemas_normalizados.append('Freshwater')
            else:
                sistemas_normalizados.append(s)
        return list(set(sistemas_normalizados))

    df['systems'] = df['systems'].apply(normalizar_sistemas)

    df_nuevo = df[['scientificName', 'redlistCategory_ordinal', 'populationTrend_ordinal', 'assessmentYear', 'systems', 'assessmentDate']]
    print(df_nuevo.head())
    
    df_count = (
        df.groupby(["assessmentYear", "redlistCategory"])["scientificName"]
        .nunique()
    )
    df_pivot = df_count.unstack(level="redlistCategory", fill_value=0)

    print(df_pivot)

    cols_a_ignorar = ['Data Deficient', 'Least Concern']
    cols_para_graficar = [col for col in df_pivot.columns if col not in cols_a_ignorar]

    # Crear el gráfico de líneas
    plt.figure(figsize=(10, 6))
    for categoria in cols_para_graficar:
        plt.plot(df_pivot.index, df_pivot[categoria], marker='o', label=categoria)

    plt.xlabel('Año de Evaluación')
    plt.ylabel('Número de Especies')
    plt.title('Tendencia de Categorías de Peligro por Año')
    plt.legend(title='Categoría')
    plt.grid(True)
    plt.show()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    df_nuevo.to_csv(os.path.join(output_dir, 'assessments.csv'), index=False)
    df_pivot.to_csv(os.path.join(output_dir, 'especies_por_anio.csv'))


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(script_dir, 'redlist_species_data_77e445ad-bbc0-4eec-bbd2-78e44b850ffb', argv[1])
    preprocesamiento(relative_path)