# -*- coding: utf-8 -*-
"""
    nome dos integrantes do grupo:
    - Thiago Pereira Camerato - 2212580 33B
    - Felipe Benevolo Rieken Pinto - 2110368 33B
    - Hugo Da Silva Freires - 2321223 33B
    -
"""

print("\n-----------------------------------------------------")
print("\n 1. Qual é o valor médio de uma diária por tipo de quarto e bairro?")
print("\n-----------------------------------------------------")
print("\n-----------------------------------------------------")
print("\n 2. Qual é a distribuição de avaliações dos hosts por número de propriedades?")
print("\n-----------------------------------------------------")
print("\n-----------------------------------------------------")
print("\n 3. Quais bairros possuem a maior e menor disponibilidade média de dias no ano?")
print("\n-----------------------------------------------------")
print("\n-----------------------------------------------------")
print("\n 4. Existe uma correlação entre a política de cancelamento e a taxa de avaliações mensais?")
print("\n-----------------------------------------------------")
print("\n-----------------------------------------------------")
print("\n 5. Como o preço é distribuído entre os diferentes anos de construção das propriedades?")


df['Decada Construcao'] = pd.cut(df['Construction year'], bins=[df['Construction year'].min(), 2010, 
                                           2020, df['Construction year'].max()], 
                                     labels=['2000', '2010', '2020'], include_lowest=True)

crossDecadaComRoomType = pd.crosstab(index=df['Decada Construcao'],
                                     columns=df['room type'],
                                     values=df['price'],
                                     aggfunc='mean')

display(crossDecadaComRoomType)
crossDecadaComRoomType.plot.bar(title='Distribuição de preço médio por tipo de quarto por década')


print("\n-----------------------------------------------------")
print("\n-----------------------------------------------------")
print("\n 6. Quais bairros possuem mais listagens com reserva instantânea?")

filtroInstantBookable = df.loc[df['instant_bookable'] == True]
instantBookablePorBairro = filtroInstantBookable.groupby('neighbourhood')['instant_bookable'].value_counts()

crossInstantBookableNeighbourhoodGroup = pd.crosstab(index=filtroInstantBookable['instant_bookable'],
                                                    columns=filtroInstantBookable['neighbourhood group'])

display(crossInstantBookableNeighbourhoodGroup)

print("\n-----------------------------------------------------")
print("\n-----------------------------------------------------")