import pandas as pd # type: ignore
from datetime import datetime

# Leer CSV
df = pd.read_csv("test.csv")

# Tomar últimos 12 registros
ultimos = df.tail(12)

# Construir tabla Markdown
tabla_md = "| Año | Mes | ICEN |\n|-----|-----|------|\n"
for _, row in ultimos.iterrows():
    tabla_md += f"| {row['yy']} | {int(row['mm']):02d} | {row['icen']:.2f} |\n"


# Fecha actual
fecha = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

# Leer README y reemplazar marcador
with open("README.md", "r") as f:
    contenido = f.read()

# Reemplazar tabla
nuevo_contenido = contenido.split("<!--TABLA_ICEN-->")[0] + \
    f"<!--TABLA_ICEN-->\n\n{tabla_md}\n\n" + \
    contenido.split("<!--TABLA_ICEN-->")[1].split("<!--ACTUALIZACION_ICEN-->")[0] + \
    f"<!--ACTUALIZACION_ICEN--> {fecha}"

# Guardar README actualizado
with open("README.md", "w") as f:
    f.write(nuevo_contenido)

