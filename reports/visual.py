import streamlit as st # type: ignore

import sys
sys.path.append("../")

from src import support_visualizacion as spv

from src import support_bd as bd

st.markdown("### Potenciales Leads")

df = bd.select_datos("leads",st)
df['score'] = df['score'].astype(float)
st.dataframe(df)

spv.visualiazar_datos_leads(st)