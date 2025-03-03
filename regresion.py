import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Cargar el conjunto de datos
df = pd.read_excel(r"Dataset_gfw_preprocesado/Country primary loss.xlsx")

# Seleccionar solo las columnas relevantes (años)
year_columns = [col for col in df.columns if col.startswith("primary_loss_ha_")]
years = np.array([int(col.split("_")[-1]) for col in year_columns]).reshape(-1, 1)
tree_loss = df[year_columns].sum().values  # Sumar todos los datos de pérdida de árboles

# Entrenar el modelo
model = LinearRegression()
model.fit(years, tree_loss)

# Guardar el modelo
joblib.dump(model, "tree_loss_model.pkl")
print("Modelo guardado como 'tree_loss_model.pkl'")

# Prediccion desde la linea de comandos
if len(sys.argv) == 2:
    try:
        year = int(sys.argv[1])  # Convertir la entrada de la línea de comandos a entero
        model = joblib.load("tree_loss_model.pkl")  # Cargar el modelo
        prediction = model.predict(np.array([[year]]))  # Predecir la pérdida de árboles
        print(f"Pérdida de árboles predicha para {year}: {prediction[0]}")
    except ValueError:
        print("Error: Por favor, ingrese un año válido como número.")
        sys.exit(1)
