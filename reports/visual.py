import streamlit as st # type: ignore
import plotly.express as px # type: ignore

import sys
sys.path.append("../")

from src import support_visualizacion as spv

from src import support_bd as bd

df = bd.select_datos("leads",st)

spv.visualizar_datos_all_leads(st,df)

spv.visualizar_datos_top_leads(st,df)