import pandas as pd
import requests
import ee
import time
from pathlib import Path

# Configuración de la cuenta de servicio
SERVICE_ACCOUNT = 'geeupdateassetaccount@test-hsluis4326.iam.gserviceaccount.com'
KEY_FILE = 'key.json'  # Ruta relativa para GitHub Actions
ASSET_ID = 'projects/test-hsluis4326/assets/csvTest'
CSV_PATH = Path(__file__).resolve().parent / 'test.csv'  # Guardar en mismo dir del script

# Autenticación
credentials = ee.ServiceAccountCredentials(SERVICE_ACCOUNT, str(KEY_FILE))
ee.Initialize(credentials)

def descargar_y_guardar_csv():
    url = "http://met.igp.gob.pe/datos/ICEN.txt"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    # Filtrar líneas válidas (ignora líneas que empiezan con '%')
    lines = response.text.strip().splitlines()
    data = [line.strip().split() for line in lines if line.strip() and not line.startswith('%')]

    # Convertir a DataFrame con encabezado claro
    df = pd.DataFrame(data, columns=["yy", "mm", "icen"])

    # Guardar como CSV en la ubicación del script
    df.to_csv(CSV_PATH, index=False)

    # Convertir a FeatureCollection con geometría dummy (0,0)
    features = []
    dummy_geom = ee.Geometry.Point([0, 0])
    for _, row in df.iterrows():
        feat = ee.Feature(dummy_geom, row.to_dict())
        features.append(feat)

    fc = ee.FeatureCollection(features)

    # Intentar borrar asset si ya existe
    try:
        print(f"Intentando borrar el asset Legacy: {ASSET_ID}")
        ee.data.deleteAsset(ASSET_ID)
        print("✅ Asset borrado exitosamente")
    except ee.EEException as e:
        print(f"⚠️  Nota: {e}")

    # Exportar a Asset (sin usar GCS)
    task = ee.batch.Export.table.toAsset(
        collection=fc,
        description='Subida_de_csvTest',
        assetId=ASSET_ID
    )
    task.start()
    print("🚀 Tarea de exportación iniciada.")
    
    # Espera a que la tarea termine (opcional, pero recomendado)
    while task.status()['state'] in ['READY', 'RUNNING']:
        time.sleep(10)
    print(f"✅ Tarea finalizada con estado: {task.status()}")

    # Establecer permisos públicos (Anyone can read)
    try:
        ee.data.setAssetAcl(ASSET_ID, {'all_users_can_read': True})
        print("🔓 Permisos actualizados: 'Anyone can read' activado.")
    except Exception as e:
        print(f"❌ Error al actualizar permisos: {e}")

descargar_y_guardar_csv()
