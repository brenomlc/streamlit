import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

df_survey = pd.read_csv("dados/survey_results_public.csv")

"""
# Python para Ciência de Dados
## Trabalho de streamlit\n
Breno Marques Lomasso Costa
"""

"#### 1- Porcentagem das pessoas que responderam que se consideram profissionais, não profissionais, estudante, hobby, ...."

st.code(language='python', body="""df_survey['MainBranch'].value_counts(normalize=True).mul(100).round(2)""")
df_emp = df_survey['MainBranch'].value_counts(normalize=True).mul(100).round(2)
st.bar_chart(df_emp)
st.write("Como podemos visualizar no gráfico de barras acima, a maior "
         "parte das pessoas (69.7%) são desenvolvedores profissionais.")

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

st.code(language='python', body="""df_survey['EdLevel'].value_counts(normalize=True).mul(100).round(2).rename_axis('EdLevel').reset_index(name='counts')""")
df_ed_level = df_survey['EdLevel'].value_counts(normalize=True).mul(100).round(2).rename_axis('EdLevel').reset_index(name='counts')
pizza = px.pie(df_ed_level, values='counts', names='EdLevel', title='Nível de educação dos entrevistados')
pizza

"""---"""

"#### 4- Qual a distribução de tempo de trabalho para cada tipo de profissional respondido na questão 1."

formacoes = df_survey['MainBranch'].explode().unique()
for formacao in formacoes:
    st.write(formacao)
    df_temp = df_survey[['MainBranch', 'YearsCode']].loc[df_survey['MainBranch'] == formacao]
    df_temp['YearsCode'].replace(to_replace="Less than 1 year", value=0, inplace=True)
    df_temp['YearsCode'].replace(to_replace="More than 50 years", value=51, inplace=True)
    df_temp.dropna(inplace=True)
    df_temp.YearsCode = pd.to_numeric(df_temp.YearsCode, errors='coerce')
    df_temp = df_temp.groupby(pd.cut(df_temp['YearsCode'], np.arange(0, 51, 10))).count()
    df_temp['YearsCode']

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
