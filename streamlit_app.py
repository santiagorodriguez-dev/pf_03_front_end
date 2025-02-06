import streamlit as st # type: ignore
import streamlit_authenticator as stauth # type: ignore

import yaml
from yaml.loader import SafeLoader

import sys
sys.path.append("../")

from src import support_bd as bd
from src import web as w

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

"""
Módulo de autenticación y carga de la aplicación en Streamlit.

Funcionalidad:
- Configura la página de Streamlit con título, icono y diseño adaptable.
- Carga las credenciales de usuario desde un archivo de configuración (`config.yaml`).
- Implementa autenticación de usuarios con `streamlit_authenticator`.
- Valida credenciales y gestiona sesiones de usuario con cookies.
- Carga la aplicación principal si el usuario ha iniciado sesión correctamente.

Dependencias:
- `streamlit` (`st`) para la interfaz de usuario.
- `streamlit_authenticator` (`stauth`) para la autenticación basada en cookies.
- `yaml` para la carga de configuraciones desde `config.yaml`.
- `support_bd` (`bd`) y `web` (`w`) como módulos de soporte.

Configuración:
- `config.yaml`: Contiene credenciales y configuración de cookies.
- `st.secrets`: Maneja credenciales de forma segura en Streamlit Cloud.

Funciones:
- `login()`: 
  - Muestra el formulario de autenticación.
  - Valida credenciales y gestiona el estado de autenticación.
  - Carga la aplicación principal (`w.load_web()`) si el usuario ha iniciado sesión correctamente.

Flujo:
1. Configura la página de Streamlit con `st.set_page_config()`.
2. Carga las credenciales y configuraciones de autenticación desde `config.yaml` y `st.secrets`.
3. Inicializa `streamlit_authenticator.Authenticate` para manejar sesiones de usuario.
4. Llama a `login()` para:
   - Autenticar al usuario.
   - Mostrar mensajes de error o advertencia en caso de credenciales incorrectas o vacías.
   - Cargar la aplicación principal en caso de autenticación exitosa.

Notas:
- La autenticación se gestiona mediante cookies, lo que permite sesiones persistentes.
- Se recomienda almacenar credenciales de manera segura en `st.secrets`.
"""

st.set_page_config(
        page_title="Asistente",
        page_icon=":sunny:",
        layout="wide",
        initial_sidebar_state="auto",
)

config['credentials'] = st.secrets["credentials"].to_dict()
config['cookie']['name'] = st.secrets['cookie']['name'] 
config['cookie']['key'], = st.secrets['cookie']['key'], 
config['cookie']['expiry_days'] = st.secrets['cookie']['expiry_days']

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Función de login
def login():

    # Mostrar el formulario de autenticación
    authenticator.login()
    if st.session_state['authentication_status']:
        w.load_web(st, authenticator)
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Introduce usuario y contraseña')

if __name__ == "__main__":
    login()
