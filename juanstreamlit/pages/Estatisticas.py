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
data = {'Nome': ['Alice', 'Bob', 'Carol'],
        'Idade': [25, 30, 22]}
df = pd.DataFrame(data)

# Exibindo a tabela no Streamlit
st.table(df)
