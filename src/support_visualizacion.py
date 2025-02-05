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

    - Score en función del nivel de estudios.
    - Score en función de la especialidad.
    - Score en función de la edad.
    - Top 5 motivos de compra con mayor score.

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
        color_continuous_scale="plasma"
    )
    st.plotly_chart(fig_especialidad)

    # Gráfico 3: Score en función de la edad
    st.subheader("Score en Función de la Edad")
    fig_edad = px.scatter(
        df, x="edad", y="score",
        title="Distribución del Score por Edad",
        labels={"edad": "Edad", "score": "Score"},
        color="score",
        color_continuous_scale="magma",
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
        color_continuous_scale="cividis"
    )
    st.plotly_chart(fig_motivos)


def visualizar_datos_top_leads(st, df):
# Filtrar el top 10% de scores
    umbral_score = df["score"].quantile(0.90)
    df_top_score = df[df["score"] >= umbral_score]

    # Calcular KPIs
    edad_promedio_top = df_top_score["edad"].mean()
    distribucion_estudios_top = df_top_score["estudios"].value_counts(normalize=True) * 100
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

    # Calcular centro del mapa
    lat_centro = 40.4165
    lon_centro = -3.70256

    # Configuración de la app
    st.title("Dashboard de KPIs - Top 10% Scores")
    st.write("Análisis de los usuarios con los mejores scores")

    # Mostrar KPIs
    st.subheader("Métricas Generales (Top 10%)")
    st.metric(label="Edad Promedio", value=f"{edad_promedio_top:.2f} años")
    st.metric(label="Score Promedio", value=f"{score_promedio_top:.2f}")

    st.subheader("Distribución de Estudios (%)")
    st.bar_chart(distribucion_estudios_top)

    st.subheader("Especialidad Más Frecuente")
    st.write(f"**{especialidad_frecuente_top}**")

    st.subheader("Distribución por Género (%) - Gráfico de Queso")
    fig_genero = px.pie(
        names=distribucion_genero_top.index,
        values=distribucion_genero_top.values,
        title="Distribución por Género"
    )
    st.plotly_chart(fig_genero)

    st.subheader("Top Ciudades con Más Usuarios - Mapa Interactivo")
    fig_map = px.scatter_mapbox(
        ciudades_mas_usuarios_top,
        lat="lat",
        lon="lon",
        size="usuarios",
        hover_name="ciudad",
        title="Usuarios por Ciudad",
        mapbox_style="open-street-map",
        zoom=3,
        center={"lat": lat_centro, "lon": lon_centro}  # Centrar el mapa
    )
    st.plotly_chart(fig_map)

    st.subheader("Datos (Top 10%)")
    st.dataframe(df_top_score.head(10))

