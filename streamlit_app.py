import streamlit as st # type: ignore
import streamlit_authenticator as stauth # type: ignore

import yaml
from yaml.loader import SafeLoader

import sys
sys.path.append("../")

from src import support_bd as bd

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

        st.markdown("*Streamlit* is **really** ***cool***.")
        st.markdown('''
            :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
            :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
        st.markdown("Here's a bouquet &mdash;\
                    :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

        multi = '''If you end a line with two spaces,
        a soft return is used for the next line.

        Two (or more) newline characters in a row will result in a hard return.
        '''
        st.markdown(multi)


        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Some content')
        st.dataframe(bd.select_datos("leads",st))
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Introduce usuario y contraseña')

if __name__ == "__main__":
    login()
