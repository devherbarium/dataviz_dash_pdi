import streamlit as st
import SOBRE
import PUBMED
import IHERB
import NUTRACEUTICAL
from PIL import Image
from streamlit_option_menu import option_menu
from aux2 import *
import streamlit_authenticator as stauth
import os


storage_account_key = os.getenv("storage_key")
container_name = "pdi-dashboard"
# storage_account_key = read_storage_key('storage_key.txt')
# Defina suas credenciais e o nome do contêiner
storage_account_name = "hlbdatalake"
# Conectar ao BlobServiceClient usando a connection string
connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
# Criar o ContainerClient
container_client = blob_service_client.get_container_client(container_name)

config = read_yaml_from_blob(
    container_name="pdi-dashboard",
    blob_name="config.yaml",
    storage_account_key=storage_account_key
)

if config:
    print("Arquivo YAML lido com sucesso:")
else:
    print("Falha ao ler o arquivo YAML.")

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()

    img_path,base_path = img_base_pth()

    # st.sidebar.image(Image.open(img_path+'\Herbarium.png'), width = 250)
    st.sidebar.image(open_img_from_blob(storage_account_key, "\Imagens\Herbarium.png"))

    st.sidebar.markdown('## <span style="color:#2F4F4F"> Observatório de Inovação </span>', unsafe_allow_html=True)
    st.sidebar.markdown(''' --- ''')

    st.sidebar.markdown('<h3 style = "text-align: left"> Selecione a opção que deseja exibir: </h3>', unsafe_allow_html = True)


    with st.sidebar:
        choose = option_menu(menu_title = None,
                             options = ['Página Inicial',
                                        'PUBMED',
                                        'IHerb',
                                        'Nutraceutical'
                                        ],
                             icons = ['house','bar-chart', 'bar-chart-line', 'bar-chart-line','bar-chart-line', 'bar-chart-line', 'whatsapp'],
                             menu_icon = 'graph-up',
                             orientation = 'vertical',
                             default_index = 0,
                             styles = {'container': {'padding': '5!important', 'background-color': '#66CDAA'}, #cor do fundo
                                                     'icon': {'color': 'black', 'font-size': '25px'},
                                                     'nav-link': {'font-size': '18px', 'text-align': 'left', 'margin': '0px', '--hover-color': '#5F9EA0'}, # cor da movimentação
                                                     'nav-link-selected': {'font-size': '18px', 'background-color': '#2F4F4F'}}) # cor da seleção

    if choose == 'Página Inicial':
        SOBRE.Sobre()

    if choose == 'PUBMED':
        PUBMED.Pubmed()

    if choose == 'IHerb':
        IHERB.IHerb()

    if choose == 'Nutraceutical':
        NUTRACEUTICAL.Nutraceutical()


elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


