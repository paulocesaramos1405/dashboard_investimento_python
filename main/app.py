import streamlit as st
import yfinance as yf
from datetime import date, timedelta
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objects as go

DATA_INICIO = '2017-01-01'
DATA_FIM = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')  

st.title('Análise de Ativos: Ações e Fundos Imobiliários')

st.sidebar.header('Escolha o tipo de ativo')

tipo_ativo = st.sidebar.radio('Selecione o tipo de ativo:', ('Ações', 'Fundos Imobiliários'))

def pegar_dados_acoes():
    path = 'acoes.csv'  # Caminho relativo
    return pd.read_csv(path, delimiter=';')

def pegar_dados_fundos():
    path = 'fundosimobiliarios.csv'  # Caminho relativo
    return pd.read_csv(path, delimiter=';')

if tipo_ativo == 'Ações':
    df = pegar_dados_acoes()
else:
    df = pegar_dados_fundos()

df['display'] = df['sigla_acao'] + " - " + df['snome']

acao = df['display']
nome_acao_escolhida = st.sidebar.selectbox('Escolha um ativo:', acao)

def_acao = df[df['display'] == nome_acao_escolhida]
acao_escolhida = def_acao.iloc[0]['sigla_acao']
acao_escolhida = acao_escolhida + '.SA'

def pegar_valores_online(sigla_acao):
    df = yf.download(sigla_acao, start=DATA_INICIO, end=DATA_FIM)
    df.reset_index(inplace=True)
    return df

df_valores = pegar_valores_online(acao_escolhida)

if df_valores.empty or df_valores['Date'].iloc[-1] < pd.Timestamp(DATA_FIM):
    st.warning("Os dados podem não estar atualizados para a data de hoje. Verifique a disponibilidade no Yahoo Finance.")
else:
    st.success("Dados atualizados até hoje.")

st.subheader(f'Tabela de valores - {nome_acao_escolhida}')
st.write(df_valores.tail(15))

st.subheader('Developed by Paulo César Ramos®')

st.markdown(
    """
    <a href="https://paulocesardeveloper.netlify.app/" target="_blank" style="text-decoration: none; font-size: 20px; color: #3498db;">
        Visite o Meu Site
    </a>
    """,
    unsafe_allow_html=True
)
