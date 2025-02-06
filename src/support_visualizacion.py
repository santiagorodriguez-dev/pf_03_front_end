# Importaciones

import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
import plotly.express as px # type: ignore

import sys
sys.path.append("../")
from src import support_bd as bd

import warnings
warnings.filterwarnings("ignore")

def visualizar_datos_all_leads(st, df):
    """
    Genera visualizaciones interactivas para analizar los datos de los leads y sus scores.

    Parámetros:
    - st: módulo de Streamlit para la visualización interactiva.
    - df: DataFrame de pandas con los datos de los leads.

    Visualizaciones:
    1. Score en función del nivel de estudios.
    2. Score en función de la especialidad.
    3. Score en función de la edad.
    4. Top 5 motivos de compra con mayor score.

    Se utilizan gráficos de Plotly Express para una mejor interactividad.
    """
    st.title("Análisis de Leads y Scores")

    st.dataframe(df)

    # Gráfico 1: Score en función del nivel de estudios
    st.subheader("Score en Función del Nivel de Estudios")
    fig_estudios = px.bar(
        df.groupby("estudios")["score"].mean().reset_index(),
        x="estudios", y="score",
        title="Score Promedio por Nivel de Estudios",
        labels={"estudios": "Nivel de Estudios", "score": "Score Promedio"},
        color="score",
        color_continuous_scale="viridis"
    )
    st.plotly_chart(fig_estudios)

    # Gráfico 2: Score en función de la especialidad
    st.subheader("Score en Función de la Especialidad")
    fig_especialidad = px.bar(
        df.groupby("especialidad")["score"].mean().reset_index(),
        x="especialidad", y="score",
        title="Score Promedio por Especialidad",
        labels={"especialidad": "Especialidad", "score": "Score Promedio"},
        color="score",
        color_continuous_scale="viridis"
    )
    st.plotly_chart(fig_especialidad)

    # Gráfico 3: Score en función de la edad
    st.subheader("Score en Función de la Edad")
    fig_edad = px.scatter(
        df, x="edad", y="score",
        title="Distribución del Score por Edad",
        labels={"edad": "Edad", "score": "Score"},
        color="score",
        color_continuous_scale="viridis",
        size_max=10
    )
    st.plotly_chart(fig_edad)

    # Gráfico 4: Top 5 Motivos de Compra con Mayor Score
    st.subheader("Top 5 Motivos de Compra con Mayor Score")
    top_motivos = df.groupby("motivo_compra")["score"].median().nlargest(5).reset_index()
    fig_motivos = px.bar(
        top_motivos, x="score", y="motivo_compra",
        orientation="h",
        title="Top 5 Motivos de Compra con Mayor Score",
        labels={"motivo_compra": "Motivo de Compra", "score": "Score Promedio"},
        color="score",
        color_continuous_scale="viridis"
    )
    st.plotly_chart(fig_motivos)

def visualizar_datos_top_leads(st, df):
    """
    Genera un dashboard con KPIs y visualizaciones para analizar el top 10% de los leads con mayor score.

    Parámetros:
    - st: módulo de Streamlit para la visualización interactiva.
    - df: DataFrame de pandas con los datos de los leads.

    Métricas y visualizaciones incluidas:
    1. Edad promedio y score promedio del top 10%.
    2. Distribución del nivel de estudios.
    3. Especialidad más frecuente.
    4. Distribución de género.
    5. Mapa con las ciudades con más usuarios del top 10%.
    6. Tabla con los datos del top 10% de scores.

    Se emplean gráficos de barras, gráficos de pastel y mapas interactivos usando Plotly.
    """
    # Filtrar el top 10% de scores
    umbral_score = df["score"].quantile(0.90)
    df_top_score = df[df["score"] >= umbral_score]

    # Calcular KPIs
    edad_promedio_top = df_top_score["edad"].mean()
    distribucion_estudios_top = df_top_score["estudios"].value_counts(normalize=True).reset_index()
    distribucion_estudios_top.columns = ["Nivel de Estudios", "Proporción"]
    distribucion_estudios_top["Proporción"] *= 100  # Convertir a porcentaje

    especialidad_frecuente_top = df_top_score["especialidad"].value_counts().idxmax()
    distribucion_genero_top = df_top_score["sexo"].value_counts()
    score_promedio_top = df_top_score["score"].mean()
    ciudades_mas_usuarios_top = df_top_score["ciudad"].value_counts().reset_index()
    ciudades_mas_usuarios_top.columns = ["ciudad", "usuarios"]

    # Coordenadas de las ciudades
    ciudades_coords = {
        "Murcia": [37.9922, -1.1307],
        "Jaén": [37.7796, -3.7842],
        "Granada": [37.1773, -3.5986],
        "Toledo": [39.8628, -4.0273],
        "Albacete": [38.9950, -1.8554],
        "Madrid": [40.4165, -3.70256]
    }

    # Agregar coordenadas
    ciudades_mas_usuarios_top["lat"] = ciudades_mas_usuarios_top["ciudad"].map(lambda x: ciudades_coords.get(x, [0, 0])[0])
    ciudades_mas_usuarios_top["lon"] = ciudades_mas_usuarios_top["ciudad"].map(lambda x: ciudades_coords.get(x, [0, 0])[1])

    lat_centro = 40.4165
    lon_centro = -3.70256

    # Configuración de la app
    st.title("Dashboard de KPIs - Top 10% Scores")
    st.write("Análisis de los usuarios con los mejores scores")

    # Mostrar KPIs
    col1, col2 = st.columns(2)
    col1.metric(label="Edad Promedio", value=f"{edad_promedio_top:.2f} años")
    col2.metric(label="Score Promedio", value=f"{score_promedio_top:.2f}")

    # Gráfico 1: Distribución de Estudios (%)
    st.subheader("Distribución de Estudios (%)")
    fig_estudios = px.bar(
        distribucion_estudios_top,
        x="Nivel de Estudios",
        y="Proporción",
        labels={"Nivel de Estudios": "Nivel de Estudios", "Proporción": "Porcentaje"},
        title="Distribución de Estudios",
        color="Nivel de Estudios",
        color_discrete_sequence=px.colors.sequential.Viridis_r
    )

    st.plotly_chart(fig_estudios)

    # Especialidad más frecuente
    st.subheader("Especialidad Más Frecuente")
    st.markdown(f"#### **{especialidad_frecuente_top}**")

    # Gráfico 2: Distribución por Género (Gráfico de Queso)
    st.subheader("Distribución por Género (%)")
    fig_genero = px.pie(
        names=distribucion_genero_top.index,
        values=distribucion_genero_top.values,
        title="Distribución por Género",
        color_discrete_sequence=px.colors.sequential.Viridis_r
    )
    st.plotly_chart(fig_genero)

    # Gráfico 3: Mapa de ciudades con más usuarios
    st.subheader("Top Ciudades con Más Usuarios")
    fig_map = px.scatter_mapbox(
        ciudades_mas_usuarios_top,
        lat="lat",
        lon="lon",
        size="usuarios",
        hover_name="ciudad",
        title="Usuarios por Ciudad",
        mapbox_style="open-street-map",
        zoom=3,
        color="usuarios",
        color_continuous_scale="viridis",
        center={"lat": lat_centro, "lon": lon_centro}  # Centrar el mapa en los datos
    )
    st.plotly_chart(fig_map)

    # Mostrar tabla con datos
    st.subheader("Datos (Top 10%)")
    st.dataframe(df_top_score.head(10))





