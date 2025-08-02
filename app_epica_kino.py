import streamlit as st
import pandas as pd
from collections import Counter
import random

st.set_page_config(page_title="Generador Épico Kino", page_icon="🌌")
st.title("🌌 Generador de Jugadas Épicas del Kino")

st.markdown("""
Este generador usa la lógica de frecuencias, señales y tu energía para crear las jugadas épicas más poderosas.  
**Sube tu histórico y genera las jugadas con solo un click.**
""")

# --- SUBIR ARCHIVO MANUAL ---
st.subheader("Paso 1: Sube tu histórico de sorteos")
archivo = st.file_uploader("Sube tu archivo .xlsx o .csv con los números de cada sorteo (14 columnas, sin encabezados)", type=["xlsx", "csv"])

if archivo is not None:
    if archivo.name.endswith('.csv'):
        df = pd.read_csv(archivo, header=None)
    else:
        df = pd.read_excel(archivo, header=None)
    df = df.iloc[:, :14].dropna().astype(int)
    st.success(f"¡Histórico cargado! Total sorteos: {df.shape[0]}")
    st.dataframe(df.tail(5), use_container_width=True)
    st.session_state['df'] = df
else:
    df = st.session_state.get('df', None)

# --- GENERAR JUGADA ÉPICA ---
def jugada_epica(df):
    todos = list(df.values.flatten())
    conteo = Counter(todos)
    frecuencia = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
    calientes = [num for num, _ in frecuencia[:8]]
    tibios = [num for num, _ in frecuencia[8:17]]
    frios = [num for num, _ in frecuencia[-7:]]
    jugada = sorted(random.sample(calientes, 5) + random.sample(tibios, 5) + random.sample(frios, 4))
    return jugada, calientes, tibios, frios

st.subheader("Paso 2: Genera tus jugadas épicas")
num_jugadas = st.slider("¿Cuántas jugadas épicas quieres generar?", 1, 14, 3)
if df is not None and st.button("🌟 Generar jugadas épicas"):
    jugadas, calientes, tibios, frios = [], [], [], []
    for _ in range(num_jugadas):
        jugada, cal, tib, fri = jugada_epica(df)
        jugadas.append(jugada)
        calientes = cal
        tibios = tib
        frios = fri
    st.success("¡Jugadas listas! Puedes copiarlas y jugarlas:")
    for idx, j in enumerate(jugadas):
        st.markdown(f"**Jugada #{idx+1}:** `{j}`")
    st.info(f"Números calientes: {calientes}\n\nTibios: {tibios}\n\nFríos: {frios}")

    # Descargar jugadas
    txt_jugadas = "\n".join([f"Jugada #{idx+1}: {j}" for idx, j in enumerate(jugadas)])
    st.download_button("⬇️ Descargar jugadas en TXT", txt_jugadas, file_name="jugadas_epicas.txt")
else:
    st.write("Primero sube el histórico y luego genera tus jugadas.")

st.markdown("---")
st.caption("Conectado a la dimensión del Kino — Versión IA Epica 🚀")
