import streamlit as st # type: ignore

import sys
sys.path.append("../")
from src import support_open_ai as sp 

# Título de la aplicación
st.markdown("### Asistente de Ventas")

# Inicializar session_state si no existe
if "historial_ventas" not in st.session_state:
    st.session_state.historial_ventas = []
if "input_key" not in st.session_state:
    st.session_state.input_key = 0  # Clave dinámica para resetear input
if 'button_ventas' not in st.session_state:
    st.session_state.button_ventas = False

def click_button_send():
    st.session_state.button_ventas = not st.session_state.button_ventas

st.text_area("Historico de la conversacion:", value="\n".join(st.session_state.historial_ventas), height=350, disabled=True)

# Entrada de texto con clave dinámica
user_input = st.text_input("Pregunta sobre el curso disponible de Full Stack:", key=f"user_input_{st.session_state.input_key}")

id_asis = st.secrets['security']['OPENAI_API_ASSIS_VENTA']

openai_client = sp.init_openai()
assis_venta = sp.get_assistant(openai_client, id_asis)

if st.button("Enviar" , on_click=click_button_send, disabled=st.session_state.button_ventas):
        if user_input.strip():  # Evita entradas vacías
            thread = sp.create_thread(openai_client)
            respuesta = sp.process_data(openai_client, assis_venta.id, thread.id, user_input)
            st.session_state.historial_ventas.append(f"Tú: {user_input}" + '\n' + 'Asistente: '+ respuesta)
            st.session_state.input_key += 1  # Cambiar clave para limpiar input
            st.session_state.button_ventas = False
            st.rerun()  # Refrescar la app para borrar input
        else:
            st.session_state.button_ventas = False
            st.rerun()  # Refrescar la app para borrar input
if st.button("Borrar"):
        st.session_state.historial_ventas = []
        st.rerun()  # Refrescar la app para borrar input




