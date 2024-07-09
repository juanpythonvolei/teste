import streamlit as st
import requests
import re
from pathlib import Path 
from datetime import datetime
import xmltodict
import shutil
import datetime
import requests
import firebase_admin
from firebase_admin import credentials, firestore,db
from time import sleep
import pprint
from st_circular_progress import CircularProgress
import webbrowser
from suporte_inteligente import ia
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
selected_page = st.sidebar.selectbox("Escolha uma página", ["Rotas e suporte", "Login", "Home"])
seletor  = st.radio("Opções", ["rota da nota", "rota de todas as notas", "suporte inteligente"])


if selected_page == 'Login':
    st.switch_page('meu_app.py')
elif selected_page == 'Home':
    st.switch_page('pages/home.py')

if seletor == 'rota da nota':
    pesquisa_nota = st.text_input(label='Pesquisar rota dessa nota')
    pesquisa = st.button('ver rotas')
    if pesquisa:
        lista = []
        destinos_info = []
        requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
        roteiro = requiscao.json()
        dados = roteiro['bancodedadosroteirooficial']
        for item in dados:
                roteiro = dados[f'{item}']
                for elemento in roteiro:
                    nota = roteiro[f'{elemento}']
                    if nota['Número da Nota'] == str(pesquisa_nota):
                        numero = nota['Número da Nota']
                        volumes = nota['Volumes']
                        valor = nota['Valor Total']
                        Cliente  = nota['Cliente']
                        base_url2 = "https://www.google.com/maps/dir/"
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
                        ponto_partida = (lat_inicial, lon_inicial)
                        ponto_partida_dict = {
                            'destino': 'Itupeva, SP',
                            'distancia': 0,
                            'Número da nota': '',
                            'volumes': '',
                            'Duração': '',
                            'coordenadas': ponto_partida,
                            'coordenadas_google': f'{lat_inicial},{lon_inicial}',
                            'cliente': ''
                        }
                        destinos_info.append(ponto_partida_dict)
                        destino = nota['Destino']
                        
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
        destinos_info.append(localizacao)
        final = base_url2 + '/'.join(destinos_info)
        webbrowser.open(final)     
        st.warning(f'Nota: {numero} volumes: {volumes} valor:{valor} cliente:{Cliente}')
elif seletor == "rota de todas as notas":
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
        total = st.button("Pesquisar todas as rotas")
        if total:
            st.write(f'Total de Roteiros disponíveis: {len(lista_total)}')
            for item in dados:
                if item == opcao_selecionada:
                    roteiro = dados[f'{item}']
                    for elemento in roteiro:
                            nota = roteiro[f'{elemento}']
                            volumes = nota['Volumes']
                            valor = nota['Valor Total']
                            Cliente  = nota['Cliente']
                            
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
                            ponto_partida = (lat_inicial, lon_inicial)
                            ponto_partida_dict = {
                                    'destino': 'Itupeva, SP',
                                    'distancia': 0,
                                    'Número da nota': '',
                                    'volumes': '',
                                    'Duração': '',
                                    'coordenadas': ponto_partida,
                                    'coordenadas_google': f'{lat_inicial},{lon_inicial}',
                                    'cliente': ''
                                }
                            destinos_info.append(ponto_partida_dict['coordenadas_google'])
                            destino = nota['Destino']
                                
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
                                            lat_inicial = location["lat"]
                                            lon_inicial = location["lng"]
                                            localizacao = f'{lat_inicial},{lon_inicial}'
                                            destinos_info.append(localizacao)
                final = base_url2 + '/'.join(destinos_info)
                webbrowser.open(final) 
elif seletor == "suporte inteligente":
       texto_ia = st.text_input(label='Digite sua pergunta')
       botao_ia = st.button('ok')
       if botao_ia:
              ia(pergunta=texto_ia)

        
              
              

            
      

    

    
