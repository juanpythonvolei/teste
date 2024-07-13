import streamlit as st
import requests

# Carrega os dados do banco de dados
requisicao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requisicao.json()
dados = roteiro['bancodedadosroteirooficial']

# Cria um dicionário para armazenar o estado das checkboxes
checkbox_states = {}

# Exibe a seleção da data
lista_total = [item for item in dados]
opcao_selecionada_data = st.selectbox("Selecione uma data", lista_total)

# Exibe as notas com checkboxes

for item in dados:
            roteiro = dados[item]
            for elemento in roteiro:
                        nota = roteiro[elemento]
                        volumes = nota['Volumes']
                        numero_nota = nota['Número da Nota']
                        valor = nota['Valor Total']
                        cliente = nota['Cliente']
                        data = nota['Data de Emissão']
                        if data == opcao_selecionada_data:
                            # Usa o dicionário para controlar o estado da checkbox
                            checkbox_states[numero_nota] = st.checkbox(f"Cliente: {cliente}. Nota: {numero_nota}. Volumes: {volumes}", key=numero_nota)
    
    # Agora você pode usar o dicionário 'checkbox_states' conforme necessário
st.write("Notas selecionadas:")
for nota, estado in checkbox_states.items():
        if estado:
            st.write(f"Nota {nota} marcada")
