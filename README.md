# 3 - Agente asistente de ventas - Aplicacion web

Este proyecto es una aplicación desarrollada en Python que utiliza Streamlit para la creación de interfaces de usuario interactivas. Está diseñado para ser ejecutado en un entorno de streamlit cloud, facilitando su configuración y despliegue.

## Contenidos del repositorio

- `.devcontainer/`: Configuración para entornos de desarrollo en contenedores de streamlit.
- `.github/`: Flujos de trabajo y configuraciones específicas de GitHub.
- `.streamlit/`: Archivos de configuración de Streamlit.
- `reports/`: Directorio destinado a informes generados por la aplicación.
- `src/`: Código fuente principal de la aplicación.
- `tools/`: Herramientas auxiliares para el desarrollo y despliegue.
- `.gitignore`: Especifica los archivos y directorios que Git debe ignorar.
- `LICENSE`: Licencia Apache 2.0 que rige el uso del proyecto.
- `README.md`: Este archivo.
- `config.yaml`: Archivo de configuración de la aplicación.
- `requirements.txt`: Lista de dependencias de Python necesarias.
- `streamlit_app.py`: Script principal para ejecutar la aplicación Streamlit.

## Tecnologías utilizadas

- **Python**: Lenguaje de programación principal.
- **Streamlit**: Framework para la creación de aplicaciones web interactivas en Python.
- **Supabase**: Base de datos alojada en Supabase en Postgres.
- **Pandas**: Pandas es una librería de Python especializada en la manipulación y el análisis de datos.
- **OpenAI**: cliente de OpenAI
- **Streamlit**: Streamlit open-source Python framework
- **plotly.express**: Plotly Express es una API consistente y de alto nivel para crear figuras.

## Configuración del entorno de desarrollo

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/santiagorodriguez-dev/pf_03_front_end.git
   cd pf_03_front_end
   ```
## Instalación de dependencias

1. **Crear un entorno virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows use venv\Scripts\activate
   ```

2. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Fichero de configuración (\.streamlit\secrets.toml)**:
   ```bash
   [cookie]
   expiry_days = 1
   key = "void"
   name = "void"

   [credentials]
   usernames = {usuario = {email = "void@void.com", name = "void", password = "void"}}

   [preauthorized]
   emails = ["void@void.com"]

   [security]
   SUPABASE_URL='void'
   SUPABASE_KEY='void'
   OPENAI_API_KEY='void'
   OPENAI_API_ASSIS_VENTA='void'
   OPENAI_API_ASSIS_CONVERSACION='void'
   ```

## Ejecución de la aplicación

Para ejecutar la aplicación Streamlit:

1. **Asegúrese de que el entorno virtual esté activado**.

2. **Ejecute el script principal**:
   ```bash
   streamlit run streamlit_app.py
   ```

## Configuración

La aplicación utiliza un archivo de configuración `config.yaml` ubicado en la raíz del proyecto. Asegúrese de revisar y modificar este archivo según sus necesidades antes de ejecutar la aplicación.

## Licencia

Este proyecto está licenciado bajo la Licencia Apache 2.0. Consulte el archivo `LICENSE` para obtener más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abra un "issue" o envíe una "pull request" para mejoras, correcciones de errores o nuevas características.

## Contacto

Para preguntas o soporte, puede contactar al mantenedor del proyecto a través de su perfil de GitHub: [santiagorodriguez-dev](https://github.com/santiagorodriguez-dev).

