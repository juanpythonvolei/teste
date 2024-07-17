import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import math
from geopy.distance import geodesic
from firebase_admin import credentials, firestore,db
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
                   'Foto':foto}
    if botao:
        ref.child(Veículo).push().set(dict_veiculo)
elif seletor == 'Pesquisar Veículos':
        lista_nomes = []
        requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
        roteiro = requiscao.json()
        dados = roteiro['Veículos']
        for item in dados:
                            veiculo = dados[f'{item}']
                            for elemento in veiculo:
                                   espec = veiculo[f'{elemento}']
                                   nome = espec['nome']
                                   lista_nomes.append(nome)
        opcao = st.select_slider('Selecione um Veículo',lista_nomes)
