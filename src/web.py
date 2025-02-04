

def load_web(st,authenticator):
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

    ventas = st.Page("tools/asistente_ventas.py", title="Asistente Venta", icon=":material/robot_2:" , default=True)
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