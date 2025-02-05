import pandas as pd  # type: ignore
from supabase import create_client, Client # type: ignore
from supabase.client import ClientOptions # type: ignore


def init_conection_bd(st):
    """
    Inicializa la conexión con la base de datos Supabase.

    Obtiene la URL y la clave de Supabase desde las variables de entorno
    y crea un cliente con opciones específicas.

    Returns:
        Client: Objeto de cliente Supabase configurado.

    Raises:
        ValueError: Si las credenciales no están definidas en las variables de entorno.
    """
    url: str = st.secrets['security']['SUPABASE_URL']
    key: str = st.secrets['security']['SUPABASE_KEY']
    return create_client(url, key,
      options=ClientOptions(
        postgrest_client_timeout=10,
        storage_client_timeout=10,
        schema="public",
      ))

def select_datos(name_bd, st):
    """
    Realiza una consulta a la base de datos Supabase y obtiene todos los datos de una tabla.

    Args:
        name_bd (str): Nombre de la tabla de la base de datos a consultar.

    Returns:
        pd.DataFrame: Un DataFrame de Pandas con los datos obtenidos de la tabla.

    Raises:
        RuntimeError: Si hay un error en la consulta a la base de datos.
    """
    supabase = init_conection_bd(st)
    response_select = supabase.table(name_bd).select("*").order("score", desc=True).execute()
    datos_select = pd.DataFrame(response_select.data).reset_index(drop=True)
    datos_select = datos_select.drop('index', axis=1)
    datos_select['score'] = datos_select['score'].astype(float)
    return datos_select.sort_values("score", ascending=False)
 

