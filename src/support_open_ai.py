# Importaciones
import pandas as pd # type: ignore
import time
import sys
sys.path.append("../")

import os
import streamlit as st # type: ignore
from openai import OpenAI # type: ignore

def init_openai():
    """
    Inicializa el cliente de OpenAI utilizando la clave API almacenada en las variables de entorno.

    Returns:
        OpenAI: Instancia del cliente de OpenAI.
    """
    OPENAI_API_KEY = st.secrets['security']['OPENAI_API_KEY']
    return OpenAI(api_key=OPENAI_API_KEY)

def get_assistant(openai_client, assistant_id):
    """
    Recupera un asistente específico de OpenAI a partir de su ID.

    Args:
        openai_client (OpenAI): Cliente de OpenAI.
        assistant_id (str): ID del asistente a recuperar.

    Returns:
        dict: Datos del asistente recuperado.
    """
    return openai_client.beta.assistants.retrieve(
        assistant_id=assistant_id
    )

def create_thread(openai_client):
    """
    Crea un nuevo hilo de conversación en OpenAI.

    Args:
        openai_client (OpenAI): Cliente de OpenAI.

    Returns:
        dict: Información del hilo creado.
    """
    return openai_client.beta.threads.create()

def process_data(openai_client, assistant_id, thread_id, message):
    """
    Envía un mensaje a un asistente de OpenAI y procesa su respuesta.

    Args:
        openai_client (OpenAI): Cliente de OpenAI.
        assistant_id (str): ID del asistente de OpenAI.
        thread_id (str): ID del hilo en el que se enviará el mensaje.
        message (str): Mensaje a enviar al asistente.

    Returns:
        str: Respuesta del asistente si está disponible, de lo contrario, None.
    """
    openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
    )

    run = openai_client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    run_status = openai_client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run.id
    )

    st.write(f"Asistente id: {assistant_id}")

    while True:
        run_status = openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == "completed":
            print("se completó exitosamente.")
            break
        elif run_status.status == "failed":
            print("petó.")
            break
        else:
            st.write(f"Esperando a que se complete...{run.id}")
            time.sleep(3)

    print(f"Thread ID: {thread_id}")
    print(f"Run ID: {run.id}")
    print(f"Run Status: {run_status.status}")

    response_messages = openai_client.beta.threads.messages.list(thread_id=thread_id)

    assistant_response = None
    for message in response_messages.data:
            assistant_response = "\n".join([block.text.value for block in message.content])
            break

    if assistant_response:
        st.write(f"respuesta procesada del asistente.")
    else:
        st.write("No se encontró una respuesta del asistente.")

    return assistant_response

def process_data_sin_mensajes(openai_client, assistant_id, thread_id, message):
    """
    Envía un mensaje a un asistente de OpenAI y obtiene la respuesta sin imprimir mensajes intermedios.

    Args:
        openai_client (OpenAI): Cliente de OpenAI.
        assistant_id (str): ID del asistente de OpenAI.
        thread_id (str): ID del hilo en el que se enviará el mensaje.
        message (str): Mensaje a enviar al asistente.

    Returns:
        str: Respuesta del asistente si está disponible, o un mensaje de error si la solicitud falla.
    """

    assistant_response = "No se encontró una respuesta del asistente."

    openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
    )

    run = openai_client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    run_status = openai_client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run.id
    )

    while True:
        run_status = openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            print("Error, no se encontró una respuesta del asistente. Fallo en llamada a OpenAI.")
            return assistant_response
        else:
            time.sleep(3)

    response_messages = openai_client.beta.threads.messages.list(thread_id=thread_id)

    
    for message in response_messages.data:
            assistant_response = "\n".join([block.text.value for block in message.content])
            break

   
    return assistant_response



