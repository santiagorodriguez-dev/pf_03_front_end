import streamlit as st # type: ignore

import sys
sys.path.append("../")
from src import support_open_ai as sp 

# Título de la aplicación
st.markdown("### Asistente de Resumen")

# Inicializar session_state si no existe
if "historial_conversacion" not in st.session_state:
    st.session_state.historial_conversacion = []
if "input_key_resumen" not in st.session_state:
    st.session_state.input_key_resumen = 0  # Clave dinámica para resetear input
if "thread_conversacion" not in st.session_state:
    st.session_state.thread_conversacion = ''  # Clave dinámica para resetear input
if 'button_resumen' not in st.session_state:
    st.session_state.button_resumen = False

def click_button_send():
    st.session_state.button_resumen = not st.session_state.button_resumen

st.text_area("Historico de la conversacion:", value="\n".join(st.session_state.historial_conversacion), height=350, disabled=True)

# Entrada de texto con clave dinámica
user_input = st.text_input("Introduce la conversacion para proceder al analisis:", key=f"user_input_{st.session_state.input_key_resumen}")

id_asis = st.secrets['security']['OPENAI_API_ASSIS_CONVERSACION']

openai_client = sp.init_openai()
assis_venta = sp.get_assistant(openai_client, id_asis)
st.session_state.thread_conversacion = sp.create_thread(openai_client)

col1, col2, col3 , col4, col5, col6, col7, col8 , col9, col10 = st.columns(10)

with col1:
    if st.button("Enviar" , on_click=click_button_send, disabled=st.session_state.button_resumen):
        if user_input.strip():  # Evita entradas vacías
            respuesta = sp.process_data(openai_client, assis_venta.id, st.session_state.thread_conversacion.id, user_input)
            st.session_state.historial_conversacion.append(f"Tú: {user_input}" + '\n' + 'Asistente: '+ respuesta)
            st.session_state.input_key_resumen += 1  # Cambiar clave para limpiar input
            st.session_state.button_resumen = False
            st.rerun()  # Refrescar la app para borrar input
        else:
            st.session_state.button_resumen = False
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
        st.session_state.historial_conversacion = []
        st.rerun()  # Refrescar la app para borrar input


