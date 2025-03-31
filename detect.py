import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Cargar el archivo CSV
file_path = "CSReport.csv"
df = pd.read_csv(file_path)

# Verificar si las columnas necesarias existen
if "Text" not in df.columns or "TC name" not in df.columns:
    raise ValueError("Las columnas 'Text' o 'TC name' no se encuentran en el archivo CSV.")

# Agregar columna 'Stations' en la primera posición
df.insert(0, "Stations", None)

# Rellenar 'Stations' con valores de 'Text' solo cuando 'TC name' sea NaN
df.loc[df["TC name"].isna(), "Stations"] = df["Text"]

# Propagar los valores de "Stations" hacia abajo (Forward Fill)
df["Stations"].fillna(method="ffill", inplace=True)
print(df)

# Crear un nuevo archivo de Excel
output_file = "stations_processed.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "Processed Data"

# Escribir los datos al archivo Excel
for r in dataframe_to_rows(df, index=False, header=True):
    ws.append(r)

# Guardar el archivo Excel
wb.save(output_file)
print(f"✅ Archivo '{output_file}' creado exitosamente.")