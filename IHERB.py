import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from datetime import timedelta
from aux2 import *

storage_account_key = os.getenv("storage_key")
container_name = "pdi-dashboard"
# storage_account_key = read_storage_key('storage_key.txt')
# Defina suas credenciais e o nome do contêiner
storage_account_name = "hlbdatalake"
# Conectar ao BlobServiceClient usando a connection string
connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"

img_path,base_path = img_base_pth()
def IHerb(): 
   # image = Image.open(img_path+'\iHerb-Emblem.png')
   image = (open_img_from_blob(storage_account_key, "\Imagens\iHerb-Emblem.png"))
                    
   st.sidebar.image(image, width=250)                
   
   st.markdown(''' --- ''')

   opcao = st.selectbox ('Escolha a opção desejada:',('Gráficos', 'Word Cloud'))
   
   if opcao == 'Gráficos':
      
      a, b, c, d, e, f, g = st.tabs(['Avaliações','Marca x Categoria', 'Produtos com Desconto x Marca',
                                     'Produtos com Desconto x Categoria', 'Avaliações - Tendência',
                                     'Tendência de Crescimento', 'Variação de Crescimento'])
      
      with a:
         ## Caminho para o arquivo
         caminho_arquivo = os.path.join(base_path,r'8_categorias_iherb.csv')

         # # Carregar dados
         # df = pd.read_csv(caminho_arquivo)
         df = read_csv_from_blob(connection_string, container_name,
                                        "\Base_dados\8_categorias_iherb.csv")

         # Ordenar o DataFrame pela data
         df = df.sort_values('Data')

         st.write('<h3 style="font-size: 20px; color: darkgreen; ">Distribuição de Avaliações x Categoria, Marca e Produto</h3>', unsafe_allow_html=True)

         # Criar controle deslizante para selecionar o número máximo de produtos exibidos
         num_produtos_total = st.slider("Número máximo de produtos exibidos", min_value=1, max_value=df['Produto'].nunique(), value=30)

         # Criar controle deslizante para selecionar o número máximo de produtos por marca
         max_products_per_brand = int(df.groupby('Marca')['Produto'].nunique().max())
         num_produtos_marca = st.slider("Número máximo de produtos por marca", min_value=1, max_value=max_products_per_brand, value=max_products_per_brand)

         # Criar uma nova coluna 'manter_marca' que indica se a marca deve ser mantida ou não
         df['manter_marca'] = df.groupby('Marca')['Produto'].transform(lambda x: x.nunique() <= num_produtos_marca)

         # Filtrar as marcas que têm um número excessivo de produtos
         df = df[df['manter_marca']]

         # Ordenar as marcas pela contagem de produtos e pegar as que têm o maior número de produtos
         marcas_top = df['Marca'].value_counts().index[:num_produtos_total]

         # Filtrar o DataFrame para conter apenas as marcas_top
         df = df[df['Marca'].isin(marcas_top)]

         # Agrupar pelo produto e pegar a linha mais recente para cada grupo
         df = df.groupby(['Categoria', 'Marca', 'Produto']).last().reset_index()

         # Criar o gráfico sunburst
         camadas = ['Categoria', 'Marca', 'Produto']
         valor = 'Avaliações'
         fig = px.sunburst(df, path=camadas, values=valor)

         # Aumentar o tamanho do gráfico
         fig.update_layout(width=1000, height=1000)

         # Renderizar o gráfico
         st.plotly_chart(fig)




      with b: 
         # Caminho para o arquivo
         caminho_arquivo = os.path.join(base_path,'8_categorias_iherb.csv')

         # # Carregar dados
         # produtos = pd.read_csv(caminho_arquivo)
         produtos = read_csv_from_blob(connection_string, container_name,
                                 "\Base_dados\8_categorias_iherb.csv")

         st.write('<h3 style="font-size: 20px; color: darkgreen; ">Marcas x Categoria</h3>', unsafe_allow_html=True)

         # Definir configurações do gráfico
         coluna_categoria = 'Categoria' # Selecionar a coluna para o eixo x
         coluna_marca = 'Marca' # Selecionar a coluna para agrupar nas barras do eixo x
         max_itens = 10 # Definir o número de barras empilhadas (no caso, marcas empilhadas por categoria)

         # Criar o gráfico de barras
         contagem = produtos.groupby(coluna_categoria)[coluna_marca].value_counts().reset_index(name='Contagem')
         contagem = contagem.sort_values(by=['Categoria', 'Contagem'], ascending=[True, False])
         contagem_limitada = contagem.groupby(coluna_categoria).head(max_itens)

         # Define uma sequência de 20 cores diferentes para as marcas
         cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                  '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5']

         fig = px.bar(contagem_limitada, x=coluna_categoria, y='Contagem', color=coluna_marca, color_discrete_sequence=cores)

         # Ajusta a altura e a largura do gráfico
         fig.update_layout(
            autosize=False,
            width=1000,
            height=800,
         )

         # Move a legenda para a parte inferior
         fig.update_layout(legend=dict(
            orientation="v",
            yanchor="top",
            y=-1.08,
            xanchor="right",
            x=0.5
         ))

         # Mostrar o gráfico no Streamlit
         st.plotly_chart(fig)

      with c: 
         # Caminho para o arquivo
         caminho_arquivo = os.path.join(base_path,'8_categorias_iherb.csv')

         # Carregar dados
         # produtos = pd.read_csv(caminho_arquivo)
         produtos = read_csv_from_blob(connection_string, container_name,
                                 "\Base_dados\8_categorias_iherb.csv")

         st.write('<h3 style="font-size: 20px; color: darkgreen; ">Produtos com Desconto x Marca</h3>', unsafe_allow_html=True)

         # Mostrar produtos que possuem preço e preço final. Ou seja, que tenham desconto e preço final não nulo.
         produtos_desconto = produtos[(~produtos['Preço'].isna()) & (~produtos['Preço Final'].isna())]

         # Definir configurações do gráfico
         dados = produtos_desconto
         coluna_categoria = 'Marca' # Selecionar a coluna para o eixo x
         coluna_marca = 'Produto' # Selecionar a coluna para agrupar nas barras do eixo x
         max_itens = 10 # Definir o número de barras empilhadas (no caso, marcas empilhadas por categoria)

         # Criar o gráfico de barras
         contagem = dados.groupby(coluna_categoria)[coluna_marca].value_counts().reset_index(name='Contagem')
         contagem = contagem.sort_values(by=[coluna_categoria, 'Contagem'], ascending=[True, False])
         contagem_limitada = contagem.groupby(coluna_categoria).head(max_itens)

         # Define uma sequência de 20 cores diferentes para as marcas
         cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                  '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5']

         fig = px.bar(contagem_limitada, x=coluna_categoria, y='Contagem', color=coluna_marca, color_discrete_sequence=cores)

         # Ajusta a altura e a largura do gráfico
         fig.update_layout(
            autosize=False,
            width=1000,
            height=800,
         )

         # Move a legenda para a parte inferior
         fig.update_layout(legend=dict(
            yanchor="top",
            y=-1,
            xanchor="center",
            x=0.5
         ))

         # Mostrar o gráfico no Streamlit
         st.plotly_chart(fig)

      with d: 
         # Caminho para o arquivo
         caminho_arquivo = os.path.join(base_path,'8_categorias_iherb.csv')

         # Carregar dados
         # produtos = pd.read_csv(caminho_arquivo)
         produtos = read_csv_from_blob(connection_string, container_name,
                                 "\Base_dados\8_categorias_iherb.csv")


         st.write('<h3 style="font-size: 20px; color: darkgreen; ">Produtos com Desconto x Categoria</h3>', unsafe_allow_html=True)

         # Mostrar produtos que possuem preço e preço final. Ou seja, que tenham desconto e preço final não nulo.
         produtos_desconto = produtos[(~produtos['Preço'].isna()) & (~produtos['Preço Final'].isna())]

         # Definir configurações do gráfico
         dados = produtos_desconto
         coluna_categoria = 'Categoria' # Selecionar a coluna para o eixo x
         coluna_marca = 'Produto' # Selecionar a coluna para agrupar nas barras do eixo x
         max_itens = 5 # Definir o número de barras empilhadas (no caso, marcas empilhadas por categoria)

         # Criar o gráfico de barras
         contagem = dados.groupby(coluna_categoria)[coluna_marca].value_counts().reset_index(name='Contagem')
         contagem = contagem.sort_values(by=[coluna_categoria, 'Contagem'], ascending=[True, False])
         contagem_limitada = contagem.groupby(coluna_categoria).head(max_itens)

         # Define uma sequência de 20 cores diferentes para as marcas
         cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                  '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5']

         fig = px.bar(contagem_limitada, x=coluna_categoria, y='Contagem', color=coluna_marca, color_discrete_sequence=cores)

         # Ajusta a altura e a largura do gráfico
         fig.update_layout(
            autosize=False,
            width=1000,
            height=800,
         )

         # Move a legenda para a parte inferior e centraliza
         fig.update_layout(legend=dict(
            yanchor="top",
            y=-1,
            xanchor="center",
            x=0.5
         ))

         # Mostrar o gráfico no Streamlit
         st.plotly_chart(fig)

      with e:
         # Caminho para o arquivo
         caminho_arquivo = os.path.join(base_path,'8_categorias_iherb.csv')

         # Carregar dados
         # df = pd.read_csv(caminho_arquivo)
         df = read_csv_from_blob(connection_string, container_name,
                                 "\Base_dados\8_categorias_iherb.csv")

         # Ordenar o DataFrame pela data
         df = df.sort_values('Data')

         # Lista de produtos únicos
         produtos = df['Produto'].unique()

         # Selecione um produto específico através de um selectbox
         produto_selecionado = st.selectbox('Selecione um produto:', produtos)

         # Filtrar DataFrame para incluir apenas as avaliações para o produto selecionado
         df_produto = df[df['Produto'] == produto_selecionado]

         # Agrupar por data e calcular a média das avaliações
         df_produto = df_produto.groupby('Data')['Avaliações'].mean().reset_index()

         # Criar um gráfico de linha para as avaliações ao longo do tempo
         fig = px.line(df_produto, x='Data', y='Avaliações', title=f'Tendência das avaliações para o produto {produto_selecionado}')

         # Renderizar o gráfico
         st.plotly_chart(fig)

      with f:
         def convert_date(date_str):
            return date_str.replace(' ', '-').replace('_', '-').replace(':', '-')

         caminho_arquivo = os.path.join(base_path, '8_categorias_iherb.csv')
         #
         # df = pd.read_csv(caminho_arquivo)
         df = read_csv_from_blob(connection_string, container_name,
                                 "\Base_dados\8_categorias_iherb.csv")
         df['Data'] = df['Data'].apply(convert_date)
         df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d-%H-%M-%S')

         # Slider para selecionar o número de dias observados
         num_dias = st.slider("Número de dias observados para avaliação de crescimento de avaliações",
                              min_value=1, max_value=(df['Data'].max() - df['Data'].min()).days, value=30)

         # Filtrar os dados com base no número de dias selecionados
         data_minima = df['Data'].max() - pd.Timedelta(days=num_dias)
         df = df[df['Data'] >= data_minima]

         # Calcular crescimento de avaliações
         df['Crescimento_Avaliações'] = df.groupby('Produto')['Avaliações'].transform(lambda x: x.iloc[-1] - x.iloc[0])

         # Sunburst plot
         camadas = ['Categoria', 'Marca', 'Produto']
         valor = 'Crescimento_Avaliações'
         fig = px.sunburst(df, path=camadas, values=valor)
         fig.update_layout(width=1000, height=1000)
         st.plotly_chart(fig)

         # Tabela classificando produtos por crescimento nas avaliações
         produtos_classificados = df[['Produto', 'Crescimento_Avaliações']].drop_duplicates().sort_values('Crescimento_Avaliações', ascending=False)
         st.table(produtos_classificados.head(10))  # Exibindo apenas os top 10 produtos

         # Selecionar produto através de um dropdown
         selected_product = st.selectbox('Selecione um produto para visualizar o gráfico:', produtos_classificados['Produto'].unique())
         df_product = df[df['Produto'] == selected_product]

         # Calcular a variação de crescimento das avaliações
         df_product['Variação de Crescimento'] = df_product['Avaliações'].diff()

         # Line plot
         fig = px.line(df_product, x='Data', y='Variação de Crescimento', title=f'Variação de Crescimento de Avaliações para {selected_product}')
         st.plotly_chart(fig)

      
      with g:
         # Slider para selecionar a quantidade de dias
         x_days = st.slider('Selecione a quantidade de dias:', min_value=1, max_value=365, value=30)

         # Data atual ou final do período
         end_date = df['Data'].max()

         # Data de início do período (últimos x dias)
         start_date = end_date - timedelta(days=x_days)

         # Filtrar os dados para os últimos x dias
         df_last_x_days = df[(df['Data'] >= start_date) & (df['Data'] <= end_date)]

         # Calcular o crescimento acumulado para cada produto
         growth_accumulated = df_last_x_days.groupby('Produto')['Avaliações'].diff().groupby(df_last_x_days['Produto']).sum().reset_index()

         # Classificar os produtos pelo crescimento acumulado
         ranked_products = growth_accumulated.sort_values(by='Avaliações', ascending=False)

         # Exibir a tabela com o top 10 produtos
         st.write('Top 10 produtos por crescimento acumulado:')
         st.table(ranked_products.head(10))

         # Dropdown para selecionar um produto
         selected_product = st.selectbox('Selecione um produto para visualizar o gráfico:', ranked_products['Produto'])

         # Filtrar o DataFrame original para o produto selecionado
         df_product = df[df['Produto'] == selected_product]

         # Calcular a variação de crescimento
         df_product['Variação de Crescimento'] = df_product['Avaliações'].diff()

         # Line plot
         fig = px.line(df_product, x='Data', y='Variação de Crescimento', title=f'Variação de Crescimento de Avaliações para {selected_product}')
         st.plotly_chart(fig)
 



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
         df_concat = read_csv_from_blob(connection_string, container_name,
                                 "\Base_dados\8_categorias_iherb.csv")

         # Concatenar o texto para a nuvem de palavras
         text_marca_concat = " ".join(review for review in df_concat.Marca)

         # Criar filtro de palavras irrelevantes para a análise pretendida:
         stopwords = set(STOPWORDS)
         stopwords.update(["ml", "fl", "oz", "Sem", "mg", "de", "sem", "e", "sistema", "premium", "classe", "ao", "lb", "g", "mcg", "now", "plus", "pura", "gold", "california", "bioperine", "nutrition", 
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
                           "Vegetariana", "UI", "Alta", "Absorção", "kg", "lbs", "Unhas", "Perdas", "Cabelos", "Pele", "Suplementos",
                           "Vegetarianas", "Life", "Animal",
                           "Gelatina", "Rápida", "Formato",
                           "Uma Vez", "Comprimidos", "Goma", "Vez", "Memória", "Uma", "Extrato", "Dosagem Dupla", "Bilhões", "à", "de", "Juba", "Completo", "Liberação",
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
         df_concat = read_csv_from_blob(connection_string, container_name,
                                 "\Base_dados\8_categorias_iherb.csv")

         # Concatenar o texto para a nuvem de palavras
         text_produto_concat = " ".join(review for review in df_concat.Produto)

         # Criar filtro de palavras irrelevantes para a análise pretendida:
         stopwords = set(STOPWORDS)
         stopwords.update(["ml", "fl", "oz", "Sem", "mg", "de", "sem", "e", "sistema", "premium", "classe", "ao", "lb", "g", "mcg", "now", "plus", "pura", "gold", "california", "bioperine", "nutrition", 
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
                           "Vegetariana", "UI", "Alta", "Absorção", "kg", "lbs", "Unhas", "Perdas", "Cabelos", "Pele", "Suplementos",
                           "Vegetarianas", "Life", "Animal",
                           "Gelatina", "Rápida", "Formato",
                           "Uma Vez", "Comprimidos", "Goma", "Vez", "Memória", "Uma", "Extrato", "Dosagem Dupla", "Bilhões", "à", "de", "Juba", "Completo", "Liberação",
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

