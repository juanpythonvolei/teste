import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import math
from geopy.distance import geodesic
from firebase_admin import credentials, firestore,db
seletor  = option_menu("Menu Principal", ["Cadastrar Veículos", "Pesquisar Veículos"], icons=["truck", "search"], default_index=1)
ref = db.reference('bancodedadosroteirooficial')
if seletor == 'Cadastrar Veículos':
    Veículo = st.text_input(label='Digite o nome do Veículo')
    Placa = st.text_input(label='Digite a placa do veículo')
    km = st.text_input(label='Digite a relação km/L do veículo')
    foto = st.text_input(label='Insira a url da foto do Veículo')
    botao = st.button('Cadastrar Veículo')
    dict_veiculo = {'nome':Veículo,
                    'Placa':Placa,
                    'Km':km,
                   'Foto':foto}
    if botao:
        ref.child(Veículo).push().set(dict_veiculo)
