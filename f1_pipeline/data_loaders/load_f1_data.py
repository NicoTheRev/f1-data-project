import io
import pandas as pd
import requests

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Consulta la API de OpenF1 para obtener las sesiones del año 2026.
    """
    # Endpoint para consultar las sesiones de la temporada 2026
    url = 'https://api.openf1.org/v1/sessions?year=2026'
    
    print(f"Iniciando la descarga de datos desde: {url}")
    response = requests.get(url)
    
    # Validamos que la API responda correctamente (Código 200)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        print(f"¡Éxito! Se descargaron {len(df)} registros de sesiones.")
        return df
    else:
        raise Exception(f"Error al consultar la API. Código de estado: {response.status_code}")


@test
def test_output(output, *args) -> None:
    """
    Test automático nativo de Mage para asegurar que el bloque funciona.
    """
    assert output is not None, 'El output es nulo, la API no trajo datos.'
    assert isinstance(output, pd.DataFrame), 'El output debe ser un DataFrame de Pandas.'
    assert not output.empty, 'El DataFrame está vacío.'