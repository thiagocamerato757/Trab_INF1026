# -*- coding: utf-8 -*-
"""
    nome dos integrantes do grupo:
    - Thiago Pereira Camerato - 2212580 33B
    - Felipe Benevolo Rieken Pinto - 2110368 33B
    - Hugo Da Silva Freires - 2321223 33B
    -
"""
import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt

# Carrega os dados do arquivo CSV
df = pd.read_csv('Airbnb_Open_Data.csv')

# Remove a coluna 'license' do DataFrame
df.drop('license', axis=1, inplace=True)

# Remove a coluna 'house_rules' do DataFrame
df.drop('house_rules', axis=1, inplace=True)

# Remove as colunas 'id', 'host id', 'host name' e 'host_identity_verified' do DataFrame
df.drop(['id', 'host name', 'host_identity_verified'], axis=1, inplace=True)

# Remove as colunas 'country' e 'country code' do DataFrame
df.drop(['country', 'country code'], axis=1, inplace=True)

# Remove a coluna 'last review' do DataFrame
df.drop(['last review'], axis=1, inplace=True)

# Converte a coluna 'price' de string para float, removendo os caracteres '$' e ','
df['price'] = df['price'].str.replace('$', '').str.replace(',', '').astype('float64')

# Converte a coluna 'service fee' de string para float, removendo os caracteres '$' e ','
df['service fee'] = df['service fee'].str.replace('$', '').str.replace(',', '').astype('float64')

# Filtra o DataFrame para incluir apenas linhas onde 'minimum nights' é maior ou igual a 0
df = df[df['minimum nights'] >= 0]

# Filtra o DataFrame para incluir apenas linhas onde 'availability 365' é maior ou igual a 0
df = df[df['availability 365'] >= 0]

df['neighbourhood group'] = df['neighbourhood group'].replace({'brookln': 'Brooklyn'})

# Preenche valores ausentes na coluna 'price' com 0
df['price'] = df['price'].fillna(0.0)

print("\n-----------------------------------------------------")
print("\n 1. Qual é o valor médio de uma diária por room type e neighbourhood group?\n")

# Sumarização 7B: Média do preço agrupada por 'room type' e 'neighbourhood group'
media_preco = df.groupby(['room type', 'neighbourhood group'])['price'].mean().unstack()
print(media_preco)

# Gráfico 6A: Gráfico de barras comparando o preço médio por tipo de quarto em cada bairro
media_preco.plot(kind='bar', figsize=(13, 15), title='Preço médio por tipo de quarto e bairro')
plt.xlabel('Tipo de Quarto')
plt.ylabel('Preço Médio')
plt.show()

print("\n-----------------------------------------------------")
print("\n 2. Qual é a distribuição de avaliações dos hosts por número de propriedades?\n")
# Tabela de frequência 5A: Tabela com a frequência absoluta da quantidade de propriedades por host
frequencia_propriedades_por_host = df['host id'].value_counts()
print(frequencia_propriedades_por_host)

# Sumarização 7C: Agrupamento por 'host id' e análise da média de 'review rate number' e 'calculated host listings count'
agrupamento_host = df.groupby('host id').agg({
    'review rate number': 'mean',
    'calculated host listings count': 'mean'
})
print(agrupamento_host)

# Gráfico 6B: Histograma ou gráfico de densidade da distribuição de avaliações dos hosts
plt.figure(figsize=(10, 6))
agrupamento_host['review rate number'].plot(kind='hist', bins=30, density=True, alpha=0.6, color='g')
agrupamento_host['review rate number'].plot(kind='kde', color='r')
plt.title('Distribuição de Avaliações dos Hosts')
plt.xlabel('Número de Avaliações')
plt.ylabel('Densidade')
plt.show()

print("\n-----------------------------------------------------")
print("\n-----------------------------------------------------")
print("\n 3. Quais bairros possuem a maior e menor disponibilidade média de dias no ano?")
print("\n-----------------------------------------------------")
print("\n-----------------------------------------------------")
print("\n 4. Existe uma correlação entre a política de cancelamento e a taxa de avaliações mensais?")
print("\n-----------------------------------------------------")
print("\n-----------------------------------------------------")
print("\n 5. Como o preço é distribuído entre os diferentes anos de construção das propriedades?\n")


df['Decada Construcao'] = pd.cut(df['Construction year'], bins=[df['Construction year'].min(), 2010, 
                                           2020, df['Construction year'].max()], 
                                     labels=['2000', '2010', '2020'], include_lowest=True)

crossDecadaComRoomType = pd.crosstab(index=df['Decada Construcao'],
                                     columns=df['room type'],
                                     values=df['price'],
                                     aggfunc='mean')

print(crossDecadaComRoomType)
crossDecadaComRoomType.plot.bar(title='Distribuição de preço médio por tipo de quarto por década')
plt.show()

print("\n-----------------------------------------------------")
print("\n-----------------------------------------------------")
print("\n 6. Quais bairros possuem mais listagens com reserva instantânea?\n")

filtroInstantBookable = df.loc[df['instant_bookable'] == True]
instantBookablePorBairro = filtroInstantBookable.groupby('neighbourhood')['instant_bookable'].value_counts()

crossInstantBookableNeighbourhoodGroup = pd.crosstab(index=filtroInstantBookable['instant_bookable'],
                                                    columns=filtroInstantBookable['neighbourhood group'])

print(crossInstantBookableNeighbourhoodGroup)

print("\n-----------------------------------------------------")
print("\n-----------------------------------------------------")