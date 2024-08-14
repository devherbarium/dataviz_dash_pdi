import streamlit as st
import numpy as np
import pandas as pd

# Define o estilo padrão para todo o texto
default_style = """
    <style>
        body {
            font-family: Arial;
            font-size: 20px;
            text-align: justify;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #556B2F;
            font-family: Arial;
            font-size: 20px;
        }
    </style>
"""

# Renderiza o estilo padrão
st.markdown(default_style, unsafe_allow_html=True)

def Sobre():

   st.markdown('## <span style="color:#2F4F4F"><left> Olá, seja bem-vindo à página inicial! </left> </span>', unsafe_allow_html=True) # Título da página
   st.markdown(''' --- ''')

   st.markdown('### <span style="color:#66CDAA"> A Ferramenta </span>', unsafe_allow_html=True) # Subtítulo
   st.markdown(
       """
Esse Dashboard Streamlit foi elaborado para visualização das informações obtidas no projeto de
'Mineração de Dados para o Desenvolvimento de Novos Produtos de Saúde' desenvolvido pela equipe do HUB de IA do SENAI
para a empresa Herbarium, durante as sprints desenvolvidas ao longo do ano e finalizado na sprint 4.
""", unsafe_allow_html=True)

   st.markdown('### <span style="color:#66CDAA"> Contextualização </span>', unsafe_allow_html=True) # Subtítulo
   st.markdown("""
Nesse projeto, vamos analisar os sites da lista de prospecção compartilhada pela empresa Herbarium. 
A proposta da Herbarium é manter-se atualizada com relação às tendências mercadológicas,
obtendo acesso ao lançamento de produtos, atualização de patentes aprovadas e mineração de informações
relevantes para medicamentos fitoterápicos, cosmetológicos, aromaterapia, produtos para infusão e suplementos alimentares, que são os seus produtos chave.
Atualmente, o controle e acompanhamento desses pontos são feitos manualmente e a intenção é automatizar o processo.
O objetivo dessa sprint é aprimorar o scraping e a ferramenta de visualização de dados desenvolvida anteriormente,
além disso verificar a possibilidade de implementação de alguma técnica de machine learning.
""", unsafe_allow_html=True)
   

   

    # Adicionar imagem
#st.image("/home/hub/projetos_hub/herbarium/sprint_2/Entrega_Final/Codigos/0-Dashboard/Imagens/senai-logo.png", width=150)
