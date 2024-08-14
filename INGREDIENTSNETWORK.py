import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.offline as py
import plotly.graph_objects as go

container_name = "pdi-dashboard"
storage_account_key = os.getenv("storage_key")
# storage_account_key = read_storage_key('storage_key.txt')
# Defina suas credenciais e o nome do contêiner
storage_account_name = "hlbdatalake"
# Conectar ao BlobServiceClient usando a connection string
connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"

def IngredientsNetWork():

    #######################################################################################################
    ######################################### Base de dados ###############################################
    #######################################################################################################
    # Estoque = pd.read_csv('Base_dados/Estoque.csv')
    Estoque = read_csv_from_blob(connection_string, container_name, "\Base_dados\Estoque.csv")
    Estoque.drop(["Unnamed: 0"], axis=1, inplace=True)
    
    
    st.markdown('## <span style="color:#3B3D94"><center> Informações individuais por produto </center></span>', unsafe_allow_html=True) # Título da página
    st.markdown(''' --- ''')

    #######################################################################################################
    ######################################### opção produto ###############################################
    #######################################################################################################

    col1, col2 = st.columns(2)
    with col1:
        lista_marca = Estoque.Marca.unique().tolist() # Criando uma lista com as marcas
        marca = st.selectbox('Selecione uma Marca:', lista_marca)
    with col2:
        lista_produtos = Estoque.groupby('Marca').get_group(marca).Descricao.unique().tolist()  # Criando uma lista com os produtos
        produto = st.selectbox('Selecione um Produto:', lista_produtos)


    #######################################################################################################
    ##################################### Definindo o dataframe de trabalho ###############################
    #######################################################################################################

    ano2022 = Estoque.groupby('Ano').get_group(2022).reset_index()
    ano2022.drop(columns=['index'],inplace = True)
    ano2022['Mes'] = ano2022['Mes'].replace(['Janeiro', 'Fevereiro','Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
                                        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ,12])
    #teste = ano2022[ano2022['Descricao'].str.contains(produto)].reset_index()
    teste = ano2022.loc[ano2022.Descricao == produto].reset_index()
    teste.drop(columns=['index'],inplace = True)

    
    info = st.checkbox('Visualizar Informações sobre o produto') # checkbox para visualizar a tabela com informações do produto 
    if info:
        st.write(teste)
    else:
        st.write("")
    
    #######################################################################################################
    ###################################### FPLOTANDO OS GRÁFICOS ##########################################
    #######################################################################################################

    trace_f1 = go.Scatter(x = teste['Mes'], y = teste['Ven_Lib'], mode = 'markers+lines', name = 'Venda Liberada')
    trace_f2 = go.Scatter(x = teste['Mes'], y = teste['Qtd_Estq'], mode = 'markers+lines', name = 'Quantidade Estoque')
    trace_f3 = go.Scatter(x = teste['Mes'], y = teste['Qtd_O_P'], mode = 'markers+lines', name = 'Quantidade Produzido')
    data = [trace_f1, trace_f2, trace_f3]
    layout = go.Layout(title_text = 'Informações do Produto', title_font_size = 25, title_x = 0.35,
                        xaxis = {'title': 'Mês'}, yaxis = {'title': 'Quantidade'},
                        paper_bgcolor = 'rgb(243, 243, 243)', plot_bgcolor = 'rgb(243, 243, 243)')
    fig = go.Figure(data = data, layout = layout)
    fig.update_xaxes(tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                ticktext = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
    st.plotly_chart(fig, use_container_width=True)

    #######################################################################################################
    #################################### opção multiselect produto ########################################
    #######################################################################################################
    st.markdown(''' --- ''')
    produto_two = st.multiselect('Selecione até 10 produtos:', lista_produtos, max_selections=10, default=[lista_produtos[0],lista_produtos[1]]) # selectbox dos produtos

    teste2 = ano2022.loc[ano2022.Descricao.isin(produto_two)].reset_index()
    teste2.drop(columns=['index'],inplace = True)

    info = st.checkbox('Visualizar os produtos') # checkbox para visualizar a tabela com informações do produto 
    if info:
        st.write(pd.DataFrame(teste2))
    else:
        st.write("")

    #######################################################################################################
    ###################################### FPLOTANDO OS GRÁFICOS ##########################################
    #######################################################################################################

    fig1 = px.bar(teste2.sort_values(by = 'Qtd_Estq', ascending = False),
                x = 'Mes', y = 'Qtd_Estq', color = 'Descricao',
                labels = {'Mes': 'Mês', 'Qtd_Estq': 'Quantidade', 'Descricao': 'Produtos'})

    fig1.update_layout(title_text = ' Quantidade Estoque', title_font_size = 25, title_x = 0.455,
                    paper_bgcolor = 'rgb(243, 243, 243)', plot_bgcolor = 'rgb(243, 243, 243)')
    fig1.update_xaxes(tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                ticktext = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
    st.plotly_chart(fig1, use_container_width=True)
