import streamlit as st # type: ignore

import sys
sys.path.append("../")
from src import support_open_ai as sp 

# Título de la aplicación
st.markdown("### Asistente Feedback (Modelo Resumen conversacion telefónica)")
separador = '********************************************************************************************************'

# Inicializar session_state si no existe
if "historial_conversacion" not in st.session_state:
    st.session_state.historial_conversacion = []
if "input_key_resumen" not in st.session_state:
    st.session_state.input_key_resumen = 0  # Clave dinámica para resetear input
if 'button_resumen' not in st.session_state:
    st.session_state.button_resumen = False

def click_button_send():
    st.session_state.button_resumen = not st.session_state.button_resumen

st.text_area("", value="\n".join(st.session_state.historial_conversacion), height=350, disabled=True)

# Entrada de texto con clave dinámica
user_input = st.text_input("Introduce la conversacion para proceder al analisis:", key=f"user_input_{st.session_state.input_key_resumen}")

id_asis = st.secrets['security']['OPENAI_API_ASSIS_CONVERSACION']

openai_client = sp.init_openai()
assis_venta = sp.get_assistant(openai_client, id_asis)

if st.button("Enviar" , on_click=click_button_send, disabled=st.session_state.button_resumen):
        if user_input.strip():  # Evita entradas vacías
            thread = sp.create_thread(openai_client)
            respuesta = sp.process_data(openai_client, assis_venta.id, thread.id, user_input)
            st.session_state.historial_conversacion.append(f"{st.session_state["name"]}: {user_input}"  + '\n' + separador + '\n' + 'Asistente: '+ respuesta + '\n' + separador)
            st.session_state.input_key_resumen += 1  # Cambiar clave para limpiar input
            st.session_state.button_resumen = False
            st.rerun()  # Refrescar la app para borrar input
        else:
            st.session_state.button_resumen = False
            st.rerun()  # Refrescar la app para borrar input

if st.button("Borrar"):
        st.session_state.historial_conversacion = []
        st.rerun()  # Refrescar la app para borrar input



