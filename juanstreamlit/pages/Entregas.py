import streamlit as st
import requests

lista_total = []
destinos_info = []
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
dados = roteiro['bancodedadosroteirooficial']
base_url2 = "https://www.google.com/maps/dir/"
        
for item in dados:
                roteiro = dados[f'{item}']
                lista_total.append(item)
opcao_selecionada_data = st.selectbox("Selecione uma data", lista_total)
total = st.button("Iniciar Nova Entrega")
if total:
        lista_feita = []
        for item in dados:
                roteiro = dados[f'{item}']
                for elemento in roteiro:
                        nota = roteiro[f'{elemento}']
                        volumes = nota['Volumes']
                        numero_nota = nota['Número da Nota']
                        valor = nota['Valor Total']
                        cliente = nota['Cliente']
                        data = nota['Data de Emissão']
                        if data == opcao_selecionada_data:
                                opcao_selecionada = st.checkbox(f"Cliente: {cliente}. Nota: {numero_nota}. Volumes: {volumes}",key=f'{numero_nota}')
                                if opcao_selecionada:
                                        estado = 'feito'
                                        lista_feita.append(estado)
                                else:
                                        lista_feita.remove(estado)
            
