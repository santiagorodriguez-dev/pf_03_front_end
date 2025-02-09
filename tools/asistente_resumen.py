import streamlit as st # type: ignore

import sys
sys.path.append("../")
from src import support_open_ai as sp


# Módulo para un asistente de feedback basado en un modelo de resumen de conversaciones telefónicas,
# implementado en Streamlit.

# Funcionalidad:
# - Muestra un historial de conversación con respuestas generadas por un asistente de IA.
# - Permite al usuario ingresar una conversación para su análisis y obtener un resumen.
# - Utiliza OpenAI para procesar la conversación y generar respuestas.
# - Permite borrar el historial de conversación.

# Dependencias:
# - Streamlit (`st`)
# - Módulo `support_open_ai` (`sp`) para la integración con OpenAI.

# Variables de estado (`st.session_state`):
# - `historial_conversacion`: Lista que almacena las interacciones entre el usuario y el asistente.
# - `input_key_resumen`: Clave dinámica para actualizar el campo de entrada y limpiarlo tras el envío.
# - `button_resumen`: Controla el estado del botón "Enviar" para evitar múltiples envíos simultáneos.

# Funciones:
# - `click_button_send()`: Alterna el estado de `button_resumen` para controlar el botón de envío.

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

# Título de la aplicación
st.markdown("### Asistente Feedback (Modelo Resumen conversacion telefónica)")
separador = '****************************************************************************************************'

# Inicializar session_state si no existe
if "historial_conversacion" not in st.session_state:
    st.session_state.historial_conversacion = []
if "input_key_resumen" not in st.session_state:
    st.session_state.input_key_resumen = 0  # Clave dinámica para resetear input
if 'button_resumen' not in st.session_state:
    st.session_state.button_resumen = False

def click_button_send():
    st.session_state.button_resumen = not st.session_state.button_resumen

st.text_area("Historial", value="\n".join(st.session_state.historial_conversacion), height=350, disabled=True)

# Entrada de texto con clave dinámica
user_input = st.text_input("Introduce la conversacion para proceder al analisis:", key=f"user_input_{st.session_state.input_key_resumen}")

id_asis = st.secrets['security']['OPENAI_API_ASSIS_CONVERSACION']

openai_client = sp.init_openai()
assis_venta = sp.get_assistant(openai_client, id_asis)

if st.button("Enviar" , on_click=click_button_send, disabled=st.session_state.button_resumen):
        if user_input.strip():  # Evita entradas vacías
            try:
                thread = sp.create_thread(openai_client)
                st.write(f"Hilo Creado...{thread.id}")
                respuesta = sp.process_data(openai_client, assis_venta.id, thread.id, user_input)
            except:
                 respuesta = 'No se ha podido procesar la respuesta, intentalo de nuevo.'

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



