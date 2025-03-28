# calendar_app.py
import streamlit as st
import calendar
from datetime import datetime
import json
import os

# Configuração da página
st.set_page_config(
    page_title="Calendário Interativo",
    layout="wide",
)

# CSS personalizado para tema tecnológico
st.markdown("""
<style>
    .main {
        background-image: linear-gradient(to bottom right, #041E42, #1E3A8A);
        color: white;
    }
    .stButton button {
        background-color: rgba(0, 100, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 5px;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: rgba(0, 150, 255, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.5);
        transform: scale(1.05);
    }
    .hoje {
        border: 2px solid #00BFFF !important;
        background-color: rgba(0, 191, 255, 0.3) !important;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(to bottom, #0D324D, #1D2B53);
    }
    h1, h2, h3 {
        color: #00BFFF;
    }
    .login-container {
        background-color: rgba(0, 30, 60, 0.7);
        padding: 30px;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        margin: 100px auto;
        max-width: 500px;
        box-shadow: 0 0 20px rgba(0, 191, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Função para salvar e carregar eventos
def salvar_evento(data, evento):
    arquivo = "eventos.json"
    eventos = {}
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            eventos = json.load(f)
    
    if data not in eventos:
        eventos[data] = []
    eventos[data].append(evento)
    
    with open(arquivo, "w") as f:
        json.dump(eventos, f)

def carregar_eventos(data):
    arquivo = "eventos.json"
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            eventos = json.load(f)
            return eventos.get(data, [])
    return []

# Sistema de login
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.title("🔒 Acesso ao Calendário")
    st.write("Por favor, digite a senha para acessar o calendário:")
    senha = st.text_input("Senha", type="password")
    login_button = st.button("Entrar")
    
    if login_button:
        if senha.lower() == "genesis factory":
            st.session_state.autenticado = True
            st.experimental_rerun()
        else:
            st.error("Senha incorreta! Tente novamente.")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Título
    st.title("📅 Calendário Interativo")
    st.markdown("<h4 style='color: #00BFFF;'>Gerenciador de Agenda Tecnológica</h4>", unsafe_allow_html=True)

    # Pegar data atual
    today = datetime.today()
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        year = st.selectbox("Ano", list(range(2020, 2031)), index=list(range(2020, 2031)).index(today.year))
    with col2:    
        month = st.selectbox("Mês", list(calendar.month_name)[1:], index=today.month - 1)
    
    # Botão para sair
    if st.sidebar.button("Sair"):
        st.session_state.autenticado = False
        st.experimental_rerun()

    # Gerar o calendário
    st.subheader(f"{month} {year}")
    cal = calendar.monthcalendar(year, list(calendar.month_name).index(month))

    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    colunas = st.columns(7)

    for i in range(7):
        colunas[i].markdown(f"<h4 style='text-align: center; color: #00BFFF;'>{dias_semana[i]}</h4>", unsafe_allow_html=True)

    # Verificar se há eventos para o mês atual
    hoje_dia = today.day
    hoje_mes = today.month
    hoje_ano = today.year

    # Variável para controlar qual dia foi clicado
    if 'dia_selecionado' not in st.session_state:
        st.session_state.dia_selecionado = None

    # Renderizar o calendário
    for semana in cal:
        colunas = st.columns(7)
        for i, dia in enumerate(semana):
            if dia == 0:
                colunas[i].markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
            else:
                # Verificar se é o dia atual
                is_hoje = (dia == hoje_dia and 
                           list(calendar.month_name).index(month) == hoje_mes and 
                           year == hoje_ano)
                
                # Formatar a data para buscar eventos
                data_str = f"{dia}-{month}-{year}"
                
                # Verificar se há eventos para esse dia
                eventos = carregar_eventos(data_str)
                tem_evento = len(eventos) > 0
                
                # Estilo do botão
                if is_hoje:
                    button_class = "hoje"
                else:
                    button_class = ""
                
                # Indicador de evento
                evento_indicator = "🔴" if tem_evento else ""
                
                # Botão do dia com indicador de evento
                if colunas[i].button(f"{dia} {evento_indicator}", 
                                  key=f"{dia}-{month}-{year}",
                                  use_container_width=True):
                    st.session_state.dia_selecionado = data_str

    # Modal para mostrar/adicionar eventos do dia selecionado
    if st.session_state.dia_selecionado:
        with st.expander(f"📆 Agenda para {st.session_state.dia_selecionado}", expanded=True):
            st.subheader(f"Eventos para {st.session_state.dia_selecionado}")
            
            # Carregar e mostrar eventos existentes
            eventos = carregar_eventos(st.session_state.dia_selecionado)
            if eventos:
                for i, evento in enumerate(eventos):
                    st.markdown(f"**{i+1}.** {evento}")
            else:
                st.info("Nenhum evento programado para este dia.")
            
            # Adicionar novo evento
            st.subheader("Adicionar Novo Evento")
            novo_evento = st.text_input("Descrição do evento")
            horario = st.time_input("Horário do evento")
            
            if st.button("Salvar Evento"):
                if novo_evento:
                    evento_completo = f"{horario.strftime('%H:%M')} - {novo_evento}"
                    salvar_evento(st.session_state.dia_selecionado, evento_completo)
                    st.success("Evento adicionado com sucesso!")
                    st.experimental_rerun()
                else:
                    st.warning("Por favor, adicione uma descrição para o evento.")
            
            if st.button("Fechar"):
                st.session_state.dia_selecionado = None
                st.experimental_rerun()

