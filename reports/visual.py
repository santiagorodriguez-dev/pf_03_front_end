import streamlit as st # type: ignore

import sys
sys.path.append("../")

from src import support_bd as bd

st.title('Analisis Potenciales Leads')
st.dataframe(bd.select_datos("leads",st))