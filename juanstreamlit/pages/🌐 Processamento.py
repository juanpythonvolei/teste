import streamlit as st
import requests
import re
from pathlib import Path
import os
from datetime import datetime
import xmltodict
import shutil
import datetime
# URL da API Directions
import firebase_admin
from firebase_admin import credentials, firestore,db
from time import sleep
import pprint
from st_circular_progress import CircularProgress
from streamlit_option_menu import option_menu
from pprint import pprint
import datetime
datas = []
ref = db.reference('bancodedadosroteirooficial')
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #FFA421;
        color: white; /* Cor do texto na barra lateral */
    }
    </style>
""", unsafe_allow_html=True)
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
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
selected = option_menu("Menu Principal", ["Processar Notas", "Excluir Conjuntos de Notas"], default_index=1)
if selected == 'Processar Notas':
    start_date = datetime.date(2000, 1, 1)
    end_date = datetime.date(2100, 1, 11)
    lista_filtrada = []
    current_date = start_date
    while current_date <= end_date:
        current_date += datetime.timedelta(days=1)
        datas.append(current_date)
    opcao_selecionada = selected_date = st.date_input("Selecione uma data", datetime.date.today())
    
    uploaded_files = st.file_uploader("Escolha as Notas", type=['xml'], accept_multiple_files=True)
    if uploaded_files:
        uso = []
        lista_notas = []
        quantidade_notas = []
        lista_datas = []
        lista_Destinos = []
        massa = 0
        destinos_info = []
        for nota in uploaded_files:
            try:
                    xml_data = nota.read()
                    documento = xmltodict.parse(xml_data)
                    if str(documento['nfeProc']['NFe']['infNFe']['ide']['dhEmi'][:10]) == str(opcao_selecionada):
                        nome = nota.name
                        if documento not in lista_filtrada:
                               lista_filtrada.append(documento)
                        else:
                            continue
            except:
                    st.warning('Algo deu errado, tente novamente')
        st.warning(f"Você carregou um total de: {len(lista_filtrada)} notas")
        for documento in lista_filtrada:
                            try:
                                                
                                                    lista_datas.append(nota)
                                                    dict_nota_fiscal = documento['nfeProc']['NFe']['infNFe']
                                                    numero_da_nota = dict_nota_fiscal['ide']['nNF']
                                                    cliente = dict_nota_fiscal['dest']['xNome']
                                                    valor_total = dict_nota_fiscal['total']['ICMSTot']['vNF']
                                                    destino = f'{dict_nota_fiscal["dest"]["enderDest"]["xLgr"]},{dict_nota_fiscal["dest"]["enderDest"]["nro"]}-{dict_nota_fiscal["dest"]["enderDest"]["xBairro"]},{dict_nota_fiscal["dest"]["enderDest"]["xMun"]}-{dict_nota_fiscal["dest"]["enderDest"]["UF"]},{dict_nota_fiscal["dest"]["enderDest"]["CEP"]}'
                                                    data_emit = documento['nfeProc']['NFe']['infNFe']['ide']['dhEmi'][:10]
                                                    lista_produtos = []
                                                    lista_Destinos.append(destino)
                                                    descricao_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['cProd']
                                                    valor_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['vProd']
                                                    try:
                                                        peso =  documento['nfeProc']['NFe']['infNFe']['transp']['vol']['pesoL']
                                                        item_nota = f'Item: {descricao_produto}  valor: {valor_produto}'
                                                        massa += float(peso)
                                                    except:
                                                            peso = 'Desconsiderável'
                                                            massa = 'Desconsiderável'
                                                    lista_produtos.append(item_nota)
        
                                                        
        
                                                    dict_nota = {
                                                        'Produtos': lista_produtos,
                                                        'Número da Nota': numero_da_nota,
                                                        'Cliente': cliente,
                                                        'Valor Total': valor_total,
                                                        'Destino': destino,
                                                        'Volumes':len(lista_produtos),
                                                        'Data de Emissão':data_emit,
                                                        'Massa': peso,
                                                        'status':'Entrega não completa',
                                                        'Veículo':'Indefinido'
                                                    }
                                                    lista_notas.append(dict_nota)
                            except:
                                                lista_produtos = []
                                                if isinstance(documento['nfeProc']['NFe']['infNFe']['det'], list):
                                                    # Iterar sobre os elementos 'det'
                                                    for item in documento['nfeProc']['NFe']['infNFe']['det']:
                                                        descricao_produto = item['prod']['cProd']
                                                        valor_prod = item['prod']['vProd']
                                                        elemento = f'Item:{descricao_produto}  valor:{valor_prod}'
                                                        lista_produtos.append(elemento)
                                                else:
                        # Acessar diretamente o campo 'cProd'
                                                    descricao_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['cProd']
                                                    valor_prod = documento['nfeProc']['NFe']['infNFe']['det']['prod']['vProd']
                                                    elemento = f'Item:{descricao_produto}  Valor:{valor_prod}'
                                                    lista_produtos.append(elemento)
                                                lista_datas.append(nota)
                                                dict_nota_fiscal = documento['nfeProc']['NFe']['infNFe']
                                                numero_da_nota = dict_nota_fiscal['ide']['nNF']
                                                cliente = dict_nota_fiscal['dest']['xNome']
                                                valor_total = dict_nota_fiscal['total']['ICMSTot']['vNF']
                                                destino = f'{dict_nota_fiscal["dest"]["enderDest"]["xLgr"]},{dict_nota_fiscal["dest"]["enderDest"]["nro"]}-{dict_nota_fiscal["dest"]["enderDest"]["xBairro"]},{dict_nota_fiscal["dest"]["enderDest"]["xMun"]}-{dict_nota_fiscal["dest"]["enderDest"]["UF"]},{dict_nota_fiscal["dest"]["enderDest"]["CEP"]}'
                                                data_emit = documento['nfeProc']['NFe']['infNFe']['ide']['dhEmi'][:10]
                                                try:
                                                    peso =  dict_nota_fiscal['transp']['vol']['pesoL']
                                                    massa += float(peso)
                                                except:
                                                    peso = 'Desconsiderável'
                                                    massa = 'Desconsiderável'
                                                lista_Destinos.append(destino)
        
                                                        
        
                                                dict_nota = {
                                                        'Produtos': lista_produtos,
                                                        'Número da Nota': numero_da_nota,
                                                        'Cliente': cliente,
                                                        'Valor Total': valor_total,
                                                        'Destino': destino,
                                                        'Volumes':len(lista_produtos),
                                                        'Data de Emissão':data_emit,
                                                        'Massa': peso,
                                                        'status':'Entrega não completa',
                                                        'Veículo':'Indefinido'
                                                    }
                                                lista_notas.append(dict_nota)
     
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
        base_url2 = "https://www.google.com/maps/dir/"
        for item in lista_Destinos:
                                    valor = item
                                    address2 = f"{valor}"
                                    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
                                    params = {
                                        "address": address2,
                                        "key": 'AIzaSyCMVv5_0c2dR16BM9r6ppgJ5sHXPD4MEc0'  # Substitua pela sua chave de API
                                    }
    
                                    response = requests.get(base_url, params=params)
                                    data = response.json()
                                    if data["status"] == "OK":
                                        location = data["results"][0]["geometry"]["location"]
                                        lat_final2 = location["lat"]
                                        lon_final2 = location["lng"]
                                        if valor == 0:
                                            pass
                                        else:
                                            url = 'https://maps.googleapis.com/maps/api/directions/json'
                                            params = {
                                                        'origin': f'Rua Louveira, Jardim Samabaia,101.Itupeva,sp',  # Origem
                                                        'destination': f'{str(address2)}',  # Destino
                                                        'key': 'AIzaSyCMVv5_0c2dR16BM9r6ppgJ5sHXPD4MEc0'  # Sua chave de API do Google Maps
                                                    }
    
                                                    # Fazendo a requisição GET
                                            response = requests.get(url, params=params)
                                            if response.status_code == 200:
                                                        data = response.json()
                                                        route = data['routes'][0]  # Primeira rota disponível
                                                        distance = route['legs'][0]['distance']['text'][:4]
                                                        distancia = float(distance.replace(' km', '').replace(',', '.'))
                                                        duration = route['legs'][0]['duration']['text']
                                                        destinos_info.append({
                                                            'destino': valor,
                                                            'distancia': distancia,
                                                            'Duração': duration,
                                                            'coordenadas':(lat_final2,lon_final2),
                                                            'coordenadas_google': f'{lat_final2},{lon_final2}',
                                                            'cliente':cliente,
                                                        })
        st.warning('Conectando ao banco de dados')
        lista_pontos = []
        destinos_ordenados = sorted(destinos_info, key=lambda x: x['distancia'])
        for destino in destinos_ordenados:        # Criar o DataFrame com todos os dados das notas
                                    local=destino['coordenadas_google']
                                    if local in lista_pontos:
                                        pass
                                    else:
                                        lista_pontos.append(local)
        final = base_url2 + '/'.join(lista_pontos)
        dict_nota['link'] = f'{final}'                    
                                
        for elemento in lista_notas:
                                    data_emissao = elemento['Data de Emissão']
                                    ref.child(data_emissao).push().set(elemento)
        else:
                            print('não confere')
        st.warning('Processo Concluído')
        st.write(f'''Total de notas:{len(lista_notas)}''')
elif selected == 'Excluir Conjuntos de Notas':
        lista_total = []
        destinos_info = []
        requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
        roteiro = requiscao.json()
        try:
            dados = roteiro['bancodedadosroteirooficial']
            base_url2 = "https://www.google.com/maps/dir/"
        except:
                st.warning('Sem Roteiros Disponíveis')
        for item in dados:
                    roteiro = dados[f'{item}']
                    lista_total.append(item)
        data_excluir  = st.selectbox("Selecione uma data para exclusão", lista_total)
        excluir = st.button('Excluir Conjunto')
        if excluir:
            try:
    
                # Referência ao nó do usuário que você deseja excluir
                usuario_ref = db.reference(f'bancodedadosroteirooficial/{data_excluir}')
                
                # Exclui o usuário
                usuario_ref.delete()
                st.warning('Conjunto excluido')
            except:
                st.warning('Conjunto inexistente')
    
