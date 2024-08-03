import streamlit as st
import requests
from streamlit_carousel import carousel
requisicao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requisicao.json()

     
dados = roteiro['bancodedadosroteirooficial']
  
    # Exibe a seleção da data
lista_total = [item for item in dados]
lista_nomes = []
lista_destinos = []
destinos_info = []
distancia_total = 0
items = []
dados2 = roteiro['Veículos']
for item in dados2:            
                            veiculo = dados2[f'{item}']
                            for elemento in veiculo:
                                   espec = veiculo[f'{elemento}']
                                   nome = espec['nome']
                                   img = espec['Foto']
                                   info = {
                                           "title": f"{nome}",
                                           "img":f"{img}",
                                       }
                                   lista_info.append(info)  
                                   lista_nomes.append(nome)
  # Carrega os dados do banco de dados
opcao_selecionada_data = st.selectbox("Selecione uma data", lista_total)
carousel(items=items, width=0.5)
veiculo = st.selectbox('Selecione um Veículo',lista_nomes)
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
                                          if str(data_emit) == str(opcao_selecionada_data):
                                            status = nota['status']
                                            if status == 'Entrega não completa':
                                              volumes = nota['Volumes']
                                              numero_nota = nota['Número da Nota']
                                              lista_notas.append(numero_nota)
                                              valor = nota['Valor Total']
                                              cliente = nota['Cliente']
                                              endereco = nota['Destino']
                                              lista_destinos.append(endereco)                      
                                                                    
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
                            requisicao_1 = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                            roteiro_1 = requisicao.json()
                            dados_1 = roteiro_1['bancodedadosroteirooficial']
                            for item in dados_1:
                                          roteiro = dados_1[f'{item}']
                                          for elemento in roteiro:
                                              nota = roteiro[f'{elemento}'] 
                                              data = nota['Data de Emissão']
                                              
                                              if data == opcao_selecionada_data:
                                                status = nota['status']
                                                link = f'https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/bancodedadosroteirooficial/{opcao_selecionada_data}/{elemento}/status.json'
                                                dados = '{"status": "Entrega realizada"}'
                                                requests.patch(link, data=dados)        
                                                link2 = f'https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/bancodedadosroteirooficial/{opcao_selecionada_data}/{elemento}/Veículo.json'
                                                dados2 = {"Veículo": veiculo}
                                                requests.post(link2, json=dados2)   
                            st.warning('Entrega realizada com Sucesso')
                               
                            
                           
                            
                                            
                                  
                else:
                            pass
            else:
                try:
                            status = 'Feito'
                            lista_conferida.remove(status)
                except:
                            pass
  
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
  
          
          # Estilização CSS embutida
  
 
                                     
                                
try:
    lista = []
    for a in dados:
                                
                                roteiro = dados[f'{a}']
                                for elemento in roteiro:
                                            nota = roteiro[f'{elemento}']
                                            data_emit = nota['Data de Emissão']
                                            if str(data_emit) == str(opcao_selecionada_data):
                                              numero_nota = nota['Número da Nota']
                                              lista.append(numero_nota)
                                              status = nota['status']
  
                                
                                              
except:
    pass  
if  status == 'Entrega não completa':
                                       
                                                            st.markdown(f'<div class="my-square">Total Nota: {len(lista_conferida)}</div>', unsafe_allow_html=True)
  
  
                
else:
  
                                                            st.markdown(f'<div class="my-square">Total Notas:{len(lista)}</div>', unsafe_allow_html=True)

                                             
