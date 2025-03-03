import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from sys import argv
import re
from scipy.stats import pearsonr

def preprocesamiento(path, forest_path):
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


    df['systems'] = df['systems'].apply(lambda x: x if isinstance(x, list) else [x])

    df_exploded = df.explode('systems').rename(columns={'systems': 'system'})

    df_exploded = df_exploded[~df_exploded['redlistCategory_ordinal'].isin([0, 1])]

    grouped = df_exploded.groupby(['system', 'redlistCategory_ordinal'])['scientificName']\
                        .nunique()\
                        .reset_index(name='count')

    pivot_df = grouped.pivot(index='system', columns='redlistCategory_ordinal', values='count').fillna(0)

    inverse_redlist_order_map = {v: k for k, v in redlist_order_map.items()}
    pivot_df = pivot_df.rename(columns=inverse_redlist_order_map)

    plt.figure(figsize=(10, 6))
    pivot_df.plot(kind='bar', stacked=False, ax=plt.gca())
    plt.xlabel('Sistema')
    plt.ylabel('Número de especies')
    plt.title('Número de especies por sistema y categoría de peligro')
    plt.legend(title='Categoría de peligro (ordinal)')
    plt.show()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    df_nuevo.to_csv(os.path.join(output_dir, 'assessments.csv'), index=False)
    df_pivot.to_csv(os.path.join(output_dir, 'especies_por_anio.csv'))


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

    df_amenazadas = df[df['redlistCategory_ordinal'] >= 2]

    df_count = (
        df_amenazadas.groupby("assessmentYear")["scientificName"]
        .nunique()
        .reset_index(name='threatened_species_count')
    )

    df_forest = pd.read_excel(forest_path)
    print(df_forest.head())
    row_index = 0

    pattern = r'tc_loss_ha_(\d{4})'
    year_columns = [col for col in df_forest.columns if re.match(pattern, col)]

    forest_years = []
    forest_loss = []

    for col in year_columns:
        match = re.match(pattern, col)
        if match:
            year = int(match.group(1))  
            forest_years.append(year)
            value = df_forest.loc[row_index, col]
            forest_loss.append(value)

    df_loss = pd.DataFrame({
        'assessmentYear': forest_years,
        'forest_loss_ha': forest_loss
    })

    df_merged = pd.merge(df_count, df_loss, on='assessmentYear', how='inner')
    print(df_merged.head())
    print(df_count.head())
    print(df_loss.head())

    df_merged.sort_values('assessmentYear', inplace=True)

    corr_pearson = df_merged['threatened_species_count'].corr(df_merged['forest_loss_ha'])
    print("Coeficiente de correlación (Pearson):", corr_pearson)

    corr_coef, p_value = pearsonr(df_merged['threatened_species_count'], df_merged['forest_loss_ha'])
    print(f"Coeficiente de correlación = {corr_coef}, p-value = {p_value}")

    plt.figure(figsize=(8, 6))
    plt.scatter(df_merged['forest_loss_ha'], df_merged['threatened_species_count'], c='blue')
    plt.xlabel("Pérdida de bosque (ha)")
    plt.ylabel("Número de especies amenazadas")
    plt.title("Relación entre Pérdida de Bosque y Especies Amenazadas")
    plt.grid(True)
    plt.show()



if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(script_dir, 'redlist_species_data_77e445ad-bbc0-4eec-bbd2-78e44b850ffb', 'assessments.csv')
    forest_path = os.path.join(script_dir, 'Dataset_gfw_preprocesado', "Country tree cover loss.xlsx")
    preprocesamiento(relative_path, forest_path)