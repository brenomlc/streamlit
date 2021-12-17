import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy import stats
from wordcloud import WordCloud

df_survey = pd.read_csv("dados/survey_results_public.csv")

"""
# Python para Ciência de Dados
## Trabalho de streamlit\n
Breno Marques Lomasso Costa
"""

with st.expander("1- Porcentagem das pessoas que responderam que se consideram profissionais, não profissionais, estudante, hobby, ...."):
    st.code(language='python', body="""df_survey['MainBranch'].value_counts(normalize=True).mul(100).round(2)""")
    df_emp = df_survey['MainBranch'].value_counts(normalize=True).mul(100).round(2)
    st.bar_chart(df_emp)
    st.write("Como podemos visualizar no gráfico de barras acima, a maior "
             "parte das pessoas (69.7%) são desenvolvedores profissionais.")

"""---"""

with st.expander("2- Distribuição das pessoas que responderam por localidade. Qual o país que teve maior participação?"):
    st.code(language='python', body="""df_survey['Country'].value_counts()""")
    df_country = df_survey['Country'].value_counts()
    st.dataframe(df_country)
    st.write("O país que teve maior pariticipação foi os EUA, com 15288 pessoas."
             "Seguido da Índia, com 10511 pariticipantes. "
             "Já o Brasil contou com 2254.")

"""---"""

with st.expander("3- Qual a distribuição nível de estudo dos participantes?"):
    st.code(language='python', body="""df_survey['EdLevel'].value_counts(normalize=True).mul(100).round(2).rename_axis('EdLevel').reset_index(name='counts')""")
    df_ed_level = df_survey['EdLevel'].value_counts(normalize=True).mul(100).round(2).rename_axis('EdLevel').reset_index(name='counts')
    pizza = px.pie(df_ed_level, values='counts', names='EdLevel', title='Nível de educação dos entrevistados')
    pizza

"""---"""

with st.expander("4- Qual a distribução de tempo de trabalho para cada tipo de profissional respondido na questão 1."):
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

with st.expander("5- Das pessoas que trabalham profissionalmente:"):
    "##### 5.1- qual a profissão delas?"
    jobs = ['I am a developer by profession', 'I am not primarily a developer, but I write code sometimes as part of my work']
    selecao = df_survey['MainBranch'].isin(jobs)
    df_jobs = df_survey[selecao]
    df_jobs = df_jobs.Employment.value_counts()
    df_jobs

    "##### 5.2- qual a escolaridade?"
    jobs = ['I am a developer by profession', 'I am not primarily a developer, but I write code sometimes as part of my work']
    selecao = df_survey['MainBranch'].isin(jobs)
    df_jobs = df_survey[selecao]
    df_jobs = df_jobs.EdLevel.value_counts()
    df_jobs

    "##### 5.3- qual o tamanho das empresas de pessoas que trabalham profissionalmente."
    jobs = ['I am a developer by profession', 'I am not primarily a developer, but I write code sometimes as part of my work']
    selecao = df_survey['MainBranch'].isin(jobs)
    df_jobs = df_survey[selecao]
    df_jobs = df_jobs.OrgSize.value_counts()
    df_jobs

"""---"""

with st.expander("6- Média salarial das pessoas que responderam."):
    st.write("Visto que cada pessoa colocou o salário na moeda em que ele ganha, irei fazer a média apenas em dólar,"
             " que foi a cotação mais utilizada pelas pessoas.")
    st.code(language='python', body="""df_survey.Currency.value_counts().nlargest(3)""")
    df_currency = df_survey.Currency.value_counts().nlargest(3)
    df_currency

    df_mean_salary = df_survey.loc[df_survey['Currency'] == 'USD\tUnited States dollar'][['CompFreq', 'CompTotal']].dropna() #Obtem apenas salários em dólar
    df_mean_salary = df_mean_salary[(np.abs(stats.zscore(df_mean_salary['CompTotal'])) < 3)] # Remove valor extremo
    df_mean_salary_year = df_mean_salary.loc[df_mean_salary['CompFreq'] == 'Yearly']['CompTotal'].divide(12) #Transforma salário anual para valor mensal
    df_mean_salary_week = df_mean_salary.loc[df_mean_salary['CompFreq'] == 'Weekly']['CompTotal'].mul(4) #Transforma salário semanal para valor mensal
    df_mean_salary_month = df_mean_salary.loc[df_mean_salary['CompFreq'] == 'Monthly']['CompTotal']
    df_mean_salary = pd.concat([df_mean_salary_year, df_mean_salary_week, df_mean_salary_month])
    st.write("O salário médio mensal dos que ganham em USD é $" + str(round(df_mean_salary.mean(), 2)))

"""---"""

with st.expander("7- Pegando os 5 países que mais responderam o questionário, qual é o salário destas pessoas?"):
    df_top_country_salary = df_survey[['Country', 'CompTotal', 'CompFreq', 'Currency']]
    top_countries = ['United States of America', 'India', 'Germany', 'United Kingdom of Great Britain and Northern Ireland', 'Canada']
    selecao = df_top_country_salary['Country'].isin(top_countries)
    df_top_country_salary = df_top_country_salary[selecao].dropna().sort_values(by='Country').reset_index(drop=True)
    st.write("Salário dos 5 países com mais participantes")
    st.dataframe(df_top_country_salary)

"""---"""

with st.expander("8- Qual a porcentagem das pessoas que trabalham com python?"):
    linguagens = df_survey['LanguageHaveWorkedWith']
    linguagens.dropna(inplace=True)
    counts = 0
    for l in linguagens:
        if 'Python' in l:
            counts += 1

    porcentagem_python = counts / len(df_survey)
    porcentagem_python = "{:.0%}".format(porcentagem_python)

    st.write("A porcentagem dos que usam disseram trabalhar com Python é de " + porcentagem_python)

"""---"""

with st.expander("9- Sobre python:"):
    "##### 9.1- Qual o nível de salário de quem trabalha com python globalmente?"
    df_python = df_survey[['LanguageHaveWorkedWith', 'CompFreq', 'CompTotal', 'Currency']].dropna()
    df_python = df_python[df_python['LanguageHaveWorkedWith'].str.contains('Python')]
    df_python = df_python[df_python['Currency'] == 'USD\tUnited States dollar']
    df_python = df_python[(np.abs(stats.zscore(df_python['CompTotal'])) < 3)]
    df_mean_salary_year = df_python.loc[df_python['CompFreq'] == 'Yearly']['CompTotal'].divide(12) #Transforma salário anual para valor mensal
    df_mean_salary_week = df_python.loc[df_python['CompFreq'] == 'Weekly']['CompTotal'].mul(4) #Transforma salário semanal para valor mensal
    df_mean_salary_month = df_python.loc[df_python['CompFreq'] == 'Monthly']['CompTotal']
    df_mean_salary = pd.concat([df_mean_salary_year, df_mean_salary_week, df_mean_salary_month])
    st.write("O salário médio mensal dos desenvolvedores Python pelo mundo que ganham em USD é $" + str(round(df_mean_salary.mean(), 2)))

    "##### 9.2- Para o Brasil, qual o nível salarial?"
    df_python = df_survey[['LanguageHaveWorkedWith', 'CompFreq', 'CompTotal', 'Country', 'Currency']].dropna()
    df_python = df_python[df_python['LanguageHaveWorkedWith'].str.contains('Python')]
    df_python = df_python[df_python['Country'] == 'Brazil']
    df_python = df_python[df_python['Currency'] == 'BRL\tBrazilian real']
    df_mean_salary_year = df_python.loc[df_python['CompFreq'] == 'Yearly']['CompTotal'].divide(12) #Transforma salário anual para valor mensal
    df_mean_salary_week = df_python.loc[df_python['CompFreq'] == 'Weekly']['CompTotal'].mul(4) #Transforma salário semanal para valor mensal
    df_mean_salary_month = df_python.loc[df_python['CompFreq'] == 'Monthly']['CompTotal']
    df_mean_salary = pd.concat([df_mean_salary_year, df_mean_salary_week, df_mean_salary_month])
    st.write("O salário médio mensal dos desenvolvedores Python no Brasil é R$" + str(round(df_mean_salary.mean(), 2)))

    "##### 9.3 Para os 5 países que mais tiveram participação, qual a média salarial?"
    df_python = df_survey[['LanguageHaveWorkedWith', 'CompFreq', 'CompTotal', 'Country', 'Currency']].dropna()
    df_python = df_python[df_python['LanguageHaveWorkedWith'].str.contains('Python')]
    top_countries = ['United States of America', 'India', 'Germany', 'United Kingdom of Great Britain and Northern Ireland', 'Canada']

    for country in top_countries:
        df_python_country = df_python[df_python['Country'] == country]

        # Pegando a moeda mais usada em cada país. Encontrado através da expressão: #
        # df_top_country_salary[df_top_country_salary['Country'] == *country_name*]['Currency'].value_counts() #
        currency = ''
        if country == 'Canada':
            df_python_country = df_python_country[df_python['Currency'] == 'CAD\tCanadian dollar']
            currency = 'CAD'
        elif country == 'United States of America':
            df_python_country = df_python_country[df_python['Currency'] == 'USD\tUnited States dollar']
            currency = 'USD'
        elif country == 'India':
            df_python_country = df_python_country[df_python['Currency'] == 'INR\tIndian rupee']
            currency = 'INR'
        elif country == 'Germany':
            df_python_country = df_python_country[df_python['Currency'] == 'EUR European Euro']
            currency = 'EUR'
        else:
            df_python_country = df_python_country[df_python['Currency'] == 'GBP\tPound sterling']
            currency = 'GBP'

        df_mean_salary_year = df_python_country.loc[df_python_country['CompFreq'] == 'Yearly']['CompTotal'].divide(12)  # Transforma salário anual para valor mensal
        df_mean_salary_week = df_python_country.loc[df_python_country['CompFreq'] == 'Weekly']['CompTotal'].mul(4)  # Transforma salário semanal para valor mensal
        df_mean_salary_month = df_python_country.loc[df_python_country['CompFreq'] == 'Monthly']['CompTotal']
        df_mean_salary = pd.concat([df_mean_salary_year, df_mean_salary_week, df_mean_salary_month])
        st.write("O salário médio mensal dos desenvolvedores Python no {} é {} {}".format(country,  currency, str(round(df_mean_salary.mean(), 2))))

"""---"""

with st.expander("10- De todos as pessoas, Qual o sistema operacional utilizado por elas?"):
    st.code(body="""df_so = df_survey['OpSys'].dropna().value_counts()""", language='python')
    df_so = df_survey['OpSys'].dropna().value_counts()
    st.dataframe(df_so)

"""---"""

with st.expander("11- Das pessoas que trabalham com python, qual a distribuição de sistema operacional utilizado por elas."):
    st.code(body="""df_so = df_survey[['OpSys', 'LanguageHaveWorkedWith']].dropna()\ndf_so[df_so['LanguageHaveWorkedWith'].str.contains('Python')]['OpSys']""", language='python')
    df_so = df_survey[['OpSys', 'LanguageHaveWorkedWith']].dropna()
    df_so = df_so[df_so['LanguageHaveWorkedWith'].str.contains('Python')]['OpSys'].value_counts()
    st.dataframe(df_so)

"""---"""

with st.expander("12- Qual a média de idade das pessoas que responderam?"):
    st.code(body="""df_age = df_survey['Age'].dropna().value_counts()""", language='python')
    df_age = df_survey['Age'].dropna().value_counts()
    st.dataframe(df_age)

"""---"""

with st.expander("13- E em python? Qual a média de idade?"):
    st.code(body="""df_age = df_survey[['Age', 'LanguageHaveWorkedWith']].dropna()\ndf_age = df_age[df_age['LanguageHaveWorkedWith'].str.contains('Python')]['Age'].value_counts()""", language='python')
    df_age = df_survey[['Age', 'LanguageHaveWorkedWith']].dropna()
    df_age = df_age[df_age['LanguageHaveWorkedWith'].str.contains('Python')]['Age'].value_counts()
    st.dataframe(df_age)

"""---"""

with st.expander("14- Para os 5 países que mais tiveram participação, qual a média salarial?"):
    df_top_country = df_survey[['Country', 'CompTotal', 'CompFreq', 'Currency']]
    top_countries = ['United States of America', 'India', 'Germany', 'United Kingdom of Great Britain and Northern Ireland', 'Canada']
    selecao = df_top_country['Country'].isin(top_countries)
    df_top_country = df_top_country[selecao].dropna()

    for country in top_countries:
        df_top_country_salary = df_top_country[df_top_country['Country'] == country]
        # Pegando a moeda mais usada em cada país. Encontrado através da expressão: #
        # df_top_country_salary[df_top_country_salary['Country'] == *country_name*]['Currency'].value_counts() #
        currency = ''
        if country == 'Canada':
            df_top_country_salary = df_top_country_salary[df_top_country_salary['Currency'] == 'CAD\tCanadian dollar']
            currency = 'CAD'
        elif country == 'United States of America':
            df_top_country_salary = df_top_country_salary[df_top_country_salary['Currency'] == 'USD\tUnited States dollar']
            currency = 'USD'
        elif country == 'India':
            df_top_country_salary = df_top_country_salary[df_top_country_salary['Currency'] == 'INR\tIndian rupee']
            # India está com valores enormes #
            df_top_country_salary = df_top_country_salary[(np.abs(stats.zscore(df_top_country_salary['CompTotal'])) < 3)]
            currency = 'INR'
        elif country == 'Germany':
            df_top_country_salary = df_top_country_salary[df_top_country_salary['Currency'] == 'EUR European Euro']
            currency = 'EUR'
        else:
            df_top_country_salary = df_top_country_salary[df_top_country_salary['Currency'] == 'GBP\tPound sterling']
            currency = 'GBP'

        df_mean_salary_year = df_top_country_salary.loc[df_top_country_salary['CompFreq'] == 'Yearly'].loc[df_top_country_salary['Country'] == country]['CompTotal'].divide(12) #Transforma salário anual para valor mensal
        df_mean_salary_week = df_top_country_salary.loc[df_top_country_salary['CompFreq'] == 'Weekly'].loc[df_top_country_salary['Country'] == country]['CompTotal'].mul(4) #Transforma salário semanal para valor mensal
        df_mean_salary_month = df_top_country_salary.loc[df_top_country_salary['CompFreq'] == 'Monthly'].loc[df_top_country_salary['Country'] == country]['CompTotal']
        df_mean_salary = pd.concat([df_mean_salary_year, df_mean_salary_week, df_mean_salary_month])
        st.write("O salário médio mensal em {} é de {} {}".format(country, currency, str(round(df_mean_salary.mean(), 2))))

"""---"""

with st.expander("15- Frequência de menções das linguagens de programação"):
    linguagens = df_survey['LanguageHaveWorkedWith']
    linguagens.dropna(inplace=True)
    counts = dict()
    for l in linguagens:
        linguagens_list = l.split(';')
        for linguagem in linguagens_list:
            if linguagem in counts:
                counts[linguagem] += 1
            else:
                counts[linguagem] = 1

    wc = WordCloud().fit_words(counts)
    st.image(wc.to_array())
