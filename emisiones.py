import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from sys import argv
import re
from scipy.stats import pearsonr

def visualizacion(path1, path2):
    df = pd.read_csv(path1)
    years = list(range(1961, 2024))

    # Extraer los valores de temperatura para cada año (convertir a float por si acaso)
    temperature_change = df.loc[0, '1961':'2023'].astype(float).values

    # Crear la gráfica de línea
    plt.figure(figsize=(10,6))
    plt.plot(years, temperature_change, marker='o', linestyle='-', label='Cambio de temperatura')
    plt.xlabel("Año")
    plt.ylabel("Cambio de temperatura (°C)")
    plt.title("Aumento de temperatura en Honduras (1961-2023)")
    plt.grid(True)
    plt.legend()
    plt.show()

    df_2 = pd.read_excel(path2)  
    print(df_2.head())

    pattern = r'gfw_forest_carbon_gross_emissions_(\d{4})__Mg_CO2e'
    year_columns = [col for col in df_2.columns if re.search(pattern, col)]

    row_index = 0
    years = []
    emissions = []

    for col in year_columns:
        match = re.search(pattern, col)
        if match:
            year = int(match.group(1))  
            years.append(year)
            value = df_2.loc[row_index, col]
            emissions.append(value)

    years_emissions = sorted(zip(years, emissions), key=lambda x: x[0])
    years_sorted, emissions_sorted = zip(*years_emissions)

    plt.figure(figsize=(10, 6))
    plt.plot(years_sorted, emissions_sorted, marker='o', linestyle='-')
    plt.title('Emisiones de carbono por año')
    plt.xlabel('Año')
    plt.ylabel('Emisiones (Mg CO2e)')
    plt.grid(True)
    plt.show()

    df_temp = pd.read_csv(path1)

    temperature_change = df_temp.loc[0, '1961':'2023'].astype(float).values

    temp_years = list(range(1961, 2024))
    temp_df = pd.DataFrame({'Year': temp_years, 'Temperature': temperature_change})

    df_co2 = pd.read_excel(path2)

    pattern = r'gfw_forest_carbon_gross_emissions_(\d{4})__Mg_CO2e'
    year_columns = [col for col in df_co2.columns if re.search(pattern, col)]

    row_index = 0
    emission_years = []
    emissions = []

    for col in year_columns:
        match = re.search(pattern, col)
        if match:
            year = int(match.group(1))
            emission_years.append(year)
            value = df_co2.loc[row_index, col]
            emissions.append(value)

    emission_years, emissions = zip(*sorted(zip(emission_years, emissions), key=lambda x: x[0]))

    emissions_df = pd.DataFrame({'Year': emission_years, 'Emissions': emissions})

    common_years = set(temp_df['Year']).intersection(set(emissions_df['Year']))

    temp_df_common = temp_df[temp_df['Year'].isin(common_years)]
    emissions_df_common = emissions_df[emissions_df['Year'].isin(common_years)]

    merged_df = pd.merge(temp_df_common, emissions_df_common, on='Year')

    merged_df.sort_values(by='Year', inplace=True)

    corr_value = merged_df['Temperature'].corr(merged_df['Emissions'])
    print("Coeficiente de correlación (Pearson) (pandas):", corr_value)

    corr_coef, p_value = pearsonr(merged_df['Temperature'], merged_df['Emissions'])
    print("Coeficiente de correlación (pearsonr):", corr_coef, "p-value:", p_value)

    plt.figure(figsize=(8, 6))
    plt.scatter(merged_df['Emissions'], merged_df['Temperature'], c='blue')
    plt.xlabel("Emisiones de CO2 (Mg CO2e)")
    plt.ylabel("Cambio de temperatura (°C)")
    plt.title("Relación entre Emisiones de CO2 y Cambio de Temperatura")
    plt.grid(True)
    plt.show()



    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path1 = os.path.join(script_dir, 'Honduras_HN_All_Indicators', "23_Annual_Surface_Temperature_Change.csv")
    relative_path2 = os.path.join(script_dir, 'Dataset_gfw_preprocesado', "Country carbon data.xlsx")
    visualizacion(relative_path1, relative_path2)
   