import streamlit as st
import requests
st.markdown("""
    <style>
       [aria-expanded='true'] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
login = st.text_input(label='Digite seu E-Mail')

senha = st.text_input(label='Digite sua senha',type="password")

botao = st.button('Criar Conta')
botao_voltar = st.button('Voltar')

key = 'AIzaSyDKr5U-JLK2SvlndWbdNULNCCJNRYVv4rg'
if botao:
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
                st.switch_page('pages/home.py')

    else:
                mensagem_erro  = requisicao_dic['error']['message']
                st.write(mensagem_erro)
elif botao_voltar:
        st.switch_page("Login.py")
