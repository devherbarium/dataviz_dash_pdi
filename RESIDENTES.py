import streamlit as st
import numpy as np
import pandas as pd

def Contato():


   st.markdown('## <span style = "color:  #2F4F4F"><center> Time de desenvolvimento HUB de IA </center></span>', unsafe_allow_html = True)
   st.markdown(''' --- ''')

    ################################################
    #################### Início ####################
    ################################################

   st.write(''':green[O dashboard interativo foi desenvolvido pelos residentes Alina Stadinik, Caio Matias e Tamires Brito como parte dos entregáveis das sprints desenvolvidas ao longo do ano e finalizado na sprint 4.
                Para maiores informações sobre cada um ou em caso de dúvidas, basta acessar os links abaixo.]''')

    ##################################################
    #################### Contatos ####################
    ##################################################

   
   st.markdown('## <span style = "color: #2F4F4F"><center> Alina Stadinik </center></span>', unsafe_allow_html = True)

   col_1, col_2, col_3 = st.columns(3)

   with col_1:
        st.components.v1.html('''<a href = "mailto:alina.komarcheuski@sistemafiep.org.br">
                                 <center>
                                 <img src = "https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target = "_blank">
                                 </center>
                                 </a>''',
                                 height = 50)

   with col_2:
        st.components.v1.html('''<a href = "https://www.linkedin.com/in/alina-stadnik-komarcheuski-5aa4b4129" target = "_blank">
                                 <center>
                                 <img src = "https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target = "_blank">
                                 </center>
                                 </a>''',
                                 height = 50)

   with col_3:
        st.components.v1.html('''<a href = "https://github.com/alina-stadnik" target = "_blank">
                                 <center>
                                 <img src = "https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" target = "_blank">
                                 </center>
                                 </a>''',
                                 height = 50)

   
   st.markdown('## <span style = "color: #2F4F4F"><center> Caio Matias </center></span>', unsafe_allow_html = True)

   col_1, col_2, col_3 = st.columns(3)

   with col_1:
        st.components.v1.html('''<a href = "mailto:caiomatias@protonmail.com">
                                 <center>
                                 <img src = "https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target = "_blank">
                                 </center>
                                 </a>''',
                                 height = 50)

   with col_2:
        st.components.v1.html('''<a href = "https://www.linkedin.com/in/caiorm/" target = "_blank">
                                 <center>
                                 <img src = "https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target = "_blank">
                                 </center>
                                 </a>''',
                                 height = 50)

   with col_3:
        st.components.v1.html('''<a href = "https://github.com/caio-matias" target = "_blank">
                                 <center>
                                 <img src = "https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" target = "_blank">
                                 </center>
                                 </a>''',
                                 height = 50)

   st.markdown('## <span style = "color: #2F4F4F"><center> Tamires Brito </center></span>', unsafe_allow_html = True)

   col_1, col_2, col_3 = st.columns(3)

   with col_1:
        st.components.v1.html('''<a href = "mailto:tamires.brito10@gmail.com">
                                        <center>
                                        <img src = "https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target = "_blank">
                                        </center>
                                        </a>''',
                                        height = 50)

   with col_2:
        st.components.v1.html('''<a href = "https://www.linkedin.com/in/tamiresbrito/" target = "_blank">
                                        <center>
                                        <img src = "https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target = "_blank">
                                        </center>
                                        </a>''',
                                        height = 50)

   with col_3:
        st.components.v1.html('''<a href = "https://github.com/tamiressbrito" target = "_blank">
                                        <center>
                                        <img src = "https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" target = "_blank">
                                        </center>
                                        </a>''',
                                        height = 50)
        


