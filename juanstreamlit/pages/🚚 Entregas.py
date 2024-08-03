import streamlit as st
import requests
requisicao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requisicao.json()

     
dados = roteiro['bancodedadosroteirooficial']
  
    # Exibe a seleção da data
lista_total = [item for item in dados]
lista_nomes = []
dados2 = roteiro['Veículos']
for item in dados2:                       
                            veiculo = dados2[f'{item}']
                            for elemento in veiculo:
                                   espec = veiculo[f'{elemento}']
                                   nome = espec['nome']
                                   lista_nomes.append(nome)
  # Carrega os dados do banco de dados
opcao_selecionada_data = st.selectbox("Selecione uma data", lista_total)
Veículo = st.selectbox('Selecione o Veículo da entrega',lista_nomes)
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
                                        try:
                                          roteiro = dados[f'{item}']
                                          for elemento in roteiro:
                                              nota = roteiro[f'{elemento}'] 
                                              data = nota['Data de Emissão']
                                              Endereco = nota['Destino']
                                              lista_destinos.append(Endereco)
                                              if data == opcao_selecionada_data:
                                                status = nota['status']
                                                link = f'https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/bancodedadosroteirooficial/{opcao_selecionada_data}/{elemento}/status.json'
                                                dados = '{"status": "Entrega realizada"}'
                                                requests.patch(link, data=dados)
                                        except:
                                          pass
                                                 
                            st.warning('Entrega realizada com Sucesso')
                            destinos_info = []
                            distancia_total = 0 
                            lista_destinos = []
                            address = "Itupeva,sp"
                            base_url = "https://maps.googleapis.com/maps/api/geocode/json"
                            params = {
                                                                        "address": address,
                                                                        "key": 'AIzaSyCMVv5_0c2dR16BM9r6ppgJ5sHXPD4MEc0'  # Substitua pela sua chave de API
                                                                    }
                            
                            response = requests.get(base_url, params=params)
                            data = response.json()
                            if data["status"] == "OK":
                                                                        location = data["results"][0]["geometry"]["location"]
                                                                        lat_inicial = location["lat"]
                                                                        lon_inicial = location["lng"]
                                                                        origem_atual = (lat_inicial, lon_inicial) 
                            for item in lista_destinos:
                              address = f"{item}"
                              base_url = "https://maps.googleapis.com/maps/api/geocode/json"
                              params = {
                                                          "address": address,
                                                          "key": 'AIzaSyCMVv5_0c2dR16BM9r6ppgJ5sHXPD4MEc0'  # Substitua pela sua chave de API
                                                      }
                      
                              response = requests.get(base_url, params=params)
                              data = response.json()
                              if data["status"] == "OK":
                                                          location = data["results"][0]["geometry"]["location"]
                                                          lat_final = location["lat"]
                                                          lon_final = location["lng"]
                                                          localizacao = f'{lat_final},{lon_final}'
                                                          if localizacao in destinos_info:
                                                              pass
                                                          else:
                                                              destinos_info.append(localizacao)
                            for i in range(len(destinos_info)): 
                              destino_info = destinos_info[i]
                              lat_final, lon_final = map(float, destino_info.split(','))  # Obtém as coordenadas do destino
                              
                              # Constrói a URL da matriz de distância
                              distance_matrix_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origem_atual[0]},{origem_atual[1]}&destinations={lat_final},{lon_final}&key=AIzaSyCMVv5_0c2dR16BM9r6ppgJ5sHXPD4MEc0"
                              
                              # Faz a requisição
                              response = requests.get(distance_matrix_url)
                              data = response.json()
                              
                              if data["status"] == "OK":
                                  distance_text = data["rows"][0]["elements"][0]["distance"]["text"]
                                  distance_value = float(distance_text.split()[0]) 
                                  distancia_total += distance_value 
                                  duration = data["rows"][0]["elements"][0]["duration"]["text"]
                                  
                                  
                                  # Agora você pode usar 'distance' e 'duration' conforme necessário
                          
                                  # Atualiza a origem para o próximo destino
                              origem_atual = (lat_final, lon_final)
                              for item in dados2:
                                if item == Veículo:
                                  veiculo = dados2[f'{item}']
                                  for elemento in veiculo:
                                         espec = veiculo[f'{elemento}']
                                         nome = espec['nome']
                                         
                                         dados2 = {f'Viagem dia': opcao_selecionada_data,'Distância':distancia_total}
                                         link2 = f'https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/bancodedadosroteirooficial/Veículos/{item}/{dados2}.json'   
                                         response = requests.post(link2, json=dados2)       
                                            
                                  
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

                                             
                                              
                                              
    # Exibe as notas com checkboxes
