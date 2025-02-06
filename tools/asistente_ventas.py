import streamlit as st # type: ignore

import sys
sys.path.append("../")
from src import support_open_ai as sp 

# """
# Módulo para un asistente de ventas basado en un modelo de IA, implementado en Streamlit.

# Funcionalidad:
# - Muestra un historial de interacción con el asistente de ventas.
# - Permite al usuario realizar consultas sobre ventas y recibir respuestas generadas por OpenAI.
# - Utiliza OpenAI para procesar la consulta y generar una respuesta relevante.
# - Opción para borrar el historial de conversación.

# Dependencias:
# - Streamlit (`st`)
# - Módulo `support_open_ai` (`sp`) para la integración con OpenAI.

# Variables de estado (`st.session_state`):
# - `historial_ventas`: Lista que almacena las interacciones entre el usuario y el asistente.
# - `input_key`: Clave dinámica para actualizar el campo de entrada y limpiarlo tras el envío.
# - `button_ventas`: Controla el estado del botón "Enviar" para evitar múltiples envíos simultáneos.

# Funciones:
# - `click_button_send()`: Alterna el estado de `button_ventas` para controlar el botón de envío.

# Flujo:
# 1. Se muestra el historial de conversación en un área de texto deshabilitada.
# 2. Se recibe la entrada del usuario a través de un campo de texto.
# 3. Al hacer clic en "Enviar":
#    - Se procesa la entrada con OpenAI.
#    - Se guarda la respuesta en el historial.
#    - Se actualiza la clave del input para limpiar el campo.
#    - Se refresca la aplicación con `st.rerun()`.
# 4. Un botón "Borrar" permite limpiar el historial de la conversación.

# Notas:
# - Evita enviar entradas vacías.
# - Usa `st.secrets` para manejar credenciales de OpenAI de forma segura.
# """


# Título de la aplicación
st.markdown("### Asistente de Ventas (Modelo Curso Full Stack)")
separador = '****************************************************************************************************'

# Inicializar session_state si no existe
if "historial_ventas" not in st.session_state:
    st.session_state.historial_ventas = []
if "input_key" not in st.session_state:
    st.session_state.input_key = 0  # Clave dinámica para resetear input
if 'button_ventas' not in st.session_state:
    st.session_state.button_ventas = False

def click_button_send():
    st.session_state.button_ventas = not st.session_state.button_ventas

st.text_area("Historial", value="\n".join(st.session_state.historial_ventas), height=350, disabled=True)

# Entrada de texto con clave dinámica
user_input = st.text_input("Introduce una consulta:", key=f"user_input_{st.session_state.input_key}")

id_asis = st.secrets['security']['OPENAI_API_ASSIS_VENTA']

openai_client = sp.init_openai()
assis_venta = sp.get_assistant(openai_client, id_asis)

if st.button("Enviar" , on_click=click_button_send, disabled=st.session_state.button_ventas):
        if user_input.strip():  # Evita entradas vacías
            thread = sp.create_thread(openai_client)
            respuesta = sp.process_data(openai_client, assis_venta.id, thread.id, user_input)
            st.session_state.historial_ventas.append(f"{st.session_state["name"]}: {user_input}"  + '\n' + separador + '\n' + 'Asistente: '+ respuesta + '\n' + separador)
            st.session_state.input_key += 1  # Cambiar clave para limpiar input
            st.session_state.button_ventas = False
            st.rerun()  # Refrescar la app para borrar input
        else:
            st.session_state.button_ventas = False
            st.rerun()  # Refrescar la app para borrar input
if st.button("Borrar"):
        st.session_state.historial_ventas = []
        st.rerun()  # Refrescar la app para borrar input




