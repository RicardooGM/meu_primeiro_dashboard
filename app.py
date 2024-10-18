import streamlit as st
import pandas as pd
import pandas_datareader as web 
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import plotly.express as px
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.grid import grid

st.title("Dashboard de ações")
with st.sidebar:
    st.image("logo-b3-brasil-bolsa-balcao-2048.png")
    ticker_list = pd.read_csv("tickers_ibra.csv")
    tickers = st.multiselect(label="Selecione as Empresas", options=ticker_list, placeholder ='Códigos')
    start_date = st.date_input("De", format="DD/MM/YYYY", value=datetime(2005,1,2))
    end_date = st.date_input("Até", format="DD/MM/YYYY", value="today")

    if tickers:
        prices = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]
#tabela
ativos = ["^BVSP","PETR4.SA","VALE3.SA","ITUB4.SA","BBAS3.SA","ITSA4.SA","WEGE3.SA"]
ibov = yf.download(ativos, period="1d", interval="60m")["Adj Close"].dropna()
ibov.columns = ibov.columns.str.rstrip(".SA")
dados = (ibov.filter(items = ["^BVSP","PETR4","VALE3","ITUB4","BBAS3","ITSA4","WEGE3"], axis = "columns")
         .rename(columns = {"^BVSP":"IBOV",}))
st.table(dados)
#colocar variação percentual e selectbox

#["^BVSP","PETR4.SA","VALE3.SA","ITUB4.SA","BBAS3.SA","ITSA4.SA","WEGE3.SA"]

#grafico ibovespa
st.subheader("Ibovespas")
opcoes = st.selectbox("Anos",("1d","5d","1mo","3mo","1y","2y","5y","10y","ytd","max"),)
ibovespa = yf.download("^BVSP")["Adj Close"].dropna()
st.line_chart(ibovespa)
#colocar medias moveis - juntar o grafico do ibovespa com o grafico das açoes selecionadas, crir box para o ibovespa

#grafico1
st.subheader("Gráfico de ações")
st.line_chart(prices)

#grafico2
st.subheader("Retornos")
retorno = prices.pct_change().dropna()
retorno()
st.line_chart(retorno)

#grafico3
st.subheader("Retorno acumulativo")
log_return = np.log(prices/prices.shift(1))
acumulative_log_return = log_return.cumsum()
st.area_chart(acumulative_log_return, use_container_width=True)


#Correlaçao - TIRAR OS .SA DOS NOMES
st.subheader("Correlação dos retornos de ativos")
nome = st.text_input("Ação 1")
nome2 = st.text_input("Ação 2")
tempo = st.selectbox("Anos",("1y","2y","5y","10y","ytd","max"))
tabela1 = yf.download(nome)
tabela11 = (tabela1.filter(items = ["Open", "High","Low","Close","Adj Close","Volume"], axis = "columns")).rename(columns = {"Adj Close":"Preco de fechamento"})
tabela111 = tabela11["Preco de fechamento"].pct_change().dropna()
tabela2 = yf.download(nome2)["Adj Close"]
tabela22 = tabela2.pct_change().dropna()
tab_corr = pd.concat([tabela111,tabela22], axis = 1, join= "inner")
correlacao = px.scatter(tab_corr, x="Preco de fechamento", y="Adj Close", trendline="lowess", color="Preco de fechamento")
st.plotly_chart(correlacao)
#Tabela de correlação
r = np.corrcoef(tabela111,tabela22)
st.table(r)

#EDITAR AS TABELAS COM TABLE


#if len(tickers) == 1:
            #prices = prices.to_frame()
            #prices.columns = [tickers[0].rstrip(".SA")]