# -*- coding: utf-8 -*-
"""
    Nome dos integrantes do Grupo 7:
    - Bruno Miksucas Pimenta - 2110717 33B
    - Thiago Pereira Camerato - 2212580 33B
    - Felipe Benevolo Rieken Pinto - 2110368 33B
    - Hugo Da Silva Freires - 2321223 33B
    -
"""

import pandas as pd
import matplotlib.pyplot as plt

# Carrega os dados do arquivo CSV
print("Carregando os dados do arquivo CSV...")
df = pd.read_csv('Airbnb_Open_Data.csv', low_memory=False)

# Remove a coluna 'license' do DataFrame
print("Removendo a coluna 'license'...")
df.drop('license', axis=1, inplace=True)

# Remove a coluna 'house_rules' do DataFrame
print("Removendo a coluna 'house_rules'...")
df.drop('house_rules', axis=1, inplace=True)

# Remove as colunas 'id', 'host id', 'host name' e 'host_identity_verified' do DataFrame
print("Removendo as colunas 'id', 'host name' e 'host_identity_verified'...")
df.drop(['id', 'host name', 'host_identity_verified'], axis=1, inplace=True)

# Remove as colunas 'country' e 'country code' do DataFrame
print("Removendo as colunas 'country' e 'country code'...")
df.drop(['country', 'country code'], axis=1, inplace=True)

# Remove a coluna 'last review' do DataFrame
print("Removendo a coluna 'last review'...")
df.drop(['last review'], axis=1, inplace=True)

# Converte a coluna 'price' de string para float, removendo os caracteres '$' e ','
print("Convertendo a coluna 'price' de string para float...")
df['price'] = df['price'].str.replace('$', '').str.replace(',', '').astype('float64')

# Converte a coluna 'service fee' de string para float, removendo os caracteres '$' e ','
print("Convertendo a coluna 'service fee' de string para float...")
df['service fee'] = df['service fee'].str.replace('$', '').str.replace(',', '').astype('float64')

# Filtra o DataFrame para incluir apenas linhas onde 'minimum nights' é maior ou igual a 0
print("Filtrando o DataFrame para incluir apenas linhas onde 'minimum nights' é maior ou igual a 0...")
df = df[df['minimum nights'] >= 0]

# Filtra o DataFrame para incluir apenas linhas onde 'availability 365' é maior ou igual a 0
print("Filtrando o DataFrame para incluir apenas linhas onde 'availability 365' é maior ou igual a 0...")
df = df[df['availability 365'] >= 0]

# Corrige o nome do bairro 'brookln' para 'Brooklyn'
print("Corrigindo o nome do bairro 'brookln' para 'Brooklyn'...")
df['neighbourhood group'] = df['neighbourhood group'].replace({'brookln': 'Brooklyn'})

# Preenche valores ausentes na coluna 'price' com 0
print("Preenchendo valores ausentes na coluna 'price' com 0...")
df['price'] = df['price'].fillna(0.0)

# Preenche valores ausentes na coluna 'review rate number' com a moda
print("Preenchendo valores ausentes na coluna 'review rate number' com a moda...")
moda_review_rate = df['review rate number'].mode()[0]
df['review rate number'] = df['review rate number'].fillna(moda_review_rate)

print("\n-----------------------------------------------------")
print("\n 1. Qual é o valor médio de uma diária por room type e neighbourhood group?\n")

# Sumarização 7B: Média do preço agrupada por 'room type' e 'neighbourhood group'
print("Calculando a média do preço agrupada por 'room type' e 'neighbourhood group'...")
media_preco = df.groupby(['room type', 'neighbourhood group'])['price'].mean().unstack()
print(media_preco)

# Gráfico 6A: Gráfico de barras comparando o preço médio por tipo de quarto em cada bairro
print("Gerando gráfico de barras comparando o preço médio por tipo de quarto em cada bairro...")
media_preco.plot(kind='bar', figsize=(13, 15), title='Preço médio por tipo de quarto e bairro')
plt.xlabel('Tipo de Quarto')
plt.ylabel('Preço Médio')
plt.show()

print("\n-----------------------------------------------------")
print("\n 2. Qual é a distribuição de avaliações dos hosts por número de propriedades?\n")

# Tabela de frequência 5A: Tabela com a frequência absoluta da quantidade de propriedades por host
print("Criando tabela de frequência com a quantidade de propriedades por host...")
frequencia_propriedades_por_host = df['host id'].value_counts()
print(frequencia_propriedades_por_host)

# Sumarização 7C: Agrupamento por 'host id' e análise da média de 'review rate number' e 'calculated host listings count'
print("Agrupando por 'host id' e analisando a média de 'review rate number' e 'calculated host listings count'...")
agrupamento_host = df.groupby('host id').agg({
    'review rate number': 'mean',
    'calculated host listings count': 'mean'
})
print(agrupamento_host)

# Gráfico 6B: Histograma ou gráfico de densidade da distribuição de avaliações dos hosts
print("Gerando histograma e gráfico de densidade da distribuição de avaliações dos hosts...")
plt.figure(figsize=(10, 6))
agrupamento_host['review rate number'].plot(kind='hist', bins=30, density=True, alpha=0.6, color='g')
agrupamento_host['review rate number'].plot(kind='kde', color='r')
plt.title('Distribuição de Avaliações dos Hosts')
plt.xlabel('Número de Avaliações')
plt.ylabel('Densidade')
plt.show()

print("\n-----------------------------------------------------")
print("\n 3. Quais bairros possuem a maior e menor disponibilidade média de dias no ano?")
# Quesito 7A: Sumarização Geral
# Quesito 7B: Sumarização com Grupos simples
# Quesito 4A: Filtro por valor
# Verificando existência de valores acima de 365, que não deveriam existir e tendenciariam as médias
max_dias_disponiveis = df['availability 365'].max()
print('Valor máximo na tabela de dias disponíveis em um ano de um airbnb:', max_dias_disponiveis)
df = df[df['availability 365'] <= 365]
agrupamento_bairro = df.groupby('neighbourhood').agg({'availability 365': 'mean'})
print(agrupamento_bairro.sort_values(by='availability 365'))
print('Bairro com maior disponibilidade média:', agrupamento_bairro.idxmax().values)
print('Bairro com menor disponibilidade média:', agrupamento_bairro.idxmin().values)
print("\n-----------------------------------------------------")
print("\n-----------------------------------------------------")
print("\n 4. Existe uma correlação entre a política de cancelamento e a taxa de avaliações mensais?")
# Quesito 1: Duas estratégias de preenchimento de valores ausentes na coluna 'review rate number'
# Estratégia 1: Substituir valores ausentes por 0
df['review rate number fill_0'] = df['review rate number'].fillna(0)

# Estratégia 2: Substituir valores ausentes pela média de 'review rate number' agrupada por 'cancellation_policy'
df['review rate number fill_policy_mean'] = df.groupby('cancellation_policy')['review rate number'].transform(lambda x: x.fillna(x.mean()))

# Quesito 3B: Criar categorias para 'review rate number' em faixas definidas
# Definimos categorias para simplificar a análise (baixa, média, alta taxa de avaliação)
df['review_rate_category'] = pd.cut(df['review rate number'], bins=[0, 2, 4, 5], labels=['Baixa', 'Média', 'Alta'])

# Quesito 7C: Agrupamento estruturado por 'cancellation_policy' e 'review rate number'
# Calculamos a média da 'review rate number' para cada política de cancelamento
agrupamento_cancelamento_avaliacoes = df.groupby('cancellation_policy')['review rate number'].mean()
print("Média de avaliações mensais por política de cancelamento:")
print(agrupamento_cancelamento_avaliacoes)
print("Logo percebemos que não tem correlação entre avaliações mensais e politica de cancelamento")

# Visualização da média de avaliações mensais por política de cancelamento
agrupamento_cancelamento_avaliacoes.plot(kind='bar', color='skyblue', figsize=(10, 6),
                                         title='Média de Avaliações Mensais por Política de Cancelamento')
plt.xlabel('Política de Cancelamento')
plt.ylabel('Média de Avaliações Mensais')
plt.show()

# Quesito 8A: Cruzamento entre 'review_rate_category' e 'cancellation_policy' para frequência de avaliações em cada política
cross_review_rate_cancel_policy = pd.crosstab(df['review_rate_category'], df['cancellation_policy'])
print("Cruzamento entre categorias de taxa de avaliação e política de cancelamento:")
print(cross_review_rate_cancel_policy)

# Visualização do cruzamento para comparar a frequência das categorias de avaliação para cada política
cross_review_rate_cancel_policy.plot(kind='bar', stacked=True, figsize=(10, 6),
                                     title='Frequência de Avaliações por Categoria e Política de Cancelamento')
plt.xlabel('Categoria de Taxa de Avaliação')
plt.ylabel('Frequência')
plt.show()
print("\n-----------------------------------------------------")
print("\n-----------------------------------------------------")
print("\n 5. Como o preço é distribuído entre os diferentes anos de construção das propriedades?\n")

print("Criando coluna 'Decada Construcao' com base no ano de construção...")
df['Decada Construcao'] = pd.cut(df['Construction year'], bins=[df['Construction year'].min(), 2010,
                                           2020, df['Construction year'].max()],
                                     labels=['2000', '2010', '2020'], include_lowest=True)

print("Criando tabela cruzada com a média de preço por tipo de quarto e década de construção...")
crossDecadaComRoomType = pd.crosstab(index=df['Decada Construcao'],
                                     columns=df['room type'],
                                     values=df['price'],
                                     aggfunc='mean')

print(crossDecadaComRoomType)
print("Gerando gráfico de barras da distribuição de preço médio por tipo de quarto por década...")
crossDecadaComRoomType.plot.bar(title='Distribuição de preço médio por tipo de quarto por década')
plt.show()

print("\n-----------------------------------------------------")
print("\n 6. Quais bairros possuem mais listagens com reserva instantânea?\n")

print("Filtrando listagens com reserva instantânea...")
filtroInstantBookable = df.loc[df['instant_bookable'] == True]
print("Agrupando listagens com reserva instantânea por bairro...")
instantBookablePorBairro = filtroInstantBookable.groupby('neighbourhood')['instant_bookable'].value_counts()

print("Criando tabela cruzada de listagens com reserva instantânea por grupo de bairro...")
crossInstantBookableNeighbourhoodGroup = pd.crosstab(index=filtroInstantBookable['instant_bookable'],
                                                    columns=filtroInstantBookable['neighbourhood group'])

print(crossInstantBookableNeighbourhoodGroup)

print("\n-----------------------------------------------------")
# Requisito 4C: Filtro Composto
# Requisito 8C: Cruzamento de colunas estruturado
print("\n 7. Qual a distribuição da data de construção de casas/apt em Chinatown? A data tem relação forte com a avaliação dessas hospedagens?")
df_neighbourhood_id = df.set_index('neighbourhood')
casas_apt_chinatown =df_neighbourhood_id[(df_neighbourhood_id.index == 'Chinatown') & (df_neighbourhood_id['room type'] == 'Entire home/apt')]
cross_chinatown_ano_review = pd.crosstab(index = casas_apt_chinatown['room type'],
                                  columns = [casas_apt_chinatown['Decada Construcao'], casas_apt_chinatown['review rate number']])
print(cross_chinatown_ano_review)
print("\n-----------------------------------------------------")
# Requisito 5B: Tabela de frequência com valores percentuais
print("\n 8. Qual o percentual de cada tipo de hospedagem?")
percentual_tipo_hospedagem = df['room type'].value_counts(normalize=True)*100
print(percentual_tipo_hospedagem)
print("\n-----------------------------------------------------")
print("\n 9. A faixa de preço influencia na review?")
# Requisito 3B: Categorias com min e max
# Requisito 8D: Cruzamento de colunas simples
df['price category'] = pd.cut(df['price'], bins=[df['price'].min(), 250, 450, 650, 850, df['number of reviews'].max()],
                                          labels=['MB', 'B', 'N', 'C', 'MC'], include_lowest = True)
cross_numreviews_reviewvalues = pd.crosstab(index = df['review rate number'],
                                            columns = df['price category'])
print(cross_numreviews_reviewvalues)
print("\n-----------------------------------------------------")