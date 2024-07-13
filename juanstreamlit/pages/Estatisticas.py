import streamlit as st
import requests
import pandas as pd
css = """
<style>
.centered-image {
    display: block;
    margin: 0 auto;
}
</style>
"""

# Insere o CSS no aplicativo
st.markdown(css, unsafe_allow_html=True)

# Exibe a imagem centralizada
st.image('https://calscycle.ca/newsite/wp-content/uploads/2022/05/Thule.png', width=500)


lista_total = []
destinos_info = []
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
dados = roteiro['bancodedadosroteirooficial']
base_url2 = "https://www.google.com/maps/dir/"
        
for item in dados:
                roteiro = dados[f'{item}']
                lista_total.append(item)
opcao_selecionada = st.selectbox("Selecione uma data", lista_total)
col1, col2 = st.beta_columns(2)

# Adicionando botões em cada coluna
if col1.button('Dados Gerais'):
    texto_nota = []
    lista_produtos = []
    lista_clientes = []
    Lista_valores = []
    lista_notas = []
    lista_volumes = []
    for item in dados:
            roteiro = dados[f'{item}']
            for elemento in roteiro:
                nota = roteiro[f'{elemento}']
                if nota['Data de Emissão'] == opcao_selecionada:
                    for item in nota:
                        numero_nota = nota['Número da Nota']
                        destino = nota['Destino']
                        data_De_emissao = nota['Data de Emissão']
                        volumes = nota['Volumes']
                        cliente = nota['Cliente']
                        Produtos = nota['Produtos'][0]
                        status = nota['status']
                        valor  = nota['Valor Total']
                    texto_nota.append(destino)
                    lista_produtos.append(Produtos)
                    lista_clientes.append(cliente)
                    Lista_valores.append(valor)
                    lista_notas.append(numero_nota)
                    lista_volumes.append(volumes)
    data = {'Destino': texto_nota,
            'Valor da nota': Lista_valores,
            'Volumes':lista_volumes,
            'Cliente':lista_clientes,
            'Nota':lista_notas,
            'Data':data_De_emissao,
            'Status':status}
    df = pd.DataFrame(data)

    # Exibindo a tabela no Streamlit
    st.table(df)
elif col2.button('Dados da rota'):
    
