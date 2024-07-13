import streamlit as st
import requests

# Carrega os dados do banco de dados
requisicao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requisicao.json()
dados = roteiro['bancodedadosroteirooficial']

# Cria um dicionário para armazenar o estado das checkboxes
checkbox_states = {}

# Exibe a seleção da data
lista_total = [item for item in dados]
opcao_selecionada_data = st.selectbox("Selecione uma data", lista_total)


for item in dados:
            lista_conferida = []
            lista_notas = []
            roteiro = dados[item]
            for elemento in roteiro:
                        nota = roteiro[elemento]
                        data = nota['Data de Emissão']
                        if data == opcao_selecionada_data:
                                    volumes = nota['Volumes']
                                    numero_nota = nota['Número da Nota']
                                    lista_notas.append(numero_nota)
                                    valor = nota['Valor Total']
                                    cliente = nota['Cliente']
                                    
                                    
                                        # Usa o dicionário para controlar o estado da checkbox
                                    checkbox_states[numero_nota] = st.checkbox(f"Cliente: {cliente}. Nota: {numero_nota}. Volumes: {volumes}", key=numero_nota)
    
    # Agora você pode usar o dicionário 'checkbox_states' conforme necessário
st.write("Notas selecionadas:")
for nota, estado in checkbox_states.items():
        if estado:
            status = 'Feito'
            lista_conferida.append(status)
            st.write(len(lista_conferida))  
            st.write(len(lista_notas))   
            if len(lista_conferida) == len(lista_notas):
                        requisicao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                        roteiro = requisicao.json()
                        dados = roteiro['bancodedadosroteirooficial']
                        for elemento in roteiro:
                            nota = roteiro[elemento]        
                            status = nota['status']
                            link = f'https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/bancodedadosroteirooficial/{opcao_selecionada}/{elemento}/status.json'
                            data = '{"status": "Entrega realizada"}'
                            requests.patch(link, data=data)
                                 
                        st.warning('Entrega realizada com Sucesso')
            else:
                        pass
        else:
            try:
                        status = 'Feito'
                        lista_conferida.remove(status)
            except:
                        pass
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
          st.markdown(f'<div class="my-square">Total Notas:{len(lista_conferida)}</div>', unsafe_allow_html=True)
with col2:
          st.markdown(f'<div class="my-square">Total Destinos</div>', unsafe_allow_html=True)
with col3:
          st.markdown(f'<div class="my-square">Total valor</div>', unsafe_allow_html=True)

# Exibe as notas com checkboxes
