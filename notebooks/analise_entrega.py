import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#carregar os dados

tempo_entrega_dataset = pd.read_csv(r'C:\Users\alan_\OneDrive\Área de Trabalho\Olist_analise\dados\olist_final.csv')
tempo_entrega_dataset['order_purchase_timestamp'] = pd.to_datetime(tempo_entrega_dataset['order_purchase_timestamp'])
tempo_entrega_dataset['order_approved_at'] = pd.to_datetime(tempo_entrega_dataset['order_approved_at'])
tempo_entrega_dataset['order_delivered_carrier_date'] = pd.to_datetime(tempo_entrega_dataset['order_delivered_carrier_date'])
tempo_entrega_dataset['order_delivered_customer_date'] = pd.to_datetime(tempo_entrega_dataset['order_delivered_customer_date'])
tempo_entrega_dataset['order_estimated_delivery_date'] = pd.to_datetime(tempo_entrega_dataset['order_estimated_delivery_date'])
print(tempo_entrega_dataset.info())

#calculando tempo de entrega e filtrando tempo de entrega por estado

tempo = tempo_entrega_dataset['order_delivered_customer_date'] - tempo_entrega_dataset['order_purchase_timestamp']
tempo_entrega_dataset['tempo'] = tempo
tempo_entrega_dataset['tempo_dias'] = tempo_entrega_dataset['tempo'].dt.days
print(tempo_entrega_dataset['tempo_dias'].head(10))

tempo_entrega = tempo_entrega_dataset['tempo_dias'].describe()
print(tempo_entrega)
quantidade_entregue = tempo_entrega_dataset[tempo_entrega_dataset['tempo_dias'] > 0]
print(len(quantidade_entregue))

entrega_estado = tempo_entrega_dataset.groupby('customer_state')['tempo_dias'].mean().round().astype(int).sort_values(ascending=False)
print(entrega_estado)

entrega_estado = entrega_estado.sort_values(ascending=True)
plt.figure(figsize=(12, 6))
plt.barh(entrega_estado.index, entrega_estado.values)
plt.title('Média de dias para entrega em cada estado apartir da data de compra')
plt.xlabel('Dias')
plt.ylabel('Estado')
plt.savefig(r'C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\graficos\entrega_estado.png')
plt.close()

#filtrando tempo de entrega por categoria

entrega_categoria = tempo_entrega_dataset.groupby('product_category_name')['tempo_dias'].mean().round().astype(int).sort_values(ascending=False)
print(entrega_categoria)

entrega_categoria_menor = entrega_categoria.sort_values(ascending=True).head(10)
plt.figure(figsize=(12, 6))
plt.barh(entrega_categoria_menor.index, entrega_categoria_menor.values)
plt.title('Categoria de produtos com menor tempo médio de entrega a partir da data de compra')
plt.xlabel('Dias')
plt.ylabel('Categoria')
plt.savefig(r'C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\graficos\entrega_categoria_menor.png')
plt.close()

entrega_categoria_maior = entrega_categoria.sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
plt.barh(entrega_categoria_maior.index, entrega_categoria_maior.values)
plt.title('Categoria de produtos com maior tempo médio de entrega a partir da data de compra')
plt.xlabel('Dias')
plt.ylabel('Categoria')
plt.savefig(r'C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\graficos\entrega_categoria_maior.png')
plt.close()

#contando categorias mais vendidas

quantidade = tempo_entrega_dataset['product_category_name'].value_counts()
#print(quantidade)

limite = quantidade.quantile(0.75)
print(limite)
quantidade_filtrada = quantidade[quantidade > limite]
print(len(quantidade_filtrada))

df_filtrado = tempo_entrega_dataset[tempo_entrega_dataset['product_category_name'].isin(quantidade_filtrada.index)]
quantidade_categoria = df_filtrado.groupby('product_category_name')['tempo_dias'].mean().round().astype(int).sort_values(ascending=False)
print(quantidade_categoria)

quantidade_categoria = quantidade_categoria.sort_values(ascending=True)
plt.figure(figsize=(12, 6))
plt.barh(quantidade_categoria.index, quantidade_categoria.values)
plt.title('Categorias mais relevantes em media de dias de entrega')
plt.xlabel('Dias')
plt.ylabel('Categoria')
plt.savefig(r'C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\graficos\quantidade_dias.png')
plt.show()