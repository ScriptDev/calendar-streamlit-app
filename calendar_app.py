import streamlit as st
import calendar
from datetime import datetime

st.set_page_config(page_title="Calendário", layout="centered")

st.title("📅 Calendário Interativo")

today = datetime.today()
year = st.sidebar.selectbox("Ano", list(range(2020, 2031)), index=list(range(2020, 2031)).index(today.year))
month = st.sidebar.selectbox("Mês", list(calendar.month_name)[1:], index=today.month - 1)

st.subheader(f"{month} {year}")
cal = calendar.monthcalendar(year, list(calendar.month_name).index(month))

dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
colunas = st.columns(7)
for i in range(7):
    colunas[i].markdown(f"**{dias_semana[i]}**")

for semana in cal:
    colunas = st.columns(7)
    for i, dia in enumerate(semana):
        if dia == 0:
            colunas[i].write("")
        else:
            colunas[i].button(str(dia), key=f"{dia}-{month}-{year}")
