import streamlit as st # type: ignore

# Título de la aplicación
st.markdown("### Asistente de Ventas")

# Inicializar session_state si no existe
if "historial_ventas" not in st.session_state:
    st.session_state.historial_ventas = []
if "input_key" not in st.session_state:
    st.session_state.input_key = 0  # Clave dinámica para resetear input


st.text_area("Respuesta del asistente:", value="\n".join(st.session_state.historial_ventas), height=350, disabled=True)

# Entrada de texto con clave dinámica
user_input = st.text_input("Pregunta sobre el curso de Full Stack:", key=f"user_input_{st.session_state.input_key}")

col1, col2, col3 , col4, col5, col6, col7, col8 , col9, col10 = st.columns(10)

with col1:
    if st.button("Enviar"):
        if user_input.strip():  # Evita entradas vacías
            st.session_state.historial_ventas.append(f"Tú: {user_input}")
            st.session_state.input_key += 1  # Cambiar clave para limpiar input
            st.rerun()  # Refrescar la app para borrar input
with col2:
    if st.button("Borrar"):
        st.session_state.historial_ventas = []
        st.rerun()  # Refrescar la app para borrar input
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
    pass


