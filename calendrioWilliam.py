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

# Carregar o arquivo CSV diretamente da pasta local
file_path = "olímpiadas - Página1 (2)_1.csv"
try:
    df_events = pd.read_csv(file_path, parse_dates=["Início", "Fim"], dayfirst=True)
    df_events["Início"] = pd.to_datetime(df_events["Início"], dayfirst=True, errors="coerce")
    df_events["Fim"] = pd.to_datetime(df_events["Fim"], dayfirst=True, errors="coerce")
    
    # Dicionário para armazenar eventos por data
    dates_dict = {}
    
    for _, row in df_events.iterrows():
        event_name = f"📌 {row['Nome']}"

        # Adicionar data de início se existir
        if pd.notna(row["Início"]):
            start_date_str = row["Início"].strftime("%d/%m")
            start_event = f"{event_name} (Início)"
            if start_date_str in dates_dict:
                dates_dict[start_date_str] += f"\n{start_event}"
            else:
                dates_dict[start_date_str] = start_event
        
        # Adicionar data de fim se existir
        if pd.notna(row["Fim"]):
            end_date_str = row["Fim"].strftime("%d/%m")
            end_event = f"{event_name} (Fim)"
            if end_date_str in dates_dict:
                dates_dict[end_date_str] += f"\n{end_event}"
            else:
                dates_dict[end_date_str] = end_event

except FileNotFoundError:
    st.error(f"O arquivo {file_path} não foi encontrado. Certifique-se de que ele está na mesma pasta do código.")
    df_events = pd.DataFrame(columns=["Nome", "Início", "Fim"])
    dates_dict = {}
except Exception as e:
    st.error(f"Erro ao processar o arquivo CSV: {e}")
    df_events = pd.DataFrame(columns=["Nome", "Início", "Fim"])
    dates_dict = {}

# Criar coluna com as datas e marcar eventos no calendário
df_calendar["Data"] = df_calendar["Dia"].astype(str).str.zfill(2) + "/" + df_calendar["Mês"].astype(str).str.zfill(2)
df_calendar["Evento"] = df_calendar["Data"].map(dates_dict).fillna("-")

# Sidebar para filtro por mês
st.sidebar.subheader("Filtrar por Mês")
selected_month = st.sidebar.selectbox("Escolha um mês", list(range(1, 13)), format_func=lambda x: calendar.month_name[x])

# Filtrar o DataFrame para o mês selecionado
df_filtered = df_calendar[df_calendar["Mês"] == selected_month]

# Exibir apenas os eventos do mês escolhido
st.write(f"### 📌 Eventos no mês de {calendar.month_name[selected_month]}")
st.data_editor(df_filtered, height=400, use_container_width=True)  # Apenas a tabela filtrada

st.sidebar.info("O calendário está sendo carregado automaticamente do arquivo local.")
