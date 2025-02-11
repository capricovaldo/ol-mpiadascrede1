import streamlit as st
import pandas as pd
import calendar
from datetime import datetime

# Certificar-se de que openpyxl está instalado
try:
    import openpyxl
except ImportError:
    st.error("A biblioteca 'openpyxl' não está instalada. Instale com 'pip install openpyxl'.")

# Função para gerar um DataFrame com as datas do ano selecionado
def generate_calendar(year):
    months = []
    days = []
    for month in range(1, 13):
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            months.append(month)
            days.append(day)
    return pd.DataFrame({"Mês": months, "Dia": days})

# Título
title = "📅 Calendário de Inscrição das Olimpíadas Científicas"
st.title(title)

# Seleção do ano
current_year = datetime.now().year
selected_year = st.sidebar.number_input("Selecione o Ano", min_value=2000, max_value=2100, value=current_year, step=1)

# Geração do calendário
df_calendar = generate_calendar(selected_year)

# Carregar o arquivo Excel diretamente da pasta local
file_path = "olímpiadas - Página1 (2)_1.csv"
try:
    df_temp = pd.read_csv(file_path)
    st.write("Colunas encontradas no arquivo:", df_temp.columns)  # Debug: Verificar colunas
    
    df_events = pd.read_csv(file_path, parse_dates=["Início", "Fim"], dayfirst=True)
    df_events["Início"] = pd.to_datetime(df_events["Início"], dayfirst=True, errors="coerce")
    df_events["Fim"] = pd.to_datetime(df_events["Fim"], dayfirst=True, errors="coerce")
    
    dates_dict = {}
    for _, row in df_events.iterrows():
        if pd.notna(row["Início"]):
            start_date_str = row["Início"].strftime("%d/%m")
            dates_dict[start_date_str] = f"{row['Nome']} (Início)"
        if pd.notna(row["Fim"]):
            end_date_str = row["Fim"].strftime("%d/%m")
            dates_dict[end_date_str] = f"{row['Nome']} (Fim)"
except FileNotFoundError:
    st.error(f"O arquivo {file_path} não foi encontrado. Certifique-se de que ele está na mesma pasta do código.")
    df_events = pd.DataFrame(columns=["Nome", "Início das inscrições", "Fim das inscrições"])
    dates_dict = {}
except Exception as e:
    st.error(f"Erro ao processar o arquivo Excel: {e}")
    df_events = pd.DataFrame(columns=["Nome", "Início", "Fim"])
    dates_dict = {}

# Exibição do calendário
df_calendar["Data"] = df_calendar["Dia"].astype(str) + "/" + df_calendar["Mês"].astype(str).str.zfill(2)
df_calendar["Evento"] = df_calendar["Data"].map(dates_dict).fillna("-")

st.dataframe(df_calendar, height=600)

st.sidebar.subheader("Filtrar por Mês")
selected_month = st.sidebar.selectbox("Escolha um mês", list(range(1, 13)), format_func=lambda x: calendar.month_name[x])

df_filtered = df_calendar[df_calendar["Mês"] == selected_month]
st.write(f"### 📌 Eventos no mês de {calendar.month_name[selected_month]}")
st.dataframe(df_filtered, height=400)

st.sidebar.info("O calendário está sendo carregado automaticamente do arquivo local: olímpiadas.xlsx")
