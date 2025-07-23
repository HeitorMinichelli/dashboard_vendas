import streamlit as st
import requests
import pandas as pd
import time

@st.cache_data
def converte_csv(df):
    return df.to_csv(index = False).encode('utf-8')


def mensagem_secesso():
    sucesso = st.success('Arquivo baixado com sucesso!', icon = '✅')
    time.sleep(5)
    sucesso.empty()

st.title('DADOS BRUTOS')

url = 'https://labdados.com/produtos'

response = requests.get(url, verify=False)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')


st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do Produto'):
    produtos = st.multiselect('Selecione os Produtos', dados['Produto'].unique())
    if produtos:
        dados = dados[dados['Produto'].isin(produtos)]

with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0, 5000))
    if preco:
        dados = dados[(dados['Preço'] >= preco[0]) & (dados['Preço'] <= preco[1])]


with st.sidebar.expander('Data da Compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))
    if data_compra:
        dados = dados[(dados['Data da Compra'] >= pd.to_datetime(data_compra[0])) &
                      (dados['Data da Compra'] <= pd.to_datetime(data_compra[1]))]
        
with st.sidebar.expander('Categoria do Produto'):
    categoria = st.multiselect('Selecione a Categoria', dados['Categoria do Produto'].unique())
    if categoria:
        dados = dados[dados['Categoria do Produto'].isin(categoria)]

with st.sidebar.expander('Frete do Produto'):
    frete = st.slider('Selecione o valor do frete', 0.0, float(dados['Frete'].max().round(0)), (0.0, float(dados['Frete'].max().round(0))))
    dados = dados[(dados['Frete'] >= frete[0]) & (dados['Frete'] <= frete[1])]

with st.sidebar.expander('Vendedores'):
    vendedores = st.multiselect('Vendedores', dados['Vendedor'].unique())
    if vendedores:
        dados = dados[dados['Vendedor'].isin(vendedores)]

with st.sidebar.expander('Estado'):
    estado = st.multiselect('Seleione o Estado da compra', dados['Local da compra'].unique())
    if estado:
        dados = dados[dados['Local da compra'].isin(estado)]

with st.sidebar.expander('Avaliação da Compra'):
    avaliacao = st.slider('Selecione a avaliação', 0, int(dados['Avaliação da compra'].max()), (0, int(dados['Avaliação da compra'].max())))
    dados = dados[(dados['Avaliação da compra'] >= avaliacao[0]) & (dados['Avaliação da compra'] <= avaliacao[1])]

with st.sidebar.expander('Tipo de Pagamento'):
    tipo_pagamento = st.multiselect('Selecione o Tipo de pagamento', dados['Tipo de pagamento'].unique())
    if tipo_pagamento:
        dados = dados[dados['Tipo de pagamento'].isin(tipo_pagamento)]
with st.sidebar.expander('Qtd de Parcelas'):
    parcelas = st.slider('Selecione a qtd de parcelas', 0, int(dados['Quantidade de parcelas'].max()), (0, int(dados['Quantidade de parcelas'].max())))
    dados = dados[(dados['Quantidade de parcelas'] >= parcelas[0]) & (dados['Quantidade de parcelas'] <= parcelas[1])]

# query = '''
# Produto in @produtos and \
# @preco[0] <= Preço <= @preco[1] and \
# @data_compra[0] <= `Data da Compra` <= @data_compra[1]
# '''

# dados_filtrados = dados.query(query)
# dados_filtrados = dados_filtrados[colunas]

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as Colunas', list(dados.columns), list(dados.columns))
    if colunas:
        dados = dados[colunas]

st.dataframe(dados)

st.markdown(f'A tabela possuí :blue[{dados.shape[0]}] linhas e :blue[{dados.shape[1]}] colunas')

st.markdown('Escreva um nome para o arquivo')
col1, col2 = st.columns(2)
with col1:
    nome_arquivo = st.text_input('', label_visibility='collapsed', value = 'dados')
    nome_arquivo += '.csv'
with col2:
    st.download_button('Fazer o download da tabela em csv', data = converte_csv(dados), file_name=nome_arquivo, mime = 'text/csv', on_click= mensagem_secesso)
