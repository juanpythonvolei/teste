import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import math
from geopy.distance import geodesic



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
selected = option_menu("Menu Principal", ["Dados Gerais", "Dados do Tranporte"], icons=["database", "truck"], default_index=1)
# Adicionando botões em cada coluna
if selected == "Dados Gerais":
    texto_nota = []
    lista_produtos = []
    lista_clientes = []
    Lista_valores = []
    lista_notas = []
    lista_volumes = []
    
    for item in dados:
            roteiro = dados[f'{item}']
            for elemento in roteiro:
                nota = roteiro[f'{elemento}']
                if nota['Data de Emissão'] == opcao_selecionada:
                    for item in nota:
                        numero_nota = nota['Número da Nota']
                        destino = nota['Destino']
                        data_De_emissao = nota['Data de Emissão']
                        volumes = nota['Volumes']
                        cliente = nota['Cliente']
                        Produtos = nota['Produtos'][0]
                        status = nota['status']
                        valor  = nota['Valor Total']
                    texto_nota.append(destino)
                    lista_produtos.append(Produtos)
                    lista_clientes.append(cliente)
                    Lista_valores.append(valor)
                    lista_notas.append(numero_nota)
                    lista_volumes.append(volumes)
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
elif selected == 'Dados do Tranporte':
    valor_total = 0
    ditancia_total = 0
    lista_duracao = []
    lista_viagem = []
    valor = []
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
    lista_total = []
    destinos_info = []
    requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
    roteiro = requiscao.json()
    dados = roteiro['bancodedadosroteirooficial']
    base_url2 = "https://www.google.com/maps/dir/"
    for item in dados:
                    roteiro = dados[f'{item}']
                    for elemento in roteiro:
                        nota = roteiro[f'{elemento}']
                        if nota['Data de Emissão'] == opcao_selecionada:
                            destino = nota['Destino']
                            valor  = nota['Valor Total']
                            valor_total += float(valor)
                            if destino in lista_total:
                                pass
                            else:
                                lista_total.append(destino)
                                
                            address = f"{destino}"
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
        distance_matrix_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={lat_incial},{lon_inicial}&destinations={lat_final},{lon_final}&key=AIzaSyCMVv5_0c2dR16BM9r6ppgJ5sHXPD4MEc0"
        
        # Faz a requisição
        response = requests.get(distance_matrix_url)
        data = response.json()
        
        if data["status"] == "OK":
            distance = data["rows"][0]["elements"][0]["distance"]["text"]
            lista_viagem.append(distance)
            duration = data["rows"][0]["elements"][0]["duration"]["text"]
            lista_duracao.append(duration)
            
            # Agora você pode usar 'distance' e 'duration' conforme necessário
    
            # Atualiza a origem para o próximo destino
        origem_atual = (lat_final, lon_final)

            
    data = {'Destino': lista_total,
            'Distância':lista_viagem,
            'Duração':lista_duracao}
    df = pd.DataFrame(data)

    # Exibindo a tabela no Streamlit
    st.table(df)




# Estilização CSS embutida
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
with col1:
    st.markdown(f'<div class="my-square">Valor Total:{valor_total}</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="my-square">Total Destinos:{len(destinos_info)}</div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="my-square">Km:{ditancia_total}</div>', unsafe_allow_html=True)
    
    

    
