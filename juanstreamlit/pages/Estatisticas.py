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
botao = st.button("Carregar Dados")

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

if botao:
    texto_nota = []
    lista_produtos = []
    lista_clientes = []
    lista_valores = []
    lista_notas = []
    lista_volumes = []
    for item in dados:
            roteiro = dados[f'{item}']
            for elemento in roteiro:
                nota = roteiro[f'{elemento}']
                if nota['Data de Emissão'] == opcao_selecionada:
                    for item in nota:
                        numero_nota = nota['Número da Nota']
                        if numero_nota in lista_notas:
                            pass
                        else:
                            lista_notas.append(numero_nota)
                        destino = nota['Destino']
                        if destino in texto_nota:
                            pass
                        else:    
                            texto_nota.append(destino)
                        data_De_emissao = nota['Data de Emissão']
                        volumes = nota['Volumes']
                        if volumes in lista_volumes:
                            pass
                        else:
                            lista_volumes.append(volumes)
                        cliente = nota['Cliente']
                        if cliente in lista_clientes:
                            pass
                        else:
                            lista_clientes.append(cliente)
                        Produtos = nota['Produtos'][0]
                        if Produtos in lista_produtos:
                            pass
                        else:
                            lista_produtos.append(Produtos)
                        status = nota['status']
                        valor  = nota['Valor Total']
                        if valor in lista_valores:
                            pass
                        else:
                            lista_valores.append(valor)
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
