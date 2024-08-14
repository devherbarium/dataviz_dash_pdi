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

def NutraIngredients():

    #######################################################################################################
    ########################################## Base de dados ##############################################
    #######################################################################################################

    # Estoque = pd.read_csv('Base_dados/Estoque.csv')
    Estoque = read_csv_from_blob(connection_string, container_name, "\Base_dados\Estoque.csv")

    st.markdown('## <span style="color:#3B3D94"> <center> Análise Temporal </center> </span>', unsafe_allow_html=True)   # Título da página
    st.markdown(''' --- ''')


    ano2022 = Estoque.groupby('Ano').get_group(2022).reset_index() # DataFrame do ano de 2022
    ano2022.drop(columns=['index', 'Unnamed: 0'],inplace = True)   # Excluindo a coluna index
    ano2022['Mes'] = ano2022['Mes'].replace(['Janeiro', 'Fevereiro','Março', 'Abril', 'Maio', 'Junho', 'Julho',
                                             'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
                                             [1, 2, 3,4, 5, 6, 7, 8, 9, 10, 11 ,12]) # Trocando os nomes dos meses por números
    
    #######################################################################################################
    ############################################# Marca ###################################################
    #######################################################################################################

    st.markdown('### <span style="color:#3B3D94"> Marca </span>', unsafe_allow_html=True) # Subtítulo

    #######################################################################################################
    ##################################### PLOTANDO OS GRÁFICOS ############################################
    #######################################################################################################

    a, b, c = st.tabs(["Venda Liberada", "Quantidade Estoque", "Quantidade Produzido"]) # opção Tab para mostrar as 3 figuras

    f2 = ano2022.groupby('Marca').get_group('EXCLUSIVO')
    f3 = ano2022.groupby('Marca').get_group('CAEMMUN B2C')
    f4 = ano2022.groupby('Marca').get_group('CAEMMUN OFFICE')
    f5 = ano2022.groupby('Marca').get_group('CAEMMUN')
    f6 = ano2022.groupby('Marca').get_group('CAEMMUN ROOMS')

    with a:

        mes_f2 = f2.groupby('Mes')[['Ven_Lib']].sum().reset_index()
        mes_f3 = f3.groupby('Mes')[['Ven_Lib']].sum().reset_index()
        mes_f4 = f4.groupby('Mes')[['Ven_Lib']].sum().reset_index()
        mes_f5 = f5.groupby('Mes')[['Ven_Lib']].sum().reset_index()
        mes_f6 = f6.groupby('Mes')[['Ven_Lib']].sum().reset_index()


        trace_f2 = go.Scatter(x = mes_f2['Mes'], y = mes_f2['Ven_Lib'], mode = 'markers+lines', name = 'EXCLUSIVO')
        trace_f3 = go.Scatter(x = mes_f3['Mes'], y = mes_f3['Ven_Lib'], mode = 'markers+lines', name = 'CAEMMUN B2C')
        trace_f4 = go.Scatter(x = mes_f4['Mes'], y = mes_f4['Ven_Lib'], mode = 'markers+lines', name = 'CAEMMUN OFFICE')
        trace_f5 = go.Scatter(x = mes_f5['Mes'], y = mes_f5['Ven_Lib'], mode = 'markers+lines', name = 'CAEMMUN')
        trace_f6 = go.Scatter(x = mes_f6['Mes'], y = mes_f6['Ven_Lib'], mode = 'markers+lines', name = 'CAEMMUN ROOMS')

        data = [trace_f2, trace_f3, trace_f4, trace_f5, trace_f6]

        layout = go.Layout(title_text = 'Venda Liberada  X Marca (2022)', title_font_size = 25, title_x = 0.2,
                        xaxis = {'title': 'Mês'}, yaxis = {'title': 'Venda Liberada'},
                        paper_bgcolor = 'rgb(243, 243, 243)', plot_bgcolor = 'rgb(243, 243, 243)')

        fig = go.Figure(data = data, layout = layout)
        fig.update_xaxes(tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                 ticktext = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
        st.plotly_chart(fig, use_container_width=True)

    with b:
        
        mes_f2 = f2.groupby('Mes')[['Qtd_Estq']].sum().reset_index()
        mes_f3 = f3.groupby('Mes')[['Qtd_Estq']].sum().reset_index()
        mes_f4 = f4.groupby('Mes')[['Qtd_Estq']].sum().reset_index()
        mes_f5 = f5.groupby('Mes')[['Qtd_Estq']].sum().reset_index()
        mes_f6 = f6.groupby('Mes')[['Qtd_Estq']].sum().reset_index()


        trace_f2 = go.Scatter(x = mes_f2['Mes'], y = mes_f2['Qtd_Estq'], mode = 'markers+lines', name = 'EXCLUSIVO')
        trace_f3 = go.Scatter(x = mes_f3['Mes'], y = mes_f3['Qtd_Estq'], mode = 'markers+lines', name = 'CAEMMUN B2C')
        trace_f4 = go.Scatter(x = mes_f4['Mes'], y = mes_f4['Qtd_Estq'], mode = 'markers+lines', name = 'CAEMMUN OFFICE')
        trace_f5 = go.Scatter(x = mes_f5['Mes'], y = mes_f5['Qtd_Estq'], mode = 'markers+lines', name = 'CAEMMUN')
        trace_f6 = go.Scatter(x = mes_f6['Mes'], y = mes_f6['Qtd_Estq'], mode = 'markers+lines', name = 'CAEMMUN ROOMS')

        data = [trace_f2, trace_f3, trace_f4, trace_f5, trace_f6]

        layout = go.Layout(title_text = 'Quantidade Estoque X Marca (2022)', title_font_size = 25, title_x = 0.2,
                        xaxis = {'title': 'Mês'}, yaxis = {'title': 'Quantidade Estoque'},
                        paper_bgcolor = 'rgb(243, 243, 243)', plot_bgcolor = 'rgb(243, 243, 243)')

        fig = go.Figure(data = data, layout = layout)
        fig.update_xaxes(tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                 ticktext = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
        st.plotly_chart(fig, use_container_width=True)

    with c:
    
        mes_f2 = f2.groupby('Mes')[['Qtd_O_P']].sum().reset_index()
        mes_f3 = f3.groupby('Mes')[['Qtd_O_P']].sum().reset_index()
        mes_f4 = f4.groupby('Mes')[['Qtd_O_P']].sum().reset_index()
        mes_f5 = f5.groupby('Mes')[['Qtd_O_P']].sum().reset_index()
        mes_f6 = f6.groupby('Mes')[['Qtd_O_P']].sum().reset_index()


        trace_f2 = go.Scatter(x = mes_f2['Mes'], y = mes_f2['Qtd_O_P'], mode = 'markers+lines', name = 'EXCLUSIVO')
        trace_f3 = go.Scatter(x = mes_f3['Mes'], y = mes_f3['Qtd_O_P'], mode = 'markers+lines', name = 'CAEMMUN B2C')
        trace_f4 = go.Scatter(x = mes_f4['Mes'], y = mes_f4['Qtd_O_P'], mode = 'markers+lines', name = 'CAEMMUN OFFICE')
        trace_f5 = go.Scatter(x = mes_f5['Mes'], y = mes_f5['Qtd_O_P'], mode = 'markers+lines', name = 'CAEMMUN')
        trace_f6 = go.Scatter(x = mes_f6['Mes'], y = mes_f6['Qtd_O_P'], mode = 'markers+lines', name = 'CAEMMUN ROOMS')

        data = [trace_f2, trace_f3, trace_f4, trace_f5, trace_f6]

        layout = go.Layout(title_text = 'Quantidade Produzido X Marca (2022)', title_font_size = 25, title_x = 0.2,
                        xaxis = {'title': 'Mês'}, yaxis = {'title': 'Quantidade Produzido'},
                        paper_bgcolor = 'rgb(243, 243, 243)', plot_bgcolor = 'rgb(243, 243, 243)')

        fig = go.Figure(data = data, layout = layout)
        fig.update_xaxes(tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                 ticktext = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
        st.plotly_chart(fig, use_container_width=True)

    #######################################################################################################
    ###################################### Tipo Armazenamento #############################################
    #######################################################################################################

    st.markdown(''' --- ''')
    st.markdown('### <span style="color:#3B3D94"> Tipo Armazenamento </span>', unsafe_allow_html=True) # Subtítulo

    #######################################################################################################
    ###################################### FPLOTANDO OS GRÁFICOS ##########################################
    #######################################################################################################
            
    d, e, f = st.tabs(["Venda Liberada", " Quantidade Estoque", "Quantidade Produzido"]) # opção Tab para mostrar as 3 figuras

    g2 = ano2022.groupby('Tipo Armazenamento').get_group('Caemmun')
    g3 = ano2022.groupby('Tipo Armazenamento').get_group('Private Pedido')
    g4 = ano2022.groupby('Tipo Armazenamento').get_group('White Label Pedido')
    g5 = ano2022.groupby('Tipo Armazenamento').get_group('Private Estoque')
    g6 = ano2022.groupby('Tipo Armazenamento').get_group('White Label Estoque')

    with d:

        mes_g2 = g2.groupby('Mes')[['Ven_Lib']].sum().reset_index()
        mes_g3 = g3.groupby('Mes')[['Ven_Lib']].sum().reset_index()
        mes_g4 = g4.groupby('Mes')[['Ven_Lib']].sum().reset_index()
        mes_g5 = g5.groupby('Mes')[['Ven_Lib']].sum().reset_index()
        mes_g6 = g6.groupby('Mes')[['Ven_Lib']].sum().reset_index()

        trace_g2 = go.Scatter(x = mes_g2['Mes'], y = mes_g2['Ven_Lib'], mode = 'markers+lines', name = 'Caemmun')
        trace_g3 = go.Scatter(x = mes_g3['Mes'], y = mes_g3['Ven_Lib'], mode = 'markers+lines', name = 'Private Pedido')
        trace_g4 = go.Scatter(x = mes_g4['Mes'], y = mes_g4['Ven_Lib'], mode = 'markers+lines', name = 'White Label Pedido')
        trace_g5 = go.Scatter(x = mes_g5['Mes'], y = mes_g5['Ven_Lib'], mode = 'markers+lines', name = 'Private Estoque')
        trace_g6 = go.Scatter(x = mes_g6['Mes'], y = mes_g6['Ven_Lib'], mode = 'markers+lines', name = 'White Label Estoque')

        data = [trace_g2, trace_g3, trace_g4, trace_g5, trace_g6]

        layout = go.Layout(title_text = 'Venda Liberada X Tipo Armazenamento (2022)', title_font_size = 25, title_x = 0.15,
                        xaxis = {'title': 'Mês'}, yaxis = {'title': 'Venda Liberada'},
                        paper_bgcolor = 'rgb(243, 243, 243)', plot_bgcolor = 'rgb(243, 243, 243)')

        fig = go.Figure(data = data, layout = layout)
        fig.update_xaxes(tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                 ticktext = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
        st.plotly_chart(fig, use_container_width=True)

    with e:

        mes_g2 = g2.groupby('Mes')[['Qtd_Estq']].sum().reset_index()
        mes_g3 = g3.groupby('Mes')[['Qtd_Estq']].sum().reset_index()
        mes_g4 = g4.groupby('Mes')[['Qtd_Estq']].sum().reset_index()
        mes_g5 = g5.groupby('Mes')[['Qtd_Estq']].sum().reset_index()
        mes_g6 = g6.groupby('Mes')[['Qtd_Estq']].sum().reset_index()

        trace_g2 = go.Scatter(x = mes_g2['Mes'], y = mes_g2['Qtd_Estq'], mode = 'markers+lines', name = 'Caemmun')
        trace_g3 = go.Scatter(x = mes_g3['Mes'], y = mes_g3['Qtd_Estq'], mode = 'markers+lines', name = 'Private Pedido')
        trace_g4 = go.Scatter(x = mes_g4['Mes'], y = mes_g4['Qtd_Estq'], mode = 'markers+lines', name = 'White Label Pedido')
        trace_g5 = go.Scatter(x = mes_g5['Mes'], y = mes_g5['Qtd_Estq'], mode = 'markers+lines', name = 'Private Estoque')
        trace_g6 = go.Scatter(x = mes_g6['Mes'], y = mes_g6['Qtd_Estq'], mode = 'markers+lines', name = 'White Label Estoque')

        data = [trace_g2, trace_g3, trace_g4, trace_g5, trace_g6]

        layout = go.Layout(title_text = 'Quantidade Estoque X Tipo Armazenamento (2022)', title_font_size = 25, title_x = 0.15,
                        xaxis = {'title': 'Mês'}, yaxis = {'title': 'Quantidade Estoque'},
                        paper_bgcolor = 'rgb(243, 243, 243)', plot_bgcolor = 'rgb(243, 243, 243)')

        fig = go.Figure(data = data, layout = layout)
        fig.update_xaxes(tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                 ticktext = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
        st.plotly_chart(fig, use_container_width=True)
    
    with f:

        mes_g2 = g2.groupby('Mes')[['Qtd_O_P']].sum().reset_index()
        mes_g3 = g3.groupby('Mes')[['Qtd_O_P']].sum().reset_index()
        mes_g4 = g4.groupby('Mes')[['Qtd_O_P']].sum().reset_index()
        mes_g5 = g5.groupby('Mes')[['Qtd_O_P']].sum().reset_index()
        mes_g6 = g6.groupby('Mes')[['Qtd_O_P']].sum().reset_index()

        trace_g2 = go.Scatter(x = mes_g2['Mes'], y = mes_g2['Qtd_O_P'], mode = 'markers+lines', name = 'Caemmun')
        trace_g3 = go.Scatter(x = mes_g3['Mes'], y = mes_g3['Qtd_O_P'], mode = 'markers+lines', name = 'Private Pedido')
        trace_g4 = go.Scatter(x = mes_g4['Mes'], y = mes_g4['Qtd_O_P'], mode = 'markers+lines', name = 'White Label Pedido')
        trace_g5 = go.Scatter(x = mes_g5['Mes'], y = mes_g5['Qtd_O_P'], mode = 'markers+lines', name = 'Private Estoque')
        trace_g6 = go.Scatter(x = mes_g6['Mes'], y = mes_g6['Qtd_O_P'], mode = 'markers+lines', name = 'White Label Estoque')

        data = [trace_g2, trace_g3, trace_g4, trace_g5, trace_g6]

        layout = go.Layout(title_text = 'Quantidade Produzido X Tipo Armazenamento (2022)', title_font_size = 25, title_x = 0.15,
                        xaxis = {'title': 'Mês'}, yaxis = {'title': 'Quantidade Produzido'},
                        paper_bgcolor = 'rgb(243, 243, 243)', plot_bgcolor = 'rgb(243, 243, 243)')

        fig = go.Figure(data = data, layout = layout)
        fig.update_xaxes(tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                 ticktext = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
        st.plotly_chart(fig, use_container_width=True)
