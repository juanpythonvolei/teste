import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
st.set_page_config(initial_sidebar_state="collapsed")
st.set_page_config(page_title="Roterização e suporte")

st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #FFA421;
        color: white; /* Cor do texto na barra lateral */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    body {
        background-color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
    <style>
       [aria-expanded='true'] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')

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
if not firebase_admin._apps:
    autenticacao  = {
    "type": "service_account",
    "project_id": "bancodedadosroteirooficial",
    "private_key_id": "3098a065f32317d6f39ddd93f4daf13ceb64befe",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCcOMX1xZZjRqS2\n/xft77sp2pMSKPZcD9TLDDrhCr3Bfhobij9hT123bIspec2Iv/d33yzAbPd+HGOb\nw550wwx0CpOAJMdjDqwi97gxLcmEA1BiGYCz6aXB4QrhelHyqd1OhV1zU7kcT+73\nlAPvXkDYXx46qCjEOabXsKs2pGKULlVqzeTO6HazyEK4FEXq6EhkLxwZOLDXGw1c\nRh5Wpsi5QniucWwvQfw1aXhkR/CZX8V9K/gyuoM++f9Kj4lOIBT8gbRcNeNbgj6Y\npz7w/8qlMbubjwYrgfZ0jcaPLicZVLsWxQ0qQbA+unBb5QCOBh9yZ5vz1eY2eAu3\nXaAeb49jAgMBAAECggEAN8I9yfihskJzJQvMnzTbQVeN+cPcFsThxy1Q0KT0UJ0x\nNVY1RAa/ZOodi4q5dQ9LhSIHh5D9DyqT1PNP2c4KYlqqBelarzz77KktOYRlsjQ6\nmyEOImkJLDemGg9+M1Y0ssOANNsTrYrMONrAQs4J6BCfKgF+N3d6WO7qVWD7/HYz\nzaZN72C2SSPk5treapAtxeuRocihkMv5QbsBArXXdvgOUqOqaLUtFaRlQMVD/jAx\ndWIkU+nY8mVlJ3vwkRZHK/pR/wzNGZh7qw9kgYF5SShskuMZswg5zE9oi09A3dKs\n37rrpC5OKMLYT/Fxe5N5/wBGMvPxJ9OHPNKn0emWLQKBgQDbmFEnqFG6D7FayvF+\njs6cCdv2VA12KNF6JaSpI+Bwmpgx27Q8IwlW8yMaMlLEL5Hxd5WE9hQVsiaVj7Be\nMAuuPONGWVcYBGYsiDtdaLdHCmaWICcJetIoHmUgd2pq6D5MwyAHuBRPl5zQBZpR\ndtEpkRdNlF537BnjuSgEAc36zQKBgQC2HuBQMb1CLBAkW274C6jmrbcnknY1j0sL\n5Gu/LEaMKUlFH+2e15nTjJSTcpJd6gdxKwEvo8kr8VgVNxIDrhLSlBEUtVmCZg72\nSZT/VwCCZNYrjBPkLIEQvshWIIWp2Tjahu5ezy/JeaBXp2KTaaZKspAUukTAtTra\n7QtwwYAS7wKBgQCsjs2+9xJ5vhkk+nK4e6m5jjnOIJCPeFXbwTbaProAYksUasv/\nsZyGOfsse7z0M1lgwRK6b9Cql9qgDlCOQvz6xxflURESa2qKtebIaSAUcATbFZr3\nZQ89vVzEHXJ/Xc6O7Yn+5tT3EnGEOdLhDxgfrMb+DIgLfnl9rCLYuz5MRQKBgQCz\n0ozd4h7jZaqSm41YcfrVupTsB9ucSt5o4aPZ4ZfO8T0deccgXfXPQjG53RjUji3G\n+hVzup76OpUkbXnmFE0Vi4nKDr5Q2QDRAhqSfI9OMM6ftPI3DBJsPFSHZhlUed1/\nOFfJWX3vy54crnPQ5jKB8wn8zWbxeICihggTz5vsFQKBgBtwJU6Dbr/EDk41J3kh\nfX2/vRT/wON69ph+cyf8R9ErA3YV888B7HbPrZ+XCmeIUY9qGn7pp9AnYr3BsOjK\nDVyf4ulO87wplBbwkZ/fcMMKNaOwynF3BN1ZBcBO43aOgQeGd9M8w/zyIfbOne4r\nc70tJyG6+OAcQx9a5NdFt3X9\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-obeze@bancodedadosroteirooficial.iam.gserviceaccount.com",
    "client_id": "103934498625514898395",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-obeze%40bancodedadosroteirooficial.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }

    cred = credentials.Certificate(autenticacao)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://bancodedadosroteirooficial-default-rtdb.firebaseio.com'  # Substitua pelo URL do seu Realtime Database
    })
else:
    pass

# Crie uma instância do cliente Realtime Database
# Define o estilo CSS para centralizar a imagem


# Configuração para ocultar a sidebar


key = 'AIzaSyDKr5U-JLK2SvlndWbdNULNCCJNRYVv4rg'
# Exibe a imagem centralizada

login = st.text_input(label='Digite seu E-mail')

senha = st.text_input(label='Digite sua senha',type="password")
if st.button('Entrar'):
    data = {"email":login,"password":senha,"returnSecureToken":True}
    requisicao = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={key}",data=data)
    requisicao_dic = requisicao.json()
    if requisicao.ok:
        st.switch_page('pages/Home.py')
    else:
        mensagem_erro  = requisicao_dic['error']['message']
        st.write(mensagem_erro)
elif st.button('Criar conta'):
    data = {"email":login,"password":senha,"returnSecureToken":True}
    requisicao = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={key}",data=data)
    requisicao_dic = requisicao.json()
    if requisicao.ok:
            refresh_token = requisicao_dic['refreshToken']
            local_id = requisicao_dic['localId']
            id_token = requisicao_dic['idToken']
            link = f'https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/{local_id}.json'
            data =f'{{"Nome":"{login}","Senha":"{senha}"}}'
            requisicao_usuario = requests.patch(link,data=data)
            st.switch_page('pages/Home.py')

    else:
            mensagem_erro  = requisicao_dic['error']['message']
            st.write(mensagem_erro)
