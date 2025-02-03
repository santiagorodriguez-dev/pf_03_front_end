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


st.set_page_config(
        page_title="Asistente de ventas",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="collapsed",
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
