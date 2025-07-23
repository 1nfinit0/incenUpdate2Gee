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

# Crear nuevo contenido completo del README
nuevo_contenido = f"""<!--TABLA_ICEN-->

{tabla_md}

<!--ACTUALIZACION_ICEN--> {fecha}
"""

# Guardar README completamente nuevo
with open("README.md", "w") as f:
    f.write(nuevo_contenido)