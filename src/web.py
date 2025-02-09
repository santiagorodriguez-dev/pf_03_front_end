

def load_web(st, authenticator):
    """
    Configura la navegación y autenticación en la aplicación web.

    Parámetros:
    - st: Módulo de Streamlit para la visualización interactiva.
    - authenticator: Manejador de autenticación para gestionar el inicio y cierre de sesión.

    Funcionalidad:
    1. Comprueba el estado de autenticación del usuario y actualiza la variable de sesión `logged_in`.
    2. Define una función interna `logout()` para manejar el cierre de sesión.
    3. Crea y configura las páginas de navegación:
        - "Usuario" para el cierre de sesión.
        - "Analisis Leads" para visualizar reportes de leads.
        - "Asistente Venta" como asistente de ventas (página predeterminada).
        - "Asistente Resumen" para generar resúmenes.
    4. Muestra la navegación solo si el usuario está autenticado.

    La función utiliza `st.navigation` para definir la estructura del menú y ejecutar la página seleccionada.
    """
    if st.session_state.authentication_status:
        st.session_state.logged_in = True

    def logout():
        authenticator.logout()
        # Mostrar el formulario de autenticación
        if st.session_state["name"]:
            st.write(f'Welcome *{st.session_state["name"]}*')
        if st.session_state['authentication_status'] is False:
            st.session_state.logged_in = False
        elif st.session_state['authentication_status'] is None:
            st.session_state.logged_in = False

    logout_page = st.Page(logout, title="Usuario", icon=":material/logout:")

    dashboard = st.Page(
        "reports/visual.py", title="Analisis Leads", icon=":material/dashboard:"
    )

    ventas = st.Page("tools/asistente_ventas.py", title="Asistente Venta", icon=":material/robot_2:")
    resumen = st.Page("tools/asistente_resumen.py", title="Asistente Resumen", icon=":material/smart_toy:")

    if st.session_state.logged_in:
        pg = st.navigation(
            {
                "Inicio": [logout_page],
                "Reports": [dashboard],
                "Tools": [ventas, resumen],
            }
        )
    else:
        pg = st.navigation({})

    pg.run()