import pandas as pd
import numpy as np
import joblib
import sys
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Cargar datos desde el archivo Excel
file_path = r"Dataset_gfw_preprocesado\Country primary loss.xlsx"  # Cambia esto por la ruta real de tu archivo
df = pd.read_excel(file_path)

# Filtrar solo las columnas de pérdida de cobertura forestal (años 2002-2023)
year_columns = [col for col in df.columns if col.startswith("primary_loss_ha_")]
df_filtered = df[year_columns].sum()  # Sumar la pérdida total por año

# Crear variables independientes (X) y dependientes (y)
years = np.array([int(col.split('_')[-1]) for col in year_columns]).reshape(-1, 1)
tree_loss = df_filtered.values.reshape(-1, 1)

# Función para calcular BIC y seleccionar el mejor grado polinomial
def select_best_polynomial(X, y, max_degree=5):
    best_bic = float('inf')
    best_degree = 1
    best_model = None

    for degree in range(1, max_degree + 1):
        poly = PolynomialFeatures(degree)
        X_poly = poly.fit_transform(X)
        
        model = sm.OLS(y, sm.add_constant(X_poly)).fit()
        bic = model.bic  # Obtener el BIC

        if bic < best_bic:
            best_bic = bic
            best_degree = degree
            best_model = model

    return best_degree, best_model

# Seleccionar el mejor modelo polinomial
best_degree, best_model = select_best_polynomial(years, tree_loss)

# Guardar el modelo en un archivo
joblib.dump((best_model, best_degree), "tree_loss_model.pkl")
print(f"Modelo guardado como 'tree_loss_model.pkl' con grado polinomial {best_degree}")

# Permitir predicciones desde la línea de comandos
if len(sys.argv) > 1:
    try:
        input_year = int(sys.argv[1])
        poly = PolynomialFeatures(best_degree)
        X_input = poly.fit_transform(np.array([[input_year]]))
        prediction = best_model.predict(sm.add_constant(X_input))[0]

        print(f"Pérdida de cobertura forestal estimada para {input_year}: {prediction:.2f} hectáreas")
    except ValueError:
        print("Error: Introduce un año válido como número.")
