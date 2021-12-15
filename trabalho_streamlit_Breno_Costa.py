import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy import stats

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
    df_temp = df_survey[['MainBranch', 'YearsCodePro']].loc[df_survey['MainBranch'] == formacao]
    df_temp['YearsCodePro'].replace(to_replace="Less than 1 year", value=0, inplace=True)
    df_temp['YearsCodePro'].replace(to_replace="More than 50 years", value=51, inplace=True)
    df_temp.dropna(inplace=True)
    df_temp.YearsCodePro = pd.to_numeric(df_temp.YearsCodePro, errors='coerce')
    df_temp = df_temp.groupby(pd.cut(df_temp['YearsCodePro'], np.arange(0, 51, 10))).count()
    df_temp['YearsCodePro']

"""---"""

"#### 5- Das pessoas que trabalham profissionalmente:"
"##### 5.1- qual a profissão delas?"
"##### 5.2- qual a escolaridade?"
"##### 5.3- qual o tamanho das empresas de pessoas que trabalham profissionalmente."

"""---"""

"#### 6- Média salarial das pessoas que responderam."

st.write("Visto que cada pessoa colocou o salário na moeda em que ele ganha, irei fazer a média apenas em dólar,"
         " que foi a cotação mais utilizada pelas pessoas.")
st.code(language='python', body="""df_survey.Currency.value_counts().nlargest(3)""")
df_currency = df_survey.Currency.value_counts().nlargest(3)
df_currency

df_mean_salary = df_survey.loc[df_survey['Currency'] == 'USD\tUnited States dollar'][['CompFreq','CompTotal']].dropna() #Obtem apenas salários em dólar
df_mean_salary = df_mean_salary[(np.abs(stats.zscore(df_mean_salary['CompTotal'])) < 3)] # Remove valor extremo
df_mean_salary_year = df_mean_salary.loc[df_mean_salary['CompFreq'] == 'Yearly']['CompTotal'].divide(12) #Transforma salário anual para valor mensal
df_mean_salary_week = df_mean_salary.loc[df_mean_salary['CompFreq'] == 'Weekly']['CompTotal'].mul(4) #Transforma salário semanal para valor mensal
df_mean_salary_month = df_mean_salary.loc[df_mean_salary['CompFreq'] == 'Monthly']['CompTotal']
df_mean_salary = pd.concat([df_mean_salary_year, df_mean_salary_week, df_mean_salary_month])
st.write("A média salarial dos que ganham em USD é $" + str(round(df_mean_salary.mean(), 2)))

## preciso como arrumar esse estouro no float ##

"""---"""

"#### 7- Pegando os 5 países que mais responderam o questionário, qual é o salário destas pessoas?"

"""---"""

"#### 8- Qual a porcentagem das pessoas que trabalham com python?"

df_python = df_survey['LanguageHaveWorkedWith']
df_python.dropna(inplace=True)
#TODO:continuar a mágica

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
