import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from aux2 import *
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import os
import re
import types
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


container_name = "pdi-dashboard"
storage_account_key = os.getenv("storage_key")
# storage_account_key = read_storage_key('storage_key.txt')
# Defina suas credenciais e o nome do contêiner
storage_account_name = "hlbdatalake"
# Conectar ao BlobServiceClient usando a connection string
connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"

st.set_option('deprecation.showPyplotGlobalUse', False)

# Baixar o conjunto de stopwords, se necessário
nltk.download('stopwords')
nltk.download('wordnet')

# Baixar o conjunto de stopwords, se necessário
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
img_path,base_path = img_base_pth()

def Nutraceutical():

   
   st.markdown(''' --- ''')

   opcao = st.selectbox ('Escolha a opção desejada:',('Gráficos', 'Word Cloud'))
   
   if opcao == 'Gráficos':
      
      a, b, c = st.tabs(['Segmentação de Notícias com t-SNE','Tendência dos Segmentos de Notícias', 'Notícias x Sentimento']) 
      
      with a:

         #  # Baixar o conjunto de stopwords, se necessário
         # nltk.download('stopwords')
         # nltk.download('wordnet')
         #
         #
         # # Agora você pode usar o conjunto de stopwords sem problemas
         # stop_words = set(stopwords.words('english'))

         # Função de hash personalizada
         def my_hash_func(func):
            return str(func)

         # Função para carregar dados
         @st.cache(hash_funcs={types.FunctionType: my_hash_func}, allow_output_mutation=True)
         def load_data():
            # file_path = os.path.join(base_path, r'3_noticias_nutraceutical_final.csv')
            # file_path ="C:\\Users\\anna.silva\\Documents\\Entrega_Final_Sprint4\\Codigos\\0-Dashboard_Final\\Base_dados\\3_noticias_nutraceutical_final.csv"
            # news_data = pd.read_csv(file_path)
            news_data = read_csv_from_blob(connection_string, container_name , "\Base_dados\\3_noticias_nutraceutical_final.csv")

            news_data['Noticia'].fillna("", inplace=True)
            news_data['Processed_Noticia'] = news_data['Noticia'].apply(preprocess_text)
            return news_data

         # Função para pré-processar o texto das notícias
         # stop_words = set(stopwords.words('english'))
         lemmatizer = WordNetLemmatizer()

         def preprocess_text(text):
            text = text.lower()
            text = re.sub(r'[^\w\s]', '', text)
            text = [lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words]
            return " ".join(text)

         # Carregar os dados
         news_data = load_data()

         # Slider para seleção do número de clusters
         num_clusters = st.slider("Número de Clusters", min_value=2, max_value=10, value=4)

         # Vetorização TF-IDF
         tfidf_vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
         tfidf_matrix = tfidf_vectorizer.fit_transform(news_data['Processed_Noticia'])

         # Aplicando o KMeans
         kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(tfidf_matrix)
         news_data['Cluster'] = kmeans.labels_

         # Reduzindo a dimensionalidade usando t-SNE
         tsne_model = TSNE(n_components=2, init='random', random_state=42)
         low_dim_data = tsne_model.fit_transform(tfidf_matrix)

         # Criando um DataFrame com os dados reduzidos e os labels dos clusters
         tsne_df = pd.DataFrame(low_dim_data, columns=['x', 'y'])
         tsne_df['Cluster'] = kmeans.labels_

         # Gráfico de dispersão com cores distintas
         fig, ax = plt.subplots(figsize=(10, 8))
         sns.scatterplot(x='x', y='y', hue='Cluster', palette='viridis', data=tsne_df, ax=ax)
         plt.title('Visualização t-SNE dos Clusters')
         st.pyplot(fig)

         # Adicionando um seletor para escolher um cluster específico
         selected_cluster = st.selectbox("Selecione um Cluster para Exibir:", list(range(num_clusters)))

         # Filtrando o DataFrame para mostrar apenas as notícias do cluster selecionado
         filtered_data = news_data[news_data['Cluster'] == selected_cluster]

         # # Mostrando os dados filtrados
         # st.write(filtered_data)

         # Mostrando os dados filtrados com links clicáveis
         st.write("### Notícias do Cluster Selecionado")
         for index, row in filtered_data.iterrows():
            st.markdown(f"[{row['Noticia']}]({row['Fonte']})")



      with b: 

         news_data = load_data()
               
         # Convertendo a coluna de data para o tipo correto
         news_data['Data_Hora_Acesso'] = pd.to_datetime(news_data['Data_Hora_Acesso'],errors='coerce')
         
         # Agrupando por mês e cluster
         trends = news_data.groupby([news_data['Data_Hora_Acesso'].dt.to_period("M"), 'Cluster']).size().reset_index(name='Counts')
         
         # Convertendo de volta para data
         trends['Data_Hora_Acesso'] = trends['Data_Hora_Acesso'].dt.to_timestamp()
         
         # Plotando
         plt.figure(figsize=(12, 6))
         sns.lineplot(x='Data_Hora_Acesso', y='Counts', hue='Cluster', data=trends)
         plt.title('Tendências dos Clusters ao Longo do Tempo')
         
         st.pyplot()


      with c: 
         # Carregar o DataFrame mesclado
         # merged_df = pd.read_csv(r"C:\Users\anna.silva\Documents\Entrega_Final_Sprint4\Codigos\3-nutraceutical\3_noticias_nutraceutical_com_sentimento.csv")
         merged_df = read_csv_from_blob(connection_string, container_name,
                                        "\\3-nutraceutical\\3_noticias_nutraceutical_com_sentimento.csv")
         # Adicionar uma coluna de Sentimento
         conditions = [
            (merged_df['compound'] > 0.05),
            (merged_df['compound'] < -0.05),
            (merged_df['compound'] >= -0.05) & (merged_df['compound'] <= 0.05)
         ]
         choices = ['Positivo', 'Negativo', 'Neutro']
         merged_df['Sentimento'] = pd.Series(pd.Categorical(pd.cut(merged_df['compound'], bins=[-1, -0.05, 0.05, 1], labels=['Negativo', 'Neutro', 'Positivo']), categories=choices))

         # Agregar dados para o gráfico Sunburst
         agg_data = merged_df.groupby(['Fonte', 'Sentimento']).size().reset_index(name='Contagem')

         # Criar o gráfico Sunburst
         fig = px.sunburst(
            agg_data,
            path=['Sentimento', 'Fonte'],
            values='Contagem',
            color='Sentimento',
            title='Gráfico Sunburst para Categorias de Notícias e Sentimento'
         )
         fig.update_layout(width=1000, height=1000)
         st.plotly_chart(fig)

         # Seletor para escolher o Sentimento
         selected_sentiment = st.selectbox("Escolha o Sentimento:", agg_data['Sentimento'].unique())

         # Filtrar os dados para encontrar o link correspondente
         filtered_data = merged_df[merged_df['Sentimento'] == selected_sentiment]

         # Exibir os links
         if not filtered_data.empty:
            st.write(f"Links para as notícias com sentimento '{selected_sentiment}':")
            for i, row in filtered_data.iterrows():
                  st.write(f"[{row['Noticia']}]({row['Fonte']})")
         else:
            st.write("Nenhum link encontrado para a seleção.")
#######################################################################################################
############################################ word cloud ###############################################
#######################################################################################################

   if opcao == 'Word Cloud':
      opcao2 = st.selectbox(
      'Selecione o Wordcloud',
      ('Marcas', 'Produtos'))   
      
      if opcao2 == 'Marcas':
         # Ler o arquivo CSV existente em um dataframe
         # df_concat = pd.read_csv(os.path.join(base_path,'8_categorias_iherb.csv'))
         # df_concat = pd.read_csv("C:\\Users\\anna.silva\\Documents\\Entrega_Final_Sprint4\\Codigos\\0-Dashboard_Final\\Base_dados\\8_categorias_iherb.csv")
         df_concat = read_csv_from_blob(connection_string, container_name,
                                        "\\Base_dados\\8_categorias_iherb.csv")
         # Concatenar o texto para a nuvem de palavras
         text_marca_concat = " ".join(review for review in df_concat.Marca)

         # Criar filtro de palavras irrelevantes para a análise pretendida:
         stopwords = set(STOPWORDS)
         stopwords.update(["ml", "fl", "oz", "Sem", "mg", "de", "sem", "e", "sistema", "premium",
                           "classe", "ao", "lb", "g", "mcg", "now", "plus", "pura", "gold",
                           "california", "bioperine", "nutrition",
                           "complexo",
                           "capsula",
                           "gel",
                           "Cápsulas Softgel",
                           "Cápsulas",
                           "Softgel",
                           "para",
                           "em",
                           "crianças",
                           "Alta"
                           "Absorção",
                           "Pó",
                           "Sabor",
                           "Alta Absorção",
                           "Homens", "Natural",
                           "Vegetais", "Mulheres", "Abelha", "Parede", "Animal", "por", "Dia", "Dosagem", "Dupla",
                           "Vegetariana", "UI", "Alta", "Absorção", "kg", "lbs", "Unhas", "Perdas",
                           "Cabelos", "Pele", "Suplementos",
                           "Vegetarianas", "Life", "Animal",
                           "Gelatina", "Rápida", "Formato",
                           "Uma Vez", "Comprimidos", "Goma", "Vez", "Memória", "Uma", "Extrato", "Dosagem Dupla",
                           "Bilhões", "à", "de", "Juba", "Completo", "Liberação",
                           ])

         # Step 1 and 2: WordCloud's generate function will do the tokenization and frequency counting
         wordcloud = WordCloud(width = 800, height = 800, 
                        background_color ='white', 
                        stopwords = stopwords, 
                        min_font_size = 10).generate(text_marca_concat) 

         # Step 3: Generate the word cloud
         plt.figure(figsize = (8, 8), facecolor = None) 
         plt.imshow(wordcloud) 
         plt.axis("off") 
         plt.tight_layout(pad = 0)

         # Displaying the plot in Streamlit
         st.pyplot(plt)
      
      elif opcao2 == 'Produtos':
         # Ler o arquivo CSV existente em um dataframe
         # df_concat = pd.read_csv(os.path.join(base_path,'8_categorias_iherb.csv'))
         # df_concat = pd.read_csv("C:\\Users\\anna.silva\\Documents\\Entrega_Final_Sprint4\\Codigos\\0-Dashboard_Final\\Base_dados\\8_categorias_iherb.csv")
         df_concat = read_csv_from_blob(connection_string, container_name,
                                        "\\Base_dados\\8_categorias_iherb.csv")
         # Concatenar o texto para a nuvem de palavras
         text_produto_concat = " ".join(review for review in df_concat.Produto)

         # Criar filtro de palavras irrelevantes para a análise pretendida:
         stopwords = set(STOPWORDS)
         stopwords.update(["ml", "fl", "oz", "Sem", "mg", "de", "sem", "e", "sistema", "premium",
                           "classe", "ao", "lb", "g", "mcg", "now", "plus", "pura",
                           "gold", "california", "bioperine", "nutrition",
                           "complexo",
                           "capsula",
                           "gel",
                           "Cápsulas Softgel",
                           "Cápsulas",
                           "Softgel",
                           "para",
                           "em",
                           "crianças",
                           "Alta"
                           "Absorção",
                           "Pó",
                           "Sabor",
                           "Alta Absorção",
                           "Homens", "Natural",
                           "Vegetais", "Mulheres", "Abelha", "Parede", "Animal", "por", "Dia", "Dosagem", "Dupla",
                           "Vegetariana", "UI", "Alta", "Absorção", "kg", "lbs", "Unhas", "Perdas",
                           "Cabelos", "Pele", "Suplementos",
                           "Vegetarianas", "Life", "Animal",
                           "Gelatina", "Rápida", "Formato",
                           "Uma Vez", "Comprimidos", "Goma", "Vez", "Memória", "Uma", "Extrato",
                           "Dosagem Dupla", "Bilhões", "à", "de", "Juba", "Completo", "Liberação",
                           ])

         # Step 1 and 2: WordCloud's generate function will do the tokenization and frequency counting
         wordcloud = WordCloud(width = 800, height = 800, 
                        background_color ='white', 
                        stopwords = stopwords, 
                        min_font_size = 10).generate(text_produto_concat) 

         # Step 3: Generate the word cloud
         plt.figure(figsize = (8, 8), facecolor = None) 
         plt.imshow(wordcloud) 
         plt.axis("off") 
         plt.tight_layout(pad = 0)

         # Displaying the plot in Streamlit
         st.pyplot(plt)

      # elif opcao2 == 'Produtos - Frequência':
      #    def create_wordcloud(text_produto_concat):
      #       # remove stop words and generate word frequency
      #       word_tokens = word_tokenize(text_produto_concat)
      #       filtered_words = [word for word in word_tokens if word not in stopwords]
      #       word_freq = nltk.FreqDist(filtered_words)
            
      #       # Create a WordCloud object
      #       wordcloud = WordCloud(width=1600, height=800, background_color="white", max_words=1000, contour_width=3, contour_color='steelblue', collocations=False)
            
      #       # Generate a word cloud from frequency
      #       wordcloud.generate_from_frequencies(word_freq)

      #       # Save the word cloud to a PIL image
      #       return wordcloud.to_array()

      #    # Displaying the plot in Streamlit
      #    wordcloud_image = create_wordcloud(text_produto_concat)
      #    st.image(wordcloud_image, use_column_width=True)

