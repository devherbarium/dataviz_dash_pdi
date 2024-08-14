import glob
import json
import os
from types import NoneType
import numpy as np
import pandas as pd
import plotly.colors as pc
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from sklearn.preprocessing import MinMaxScaler
from aux2 import *

img_path,base_path = img_base_pth()

container_name = "pdi-dashboard"
storage_account_key = os.getenv("storage_key")
# storage_account_key = read_storage_key('storage_key.txt')
# Defina suas credenciais e o nome do contêiner
storage_account_name = "hlbdatalake"
# Conectar ao BlobServiceClient usando a connection string
connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"

def Pubmed():
   # st.sidebar.image(Image.open(img_path+'\pubmed-logo.png'), width = 250)
   st.sidebar.image(open_img_from_blob(storage_account_key, "\Imagens\pubmed-logo.png"))

   #st.markdown('## <span style="color:#3B3D94"><center> Distribuição de Frequência </center> </span>', unsafe_allow_html=True) # Título da página
   st.markdown(''' --- ''')

   opcao = st.selectbox ('Escolha a opção desejada:',('Gráficos', 'Word Cloud'))
   
   if opcao == 'Gráficos':
      a, b, c  = st.tabs(["Frequência de Termos", "Score de Similaridade", "Tendências"]) # opção Tab para mostrar as 3 figuras
      with a:

         # df_tfidf = pd.read_excel(base_path+'\TF-IDF_PubMed.xlsx')
         df_tfidf = read_excel_from_blob(connection_string, container_name, "\Base_dados\TF-IDF_PubMed.xlsx", cols=None)

         # Filter in final_df
         dict_top_terms = {}
         dict_top_terms['aroma'] = df_tfidf.query("group == 'aroma'")
         dict_top_terms['canna'] = df_tfidf.query("group == 'canna'")
         dict_top_terms['supp'] = df_tfidf.query("group == 'supp'")
         dict_top_terms['herba'] = df_tfidf.query("group == 'herba'")
         dict_top_terms['prob'] = df_tfidf.query("group == 'prob'")

         def create_tuple_dictionary(dataframe):
            # Create an empty dictionary to store the values
            tuple_dict = {}

            # Iterate through the rows of the dataframe
            for index, row in dataframe.iterrows():
                # Get the values from the 'group', 'words_tfidf', and 'value_tfidf' columns
                group_value = row['group']
                words_tfidf_value = row['words_tfidf']
                value_tfidf_value = row['value_tfidf']

                # Create a tuple with the values
                tuple_value = (words_tfidf_value, value_tfidf_value)

                # Check if the group_value already exists in the dictionary
                if group_value in tuple_dict:
                    tuple_dict[group_value].append(tuple_value)
                else:
                    tuple_dict[group_value] = [tuple_value]

            return tuple_dict
         
         dict_from_groups = create_tuple_dictionary(df_tfidf)

         def plot_chart(dictionary, key_name, num_values):
            # Check if the specific key exists in the dictionary
            if type(key_name) is NoneType:
                return 
            if key_name not in dictionary:
                print(f"Error: '{key_name}' is not found in the dictionary.")
                return

            # Extract values from the dictionary based on the provided key_name
            values_tuple = dictionary[key_name][:num_values]

            # Extract keys and values from the values_tuple
            x = [t[0] for t in values_tuple]
            y = [t[1] for t in values_tuple]

            # Use a predefined color palette for colorful bars
            bar_colors = px.colors.qualitative.Plotly * (len(values_tuple) // len(px.colors.qualitative.Plotly) + 1)

            # Create the bar chart
            fig = go.Figure(data=[go.Bar(
                x=y,
                y=x,
                orientation='h',
                marker=dict(
                    color=bar_colors[:len(values_tuple)],  # Use only the required number of colors
                    line=dict(
                        color='rgba(58, 71, 80, 1.0)',
                        width=1.5,
                    )
                )
            )])

            # Customize the layout
            fig.update_layout(
                title=f'TF-IDF Frequency - Group {key_name}: Top {num_values} palavras (ano 2022)',
                xaxis_title='TF-IDF Frequency',
                yaxis_title='Palavras',
                height=600,  
                width=900,   
            )

            # Get the information from the 'top_search_terms' column for the specific key
            row = df_tfidf[df_tfidf['group'] == key_name].iloc[0]
            terms = row['top_search_terms']


            # Add subtitle as an annotation
            subtitle = f"{terms}"
            fig.add_annotation(
                go.layout.Annotation(
                    text=subtitle,
                    align='left',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=1.05,
                )
            )

            # Show the interactive plot
            return fig
         
         # Crie um dicionário de mapeamento para os nomes dos grupos
         group_names_tfidf = {
            "Aroma": "Aromaterapia",
            "Canna": "Cannabis",
            "Supp": "Suplementos",
            "Herba": "Fitoterápicos",
            "Prob": "Probióticos"
         }
         
         select_group = st.selectbox("Group:", group_names_tfidf.values(), key=5)
         num_words_tdidf = st.slider("Select Number of Words", min_value=5, max_value=50, value=30, key=4)

         if select_group == 'Aromaterapia':
            temp_group = 'aroma'
         elif select_group =='Cannabis':
             temp_group = 'canna'
         elif select_group == 'Suplementos':
             temp_group = 'supp'
         elif select_group == 'Fitoterápicos':
             temp_group = 'herba'
         else:
             temp_group = 'prob'
         
         st.plotly_chart(plot_chart(dict_from_groups, temp_group, num_words_tdidf))
         

      with b:  

         group_names_similarity = {
            "Aroma": "Aromaterapia",
            "Canna": "Cannabis",
            "Supp": "Suplementos",
            "Herba": "Fitoterápicos",
            "Prob": "Probióticos"
         }
         
         select_group_similarity = st.selectbox("Group:", group_names_similarity.values(), key=6)
         num_words_similarity = st.slider("Select Number of Words", min_value=5, max_value=100, value=30, key=7)
      
         graph_one, graph_two = st.tabs(['Areas Terapeuticas', 'Partes da Planta'])

         # df_similarity = pd.read_excel(base_path+'\SORTED-score-similarity.xlsx')
         df_similarity = read_excel_from_blob(connection_string, container_name, "\Base_dados\SORTED-score-similarity.xlsx", cols=None)
         
         # df_similarity_plants = pd.read_excel(base_path+'\SORTED-score-similarity-plants.xlsx')
         df_similarity_plants = read_excel_from_blob(connection_string, container_name, "\Base_dados\SORTED-score-similarity-plants.xlsx", cols=None)

         def plot_graph(group_df, group,number_words):
            df = group_df[group_df['Grupo'] == group].head(number_words)

            unique_combinations = set()

            # Filter out duplicate rows based on Palavra-Area and Score_Similaridade
            filtered_df = []
            for _, row in df.iterrows():
                combination = (row['Palavra-Area'], row['Score_Similaridade'])
                if combination not in unique_combinations:
                    filtered_df.append(row)
                    unique_combinations.add(combination)

            new_filtered_df = pd.DataFrame(filtered_df)

            num_bars = len(new_filtered_df)
            colorscale = pc.qualitative.Plotly

            fig = go.Figure(data=go.Bar(
                x=new_filtered_df['Palavra-Area'],
                y=new_filtered_df['Score_Similaridade'],
                marker=dict(color=new_filtered_df['Score_Similaridade'], colorscale=colorscale),
            ))

            fig.update_layout(
                title=f'Score Similarity - Group: {group}',
                xaxis_title='Palavra-Area',
                yaxis_title='Score_Similaridade'
            )

            return fig

         if select_group_similarity == 'Aromaterapia':
            temp_group = 'Aroma'
         elif select_group_similarity =='Cannabis':
             temp_group = 'Canna'
         elif select_group_similarity == 'Suplementos':
             temp_group = 'Supp'
         elif select_group_similarity == 'Fitoterápicos':
             temp_group = 'Herba'
         else:
             temp_group = 'Prob'

         with graph_one:
            st.plotly_chart(plot_graph(df_similarity, temp_group, num_words_similarity))

         with graph_two:
            st.plotly_chart(plot_graph(df_similarity_plants, temp_group, num_words_similarity))


         with c:

            group_names_trend = {
               "Aroma": "Aromaterapia",
               "Canna": "Cannabis",
               "Supp": "Suplementos",
               "Herba": "Fitoterápicos",
               "Prob": "Probióticos"
            }
            # Read .csv files (script from web scraping - PubMed)
            # Receive folder path and return a dict of search terms
            # def read_all_files(path):
            #     file_list_search_terms = {}
            #     files = glob.glob(path+"/*.csv")
            #     for file in files:
            #         file_df = pd.read_csv(file)
            #         text = str(file_df.iloc[0]) #row 0 from csv
            #         search_term = text.split('   ')[0].split(': ')[1] #get Search Term from csv
            #         file_list_search_terms[search_term] = file #save File name by {Search Term (key): file.csv}
            #
            #     return file_list_search_terms

            def read_all_files_from_blob(connection_string, container_name, directory_path):
                """
                Lê todos os arquivos CSV de uma pasta específica em um contêiner blob do Azure e retorna um dicionário
                com os termos de busca e nomes de arquivos.

                :param connection_string: String de conexão ao Azure Blob Storage.
                :param container_name: Nome do contêiner do blob.
                :param directory_path: Caminho do diretório dentro do contêiner do blob.
                :return: Dicionário com {termo_de_busca: nome_do_arquivo}.
                """
                file_list_search_terms = {}

                # Conectar ao serviço de blob
                blob_service_client = BlobServiceClient.from_connection_string(connection_string)
                container_client = blob_service_client.get_container_client(container_name)

                # Listar todos os blobs no diretório especificado
                blob_list = container_client.list_blobs(name_starts_with=directory_path)

                for blob in blob_list:
                    # Verificar se o blob é um arquivo CSV
                    if blob.name.endswith('.csv'):
                        # Baixar o blob
                        blob_client = container_client.get_blob_client(blob.name)
                        stream_downloader = blob_client.download_blob()
                        blob_data = stream_downloader.readall()

                        # Ler o conteúdo do blob como um DataFrame do pandas
                        file_df = pd.read_csv(BytesIO(blob_data))

                        # Extrair o termo de busca da primeira linha
                        text = str(file_df.iloc[0])  # linha 0 do CSV
                        search_term = text.split('   ')[0].split(': ')[1]  # obter o termo de busca do CSV

                        # Armazenar o termo de busca e o nome do arquivo no dicionário
                        file_list_search_terms[search_term] = blob.name

                return file_list_search_terms

            # Use the function 'read_files' to create the list with the words from dictionary
            results_folder_path = r"C:\Users\anna.silva\Documents\Entrega_Final_Sprint4\Codigos\0-Dashboard_Final\pubmed_dados\Results_Year_PubMed"
            # file_list_search_terms = read_all_files(results_folder_path)

            file_list_search_terms = read_all_files_from_blob(connection_string, container_name, "\Results_Year_PubMed")


            # Receive Search Term and get the corresponding CSV file
            def open_csv_file(file_path):
                try: 
                    return pd.read_csv(file_path, header=1) # no header

                except:
                    return  
                
            # For each search term .csv this function will read (open the file), get the year and count and save in a dict (key=search_term,year)
            # Return: {[search_term]: {[year_of_publication]:count_of_the_year,...}} 
            def read_year_count(file_list_search_terms):
                dict_term_year_count = {}
                for search_term in file_list_search_terms:
                    dataframe = open_csv_file(file_list_search_terms[search_term])
                    dict_term_year_count[search_term] = {}
                    for idx, year in enumerate(dataframe['Year']):
                        year = str(year)
                        dict_term_year_count[search_term][year] = dataframe['Count'][idx]

                return dict_term_year_count

            dict_term_year_count = read_year_count(file_list_search_terms)   
            #
            # dict_herb = pd.read_excel(base_path+'\dic_herb.xlsx')
            dict_herb = read_excel_from_blob(connection_string, container_name, "\Base_dados\dic_herb.xlsx")

            # Create a list of words from the same group
            grouped_words = dict_herb.groupby('Group')['Search Term'].apply(lambda x: list(x))

            # List of terms of each category 
            aroma_list_words = grouped_words[0]
            cannabis_list_words = grouped_words[1]
            supp_list_words = grouped_words[2]
            herba_list_words = grouped_words[3]
            prob_list_words = grouped_words[4]

            # Create dictionaries for each group to store the results
            dict_aroma = {}
            dict_cannabis = {}
            dict_supp = {}
            dict_herba = {}
            dict_prob = {}

            # Group the terms of each group using the main dictionary dict_term_year_count
            for term in aroma_list_words:
                if term in dict_term_year_count:
                    dict_aroma[term] = dict_term_year_count[term]

            for term in cannabis_list_words:
                if term in dict_term_year_count:
                    dict_cannabis[term] = dict_term_year_count[term]

            for term in supp_list_words:
                if term in dict_term_year_count:
                    dict_supp[term] = dict_term_year_count[term]

            for term in herba_list_words:
                if term in dict_term_year_count:
                    dict_herba[term] = dict_term_year_count[term]

            for term in prob_list_words:
                if term in dict_term_year_count:
                    dict_prob[term] = dict_term_year_count[term]

            def visualize_year_count_plotly(data_dict, group_name):
               fig = go.Figure()
               fig.update_layout(title=f"Year Count for Group: {group_name}",
                                 xaxis_title="Year of Publication",
                                 yaxis_title="Count")

               for term, year_count in data_dict.items():
                   years = list(year_count.keys())
                   counts = list(year_count.values())

                   # Convert years to integers and sort the data by year
                   years_int = [int(year) for year in years]
                   years_sorted, counts_sorted = zip(*sorted(zip(years_int, counts)))

                   fig.add_trace(go.Scatter(x=years_sorted, y=counts_sorted, mode='lines', name=term))

               return fig

            group_name = st.selectbox("Select Group", group_names_trend.values(), key=1)
            num_years_choice = st.slider("Select Number of Years for Publications", min_value=1, max_value=70, value=5, key=2)
            trend_years_choice = st.slider("Select Number of Years for Trend", min_value=1, max_value=22, value=5, key=3)

            graph_1, graph_2, graph_3, graph_4 = st.tabs(['Série Temporal', 'Série temporal - anos', 'Tendência para o grupo', 'Tendência para um periodo específico'])

            if group_name == 'Aromaterapia':
               dict_temp = dict_aroma
            elif group_name =='Cannabis':
                dict_temp = dict_cannabis
            elif group_name == 'Suplementos':
                dict_temp = dict_supp
            elif group_name == 'Fitoterápicos':
                dict_temp = dict_herba
            else:
                dict_temp = dict_prob

            with graph_1:
               # Visualize the data for each group 
               st.plotly_chart(visualize_year_count_plotly(dict_temp, group_name))

            def select_num_years(data_dict, group_name, num_years):
               fig = go.Figure()
               num_years = int(num_years)
               year_for_title = 2023 - num_years
               fig.update_layout(title=f"Last {num_years} years (2022 - {year_for_title}): {group_name}",
                                 xaxis_title="Year of Publication",
                                 yaxis_title="Count")

               for term, year_count in data_dict.items():
                   years = list(year_count.keys())
                   counts = list(year_count.values())

                   # Convert years to integers and sort the data by year
                   years_int = [int(year) for year in years]
                   years_sorted, counts_sorted = zip(*sorted(zip(years_int, counts)))

                   # Filter data for the last num_years starting from 2023
                   years_filtered = [year for year in years_sorted if year >= 2023 - num_years + 1]
                   counts_filtered = [counts_sorted[i] for i, year in enumerate(years_sorted) if year >= 2023 - num_years + 1]

                   fig.add_trace(go.Scatter(x=years_filtered, y=counts_filtered, mode='lines+markers', name=term))

               return fig
            
            with graph_2:
               # Visualize the data for each group 
               st.plotly_chart(select_num_years(dict_temp, group_name, num_years_choice))

            def trend_chart(dict_group, group_name):
               df = pd.DataFrame(dict_group)
        
               # Convert the index to a datetime object
               df.index = pd.to_datetime(df.index)
               
               # Calculate the total publication counts for each year
               df['Total Counts'] = df.sum(axis=1)

               # Fit a linear trend line to the total publication counts
               coefficients = np.polyfit(df.index.year, df['Total Counts'], 1)
               trend = np.polyval(coefficients, df.index.year)

               # Filter the data to keep only the positive trend values
               positive_trend_mask = trend >= 0
               df_positive_trend = df[positive_trend_mask]
               trend_positive = trend[positive_trend_mask]

               # Create a Plotly Express line chart for positive trend supplements
               fig = px.line(df_positive_trend, x=df_positive_trend.index, y=['Total Counts'], 
                             title=f'{group_name} - Publication Trends Over Time',
                             labels={'index': 'Year', 'Total Counts': 'Publication Counts'})

               # Add the trend line to the plot using the add_trace() method
               fig.add_trace(go.Scatter(x=df_positive_trend.index, y=trend_positive, mode='lines', name='Trend Line'))

               # Update x-axis labels for better readability
               fig.update_xaxes(tickangle=45)

               # Show the plot
               return fig
            
            with graph_3:
               print(dict_temp)
               # Visualize the data for each group 
               st.plotly_chart(trend_chart(dict_temp, group_name))

            def test_create_df(dict_group, start_year, end_year):
               # create a transposed df from dict_group
               df = pd.DataFrame(dict_group).T

               # Select columns from year 2022 to 2000
               #start_year = 2022
               #end_year = 2020

               selected_columns = df.loc[:, str(start_year):str(end_year)]

               missing_data = selected_columns.isnull()
               missing_counts = missing_data.sum()

               # Problems with Nan values:
               # Fill NaN values in each column with the mean of the column
               filled_df = selected_columns.fillna(selected_columns.mean())

               # Data standardization
               # Calculate the mean and standard deviation for each year (column)
               means = filled_df.mean(axis=0)
               stds = filled_df.std(axis=0)

               # Apply standardization to the DataFrame
               standardized_df = (filled_df - means) / stds


               # Min-Max Scaling preserves the shape of the original distribution
               scaler = MinMaxScaler()
               scaled_data = scaler.fit_transform(standardized_df)
               scaled_df = pd.DataFrame(scaled_data, columns=standardized_df.columns, index=standardized_df.index)

               return scaled_df.T
            
            def test_trend_chart(group_name, dict_group, end_year):
               start_year = '2022'

               # create df
               df = test_create_df(dict_group, start_year, end_year)

               # Convert the index to a datetime object
               df.index = pd.to_datetime(df.index)

               # Calculate the total publication counts for each year
               df['Total Counts'] = df.sum(axis=1)

               # Fit a linear trend line to the total publication counts
               coefficients = np.polyfit(df.index.year, df['Total Counts'], 1)
               trend = np.polyval(coefficients, df.index.year)

               # Filter the data to keep only the positive trend values
               positive_trend_mask = trend >= 0
               df_positive_trend = df[positive_trend_mask]
               trend_positive = trend[positive_trend_mask]

               # Calculate the mean of 'Total Counts'
               mean_total_counts = df['Total Counts'].mean()

               # Create a Plotly Express line chart for positive trend supplements
               fig = px.line(df_positive_trend, x=df_positive_trend.index, y=['Total Counts'], 
                             title=f' {group_name} - Publication Trends Over Time (2022 - {end_year})',
                             labels={'index': 'Year', 'Total Counts': 'Publication Counts'})

               # Add the trend line to the plot using the add_trace() method
               fig.add_trace(go.Scatter(x=df_positive_trend.index, y=trend_positive, mode='lines', name='Trend Line'))

               # Add the mean line to the plot
               fig.add_trace(go.Scatter(x=df_positive_trend.index, y=[mean_total_counts] * len(df_positive_trend.index),
                                        mode='lines', name='Mean Line', line=dict(dash='dash')))

               # Update x-axis labels for better readability
               fig.update_xaxes(tickangle=45)

               # Show the plot
               return fig
            
            with graph_4:
               # Visualize the data for each group 
               
               st.plotly_chart(test_trend_chart(group_name, dict_temp, str(2022 - trend_years_choice)))



   elif opcao == 'Word Cloud':
      # # Função para carregar um dicionário a partir de um arquivo JSON
      # def load_dict(filename):
      #    with open(os.path.join('Base_dados', filename), "r") as f:
      #          return json.load(f)

      def load_dict_from_blob(connection_string, container_name, blob_name):
          """
          Carrega um arquivo JSON de um contêiner blob do Azure e retorna seu conteúdo como um dicionário.

          :param connection_string: String de conexão ao Azure Blob Storage.
          :param container_name: Nome do contêiner do blob.
          :param blob_name: Nome do arquivo blob.
          :return: Dicionário com os dados do arquivo JSON.
          """
          # Conectar ao serviço de blob
          blob_service_client = BlobServiceClient.from_connection_string(connection_string)
          container_client = blob_service_client.get_container_client(container_name)

          # Baixar o blob
          blob_client = container_client.get_blob_client(blob_name)
          stream_downloader = blob_client.download_blob()
          blob_data = stream_downloader.readall()

          # Ler o conteúdo do blob como um dicionário JSON
          data = json.load(BytesIO(blob_data))

          return data

      # Dicionário para armazenar os top words de cada grupo
      top_words = {
         'Aromaterapia': load_dict_from_blob(connection_string, container_name,"\Base_dados\aroma_terms_top_words.json"),
         'Cannabis': load_dict_from_blob(connection_string, container_name,"\Base_dados\canna_terms_top_words.json"),
         'Suplementos': load_dict_from_blob(connection_string, container_name,"\Base_dados\supp_terms_top_words.json"),
         'Fitoterápicos': load_dict_from_blob(connection_string, container_name,"\Base_dados\herba_terms_top_words.json"),
         'Probióticos': load_dict_from_blob(connection_string, container_name,"\Base_dados\prob_terms_top_words.json")
      }

      # Função para criar uma nuvem de palavras
      #def create_wordcloud(group_top_words):
         # Create a WordCloud object
         #wordcloud = WordCloud(width=1600, height=800, background_color="white", max_words=1000, contour_width=3, contour_color='steelblue',collocations=False)

         # Generate a word cloud
         #wordcloud.generate_from_frequencies(group_top_words)

         # Save the word cloud to a PIL image
         #return wordcloud.to_array()

      # Use a selectbox to let users choose which word cloud to view
      #choice = st.selectbox("Selecione o Wordcloud", list(top_words.keys()))

      # Generate the word cloud for the selected group
      #wordcloud_image = create_wordcloud(top_words[choice])

      # Display the selected word cloud
     # st.image(wordcloud_image, use_column_width=True)
