import streamlit as st
import requests

lista_total = []
destinos_info = []
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
dados = roteiro['bancodedadosroteirooficial']
base_url2 = "https://www.google.com/maps/dir/"
selected = option_menu("Menu Principal", ["Historico de Entregas", "Produtos das entregas"], icons=["database", "truck"], default_index=1)
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

for item in dados:
            texto_historico = ''
            roteiro = dados[f'{item}']
            for elemento in roteiro:
                    nota = roteiro[f'{elemento}']
                    volumes = nota['Volumes']
                    data = nota['Data de Emissão']    
                    numero_nota = nota['Número da Nota']
                    valor = nota['Valor Total']
                    cliente = nota['Cliente']
                    historico = f'''\n
                    
                    Data: {data}\n
                    Volumes: {volumes}\n                
                    Numero: {numero_nota}\n
                    Valor: {valor}\n    
                    Cliente: {cliente}
                    
                    \n
                    '''               
                    texto_historico += historico
            st.markdown(f'<div class="my-square">{texto_historico}</div>', unsafe_allow_html=True)      
    
     


