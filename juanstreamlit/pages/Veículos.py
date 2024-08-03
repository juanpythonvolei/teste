import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import math
from geopy.distance import geodesic
from firebase_admin import credentials, firestore,db
from streamlit_calendar import calendar
import datetime

calendar_options = {
    "editable": "true",
    "selectable": "true",
    # ... outras opções ...
}

# Exemplo de eventos no calendário
calendar_events = [
    {"title": "Evento 1", "start": "2023-07-31T08:30:00", "end": "2023-07-31T10:30:00"},
    # ... outros eventos ...
]

# Crie o calendário


# Exiba o calendário no Streamlit
selected_date = st.date_input("Selecione uma data", datetime.date.today())
seletor  = option_menu("Menu Principal", ["Cadastrar Veículos", "Pesquisar Veículos"], icons=["truck", "search"], default_index=1)
ref = db.reference('Veículos')
if seletor == 'Cadastrar Veículos':
    lista_km = []
    km = 0
    for i in range(30):
        km += 1
        lista_km.append(km)
if seletor == 'Cadastrar Veículos':
    Veículo = st.text_input(label='Digite o nome do Veículo')
    Placa = st.text_input(label='Digite a placa do veículo')
    km = st.selectbox("Selecione a relação km/L do veículo", lista_km)
    foto = st.text_input(label='Insira a url da foto do Veículo')
    botao = st.button('Cadastrar Veículo')
    dict_veiculo = {'nome':Veículo,
                    'Placa':Placa,
                    'Km':km,
                   'Foto':foto,
                   'Distância':'Nenhuma'}
    if botao:
        ref.child(Veículo).push().set(dict_veiculo)
elif seletor == 'Pesquisar Veículos':
        lista_nomes = []
        lista_veiculos = []
        lista_locais = []
        destinos_info = []
        requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
        roteiro = requiscao.json()
        dados = roteiro['Veículos']
        
        for item in dados:
                            veiculo = dados[f'{item}']
                            for elemento in veiculo:
                                   espec = veiculo[f'{elemento}']
                                   nome = espec['nome']
                                   lista_nomes.append(nome)
        opcao = st.selectbox('Selecione um Veículo',lista_nomes)
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
        requiscao2 = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
        roteiro2 = requiscao2.json()        
        dados2 = roteiro2['bancodedadosroteirooficial']    
        for item in dados2:
                              
                              roteiro = dados2[f'{item}']
                              for elemento in roteiro:
                                          nota = roteiro[f'{elemento}']
                                          y  = nota['Veículo']
                                          for x in y:
                                              veiculo = y[f'{x}']
                                              if veiculo == opcao:
                                                  lista_veiculos.append(veiculo)
                                              

        for item in dados:
                            veiculo = dados[f'{item}']
                            for elemento in veiculo: 
                                   espec = veiculo[f'{elemento}']
                                   nome = espec['nome']
                                   if nome == opcao: 
                                       link = espec['Foto']
                                       st.image(link) 
                                       placa = espec['Placa']
                                       kilometragem = espec['Km']
                                       dict = {'Nome':nome,'Placa':placa,'Kilometragem':kilometragem}
                                       st.table(dict)
