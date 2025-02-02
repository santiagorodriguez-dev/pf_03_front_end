import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


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
    st.title("Asistente de ventas")
    
    # Mostrar el formulario de autenticación
    authenticator.login()
    if st.session_state['authentication_status']:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Some content')
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Introduce usuario y contraseña')

if __name__ == "__main__":
    login()
