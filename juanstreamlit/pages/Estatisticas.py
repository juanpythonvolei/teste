import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import math




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
                                                            distance_matrix_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={lat_inicial},{lon_inicial}&destinations={lat_final},{lon_final}&key=AIzaSyCMVv5_0c2dR16BM9r6ppgJ5sHXPD4MEc0"
                                                    
                                                            # Fazendo a requisição
                                                            response = requests.get(distance_matrix_url)
                                                            data = response.json()
                                                            
                                                            if data["status"] == "OK":
                                                                distance = data["rows"][0]["elements"][0]["distance"]["text"]
                                                                duration = data["rows"][0]["elements"][0]["duration"]["text"]
                                                               
    def euclidean_distance(x1, y1, x2, y2):
        return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5

# Calcular a distância entre o local de origem e cada destino
    for destino in destinos_info:
        lat_destino, lon_destino = map(float, destino.split(","))
        dist = euclidean_distance(lat_inicial, lon_inicial, lat_destino, lon_destino)
        lista_viagem.append(dist)
    distance_matrix_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={lat_inicial},{lon_inicial}&destinations={'|'.join(destinos_info)}&key=AIzaSyCMVv5_0c2dR16BM9r6ppgJ5sHXPD4MEc0"

    # Fazendo a requisição
    response = requests.get(distance_matrix_url)
    data = response.json()
    
    if data["status"] == "OK":
        for i, destination in enumerate(data["destination_addresses"]):
            duration = data["rows"][0]["elements"][i]["duration"]["text"]
            lista_duracao.append(duration)
            
    data = {'Destino': lista_total,
            'Distância':lista_viagem,
            'Duração':lista_duracao}
    df = pd.DataFrame(data)

    # Exibindo a tabela no Streamlit
    st.table(df)


st.markdown('<div class="my-square">Quadrado Estilizado</div>', unsafe_allow_html=True)                                    
        
    
    

    
