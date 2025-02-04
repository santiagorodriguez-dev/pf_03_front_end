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
if "thread_ventas" not in st.session_state:
    st.session_state.thread_ventas = ''  # Clave dinámica para resetear input
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
st.session_state.thread_ventas = sp.create_thread(openai_client)

col1, col2, col3 , col4, col5, col6, col7, col8 , col9, col10 = st.columns(10)

with col1:
    if st.button("Enviar" , on_click=click_button_send, disabled=st.session_state.button_ventas):
        if user_input.strip():  # Evita entradas vacías
            respuesta = sp.process_data(openai_client, assis_venta.id, st.session_state.thread_ventas.id, user_input)
            st.session_state.historial_ventas.append(f"Tú: {user_input}" + '\n' + 'Asistente: '+ respuesta)
            st.session_state.input_key += 1  # Cambiar clave para limpiar input
            st.session_state.button_ventas = False
            st.rerun()  # Refrescar la app para borrar input
        else:
            st.session_state.button_ventas = False
            st.rerun()  # Refrescar la app para borrar input
with col2:
    pass
with col4:
    pass
with col5:
    pass
with col6 :
    pass
with col7:
    pass
with col8:
    pass
with col9 :
    pass
with col10 :
    if st.button("Borrar"):
        st.session_state.historial_ventas = []
        st.rerun()  # Refrescar la app para borrar input


