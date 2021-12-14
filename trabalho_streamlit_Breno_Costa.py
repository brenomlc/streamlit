import streamlit as st
import pandas as pd

df_survey = pd.read_csv("dados/survey_results_public.csv")

"""
# Python para Ciência de Dados
## Trabalho de streamlit\n
Breno Marques Lomasso Costa
"""

"#### 1- Porcentagem das pessoas que responderam que se consideram profissionais, não profissionais, estudante, hobby, ...."

st.code(language='python', body="""df_survey.groupby('MainBranch')['MainBranch'].count().rename('Percentage').transform(lambda x: x/x.sum()*100)""")
df_emp = df_survey.groupby('MainBranch')['MainBranch'].count().rename('Percentage').transform(lambda x: x/x.sum()*100)
st.bar_chart(df_emp)
st.write("Como podemos visualizar no gráfico de barras acima, a maior "
         "parte das pessoas (69%) são desenvolvedores profissionais.")

"""---"""

"#### 2- Distribuição das pessoas que responderam por localidade. Qual o país que teve maior participação?"

st.code(language='python', body="""df_survey['Country'].value_counts()""")
df_country = df_survey['Country'].value_counts()
df_country
st.write("O país que teve maior pariticipação foi os EUA, com 15288 pessoas."
         "Seguido da Índia, com 10511 pariticipantes. "
         "Já o Brasil contou com 2254.")

"""---"""

"#### 3- Qual a distribuição nível de estudo dos participantes?"

"""---"""

"#### 4- Qual a distribução de tempo de trabalho para cada tipo de profissional respondido na questão 1."

"""---"""

"#### 5- Das pessoas que trabalham profissionalmente:"
"##### 5.1- qual a profissão delas?"
"##### 5.2- qual a escolaridade?"
"##### 5.3- qual o tamanho das empresas de pessoas que trabalham profissionalmente."

"""---"""

"#### 6- Média salarial das pessoas que responderam."

"""---"""

"#### 7- Pegando os 5 países que mais responderam o questionário, qual é o salário destas pessoas?"

"""---"""

"#### 8- Qual a porcentagem das pessoas que trabalham com python?"

"""---"""

"#### 9- Sobre python:"
"##### 9.1- Qual o nível de salário de quem trabalha com python globalmente?"
"##### 9.2- Para o Brasil, qual o nível salarial?"

"""---"""

"#### 10- Para os 5 países que mais tiveram participação, qual a média salarial?"

"""---"""

"#### 11- De todos as pessoas, Qual o sistema operacional utilizado por elas?"

"""---"""

"#### 12- Das pessoas que trabalham com python, qual a distribuição de sistema operacional utilizado por elas."

"""---"""

"#### 13- Qual a média de idade das pessoas que responderam?"

"""---"""

"#### 14- E em python? Qual a média de idade?"
