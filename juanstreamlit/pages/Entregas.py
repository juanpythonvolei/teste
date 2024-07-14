import streamlit as st
import requests
requisicao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requisicao.json()
dados = roteiro['bancodedadosroteirooficial']
  # Exibe a seleção da data
lista_total = [item for item in dados]
# Carrega os dados do banco de dados
opcao_selecionada_data = st.selectbox("Selecione uma data", lista_total)
botao = st.button('Iniciar Nova Rota')
checkbox_states = {}
try:
    lista_alerta = []
    lista_conferida = []
    lista_notas = []
    for item in dados:
                            
                            roteiro = dados[f'{item}']
                            for elemento in roteiro:
                                        nota = roteiro[f'{elemento}']
                                        data_emit = nota['Data de Emissão']
                                        if data_emit == opcao_selecionada_data:
                                          status = nota['status']
                                          if status == 'Entrega não completa':
                                            volumes = nota['Volumes']
                                            numero_nota = nota['Número da Nota']
                                            lista_notas.append(numero_nota)
                                            valor = nota['Valor Total']
                                            cliente = nota['Cliente']
                                                                  
                                                                  
                                                                      # Usa o dicionário para controlar o estado da checkbox
                                            checkbox_states[numero_nota] = st.checkbox(f"Cliente: {cliente}. Nota: {numero_nota}. Volumes: {volumes}", key=numero_nota)
                                          else:
  
                                            st.warning('Entrega Completa')
except:
      pass
  
  
      
      # Agora você pode usar o dicionário 'checkbox_states' conforme necessário
  
for nota, estado in checkbox_states.items():
          if estado:
              status = 'Feito'
              lista_conferida.append(status)
              if len(lista_conferida) == len(lista_notas):
                          requisicao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                          roteiro = requisicao.json()
                          dados = roteiro['bancodedadosroteirooficial']
                          for item in dados:
                                      roteiro = dados[f'{item}']
                                      for elemento in roteiro:
                                          nota = roteiro[f'{elemento}'] 
                                          data = nota['Data de Emissão']
                                          if data == opcao_selecionada_data:
                                            status = nota['status']
                                            link = f'https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/bancodedadosroteirooficial/{opcao_selecionada_data}/{elemento}/status.json'
                                            dados = '{"status": "Entrega realizada"}'
                                            requests.patch(link, data=dados)
                                               
                          st.warning('Entrega realizada com Sucesso')
              else:
                          pass
          else:
              try:
                          status = 'Feito'
                          lista_conferida.remove(status)
              except:
                          pass
col1, col2, col3 = st.columns(3)
        
        # Estilização CSS embutida
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

try:
  lista = []
  lista_conferencia = []
  for a in dados:
                              
                              roteiro = dados[f'{a}']
                              for elemento in roteiro:
                                          nota = roteiro[f'{elemento}']
                                          data_emit = nota['Data de Emissão']
                                          if data_emit == opcao_selecionada_data:
                                            numero_nota = nota['Número da Nota']
                                            lista.append(numero_nota)
                                            valor = nota['Valor Total']
                                            valor_final += valor
                                            status = nota['status']
                                            status.append(status)
except:
  pass  
if  'Entrega não completa' in lista_conferencia:
                                              with col1:
                                                          st.markdown(f'<div class="my-square">Total Notas:{len(lista_conferida)}</div>', unsafe_allow_html=True)
                                              with col2:
                                                          st.markdown(f'<div class="my-square">Total Destinos</div>', unsafe_allow_html=True)
                                              with col3:
                                                          st.markdown(f'<div class="my-square">Total valor</div>', unsafe_allow_html=True)
else:
                                              with col1:
                                                          st.markdown(f'<div class="my-square">Total Notas:{len(lista_conferida)}</div>', unsafe_allow_html=True)
                                              with col2:
                                                          st.markdown(f'<div class="my-square">Valor: </div>', unsafe_allow_html=True)
                                              with col3:
                                                          st.markdown(f'<div class="my-square">Situação: </div>', unsafe_allow_html=True)
                                              
                                              
    # Exibe as notas com checkboxes
