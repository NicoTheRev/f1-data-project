import io
import os
from google.cloud import storage
from pandas import DataFrame

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    """
    Exporta el DataFrame a GCS usando el cliente nativo de Google Cloud.
    Bypassea el io_config.yaml para evitar errores de formato OpenSSL.
    """
    # ⚠️ REEMPLAZA CON EL NOMBRE EXACTO DE TU BUCKET DE GCP
    bucket_name = 'f1-data-lake-raw' 
    object_key = 'raw/sessions/year=2026/f1_sessions.parquet'

    print("Conectando con Google Cloud Storage de forma nativa...")
    
    # El cliente de Google busca GOOGLE_APPLICATION_CREDENTIALS automáticamente
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_key)

    print("Convirtiendo DataFrame a formato Parquet en memoria (RAM)...")
    # Procesamos en memoria usando un buffer de bytes para máxima eficiencia
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, index=False, engine='pyarrow')
    parquet_buffer.seek(0) # Apuntar al inicio del archivo virtual

    print(f"Subiendo archivo a: gs://{bucket_name}/{object_key}")
    blob.upload_from_file(parquet_buffer, content_type='application/octet-stream')

    print("¡Éxito total! Datos optimizados y cargados en el Data Lake sin errores.")