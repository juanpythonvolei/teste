import streamlit as st
import requests
from streamlit_option_menu import option_menu
lista_total = []
destinos_info = []
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
dados = roteiro['bancodedadosroteirooficial']
base_url2 = "https://www.google.com/maps/dir/"
selected = option_menu("Menu Principal", ["Historico de Entregas", "Produtos das entregas"], icons=["file", "shop"], default_index=1)
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
if selected == 'Historico de Entregas':
          for item in dados:
                      try:               
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
                      except:        
                              st.warning('Roteiro não está disponível')
elif selected ==  "Produtos das entregas":
          lista_total = []
          destinos_info = []
          requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
          roteiro = requiscao.json()
          dados = roteiro['bancodedadosroteirooficial']
          base_url2 = "https://www.google.com/maps/dir/"
          try:
                    for item in dados:
                                    roteiro = dados[f'{item}']
                                    lista_total.append(item)
                    opcao_selecionada = st.selectbox("Selecione uma data", lista_total)
                    for item in dados:
                                texto_historico = ''
                                roteiro = dados[f'{item}']
                                for elemento in roteiro:
                                        nota = roteiro[f'{elemento}']
                                        data = nota['Data de Emissão']    
                                        if data == opcao_selecionada:
                                                  volumes = nota['Volumes']
                                                  numero_nota = nota['Número da Nota']
                                                  valor = nota['Valor Total']
                                                  cliente = nota['Cliente']
                                                  produtos = nota['Produtos']
                                                  historico = f'''
                                                  
                    Data: {data}\n              
                    Numero: {numero_nota}\n
                    Produtos: {produtos}\n
                                                  
                                                  
                                                  '''               
                                                  texto_historico += historico
                                st.markdown(f'<div class="my-square">{texto_historico}</div>', unsafe_allow_html=True)    
          except:
                    st.warnig('Roteiro não está disponível')
          
    
     


