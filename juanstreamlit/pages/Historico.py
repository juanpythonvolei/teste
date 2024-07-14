import streamlit as st
import requests

lista_total = []
destinos_info = []
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
dados = roteiro['bancodedadosroteirooficial']
base_url2 = "https://www.google.com/maps/dir/"
texto_historico = []
for item in dados:
                roteiro = dados[f'{item}']
                lista_total.append(item)
opcao_selecionada = st.selectbox("Selecione uma data", lista_total)
if opcao_selecionada:
        for item in dados:
            roteiro = dados[f'{item}']
            for elemento in roteiro:
                nota = roteiro[f'{elemento}']
                data = nota['Data de Emissão']
                if  data == opcao_selecionada:
                    volumes = nota['Volumes']
                    numero_nota = nota['Número da Nota']
                    valor = nota['Valor Total']
                    cliente = nota['Cliente']
            historico = f'Data: {data}\n Volumes:{volumes}\n Numero: {numero_nota}\n Valor: {valor}\n Cliente: {cliente}'
            texto_historico.append(historico)

for item in texto_historico:
    css_style = """
                                                                        .my-square {
                                                                            background-color:#0275b1;
                                                                            border-radius: 10px;
                                                                            display: flex;
                                                                            justify-content: center;
                                                                            align-items: center;
                                                                            color: white;
                                                                        }
                                                                    """
                                                                    
                                                                    # Aplicando o estilo e inserindo os quadrados

    st.markdown(f"<style>{css_style}</style>", unsafe_allow_html=True)
    st.markdown(f'<div class="my-square">{item}</div>', unsafe_allow_html=True)



