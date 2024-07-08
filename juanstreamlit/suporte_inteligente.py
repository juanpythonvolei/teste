import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import openpyxl
import pandas as pd
from tkinter.filedialog import askopenfilename
import tkinter as tk
from tkinter import ttk
import PyPDF2
import requests
import streamlit as st
import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()

def ia(pergunta):
    
    GOOGLE_API_KEY = 'AIzaSyB2uaEtcP8T2_Fy6bhmXC3828qysZEqjNQ'
    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-1.5-flash')

    chat = model.start_chat(history=[])
    requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
    roteiro = requiscao.json()
    dados = roteiro['bancodedadosroteirooficial']
    texto_nota = ''
    for item in dados:
        roteiro = dados[f'{item}']
        for elemento in roteiro:
            nota = roteiro[f'{elemento}']
            for item in nota:
                numero_nota = nota['Número da Nota']
                destino = nota['Destino']
                data_De_emissao = nota['Data de Emissão']
                volumes = nota['Volumes']
                cliente = nota['Cliente']
                Produtos = nota['Produtos'][0]
                status = nota['status']
                valor  = nota['Valor Total']
            infos = f'Numero nota:{numero_nota}. volumes:{volumes}. cliente:{cliente}. Produtos:{Produtos}. status:{status}. valor:{valor}. destino:{destino}. data de emissão:{data_De_emissao}\n'
            if str(infos) in str(texto_nota):
                pass
            else:
                texto_nota += str(infos)
    response = chat.send_message(f'{pergunta}:\n\n{texto_nota}\n')
    resposta = response.text
    st.write(f'{resposta}')
