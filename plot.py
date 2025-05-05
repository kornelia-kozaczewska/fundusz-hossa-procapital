import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Dashboard portfela", layout="wide")
st.title("Interaktywny dashboard portfela (Plotly)")

DATA_URL = (
    "https://raw.githubusercontent.com/"
    "kornelia-kozaczewska/fundusz-hossa-procapital/"
    "main/portfolio.csv"
)
DATE_COL = "Data zrealizowania transakcji"
NAME_COL = "Nazwa spółki"

@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv(DATA_URL, sep=";")
    df.columns = df.columns.str.strip()
    df = df.loc[:, df.columns.str.strip() != ""]
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], format="%m/%d/%y", errors="coerce")
    return df.dropna(subset=[DATE_COL])

df = load_data()

# --- wybór zakresu dat z date_input zamiast slidera ---
min_d = df[DATE_COL].min().date()
max_d = df[DATE_COL].max().date()
start_d, end_d = st.date_input(
    "Wybierz zakres dat:",
    value=(min_d, max_d),
    min_value=min_d,
    max_value=max_d
)

# przefiltruj DataFrame po datach (porównujemy .date())
mask = (df[DATE_COL].dt.date >= start_d) & (df[DATE_COL].dt.date <= end_d)
df_filt = df.loc[mask]

# --- 1) Wykres liniowy: liczba transakcji miesięcznie ---
monthly = (
    df_filt
    .groupby(df_filt[DATE_COL].dt.to_period("M"))
    .size()
    .sort_index()
)
monthly.index = monthly.index.astype(str)
fig_line = px.line(
    x=monthly.index,
    y=monthly.values,
    labels={"x": "Miesiąc", "y": "Liczba transakcji"},
    title="Liczba transakcji w kolejnych miesiącach"
)
st.plotly_chart(fig_line, use_container_width=True)

# --- 2) Wykres słupkowy: TOP 10 spółek ---
top10 = df_filt[NAME_COL].value_counts().nlargest(10)
fig_bar = px.bar(
    x=top10.index,
    y=top10.values,
    labels={"x": "Spółka", "y": "Liczba transakcji"},
    title="TOP 10 najczęściej handlowanych spółek"
)
fig_bar.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_bar, use_container_width=True)

# --- rozwiń, żeby zobaczyć surowe dane ---
with st.expander("Pokaż surowe dane"):
    st.dataframe(df_filt, use_container_width=True)