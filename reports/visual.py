import streamlit as st # type: ignore
import plotly.express as px

import sys
sys.path.append("../")

from src import support_visualizacion as spv

from src import support_bd as bd

st.markdown("### Potenciales Leads")

df = bd.select_datos("leads",st)
df['score'] = df['score'].astype(float)
st.dataframe(df)

spv.visualiazar_datos_leads(st)


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
st.subheader("📊 Métricas Generales (Top 10%)")
st.metric(label="Edad Promedio", value=f"{edad_promedio_top:.2f} años")
st.metric(label="Score Promedio", value=f"{score_promedio_top:.2f}")

st.subheader("📚 Distribución de Estudios (%)")
st.bar_chart(distribucion_estudios_top)

st.subheader("🎓 Especialidad Más Frecuente")
st.write(f"**{especialidad_frecuente_top}**")

st.subheader("👥 Distribución por Género (%) - Gráfico de Queso")
fig_genero = px.pie(
    names=distribucion_genero_top.index,
    values=distribucion_genero_top.values,
    title="Distribución por Género"
)
st.plotly_chart(fig_genero)

st.subheader("🌍 Top Ciudades con Más Usuarios - Mapa Interactivo")
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

st.subheader("📜 Vista Previa de Datos (Top 10%)")
st.dataframe(df_top_score.head(10))

# Pie de página
st.write("Aplicación creada con Streamlit")