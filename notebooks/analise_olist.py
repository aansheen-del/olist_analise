import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#carregar dados

df_orders = pd.read_csv(r"C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\dados\olist_orders_dataset.csv")
df_orders['order_delivered_customer_date'] = pd.to_datetime(df_orders['order_delivered_customer_date'])
df_orders['order_estimated_delivery_date'] = pd.to_datetime(df_orders['order_estimated_delivery_date'])
print(df_orders.info())

atraso = df_orders['order_delivered_customer_date'] - df_orders['order_estimated_delivery_date']
df_orders['atraso'] = atraso
df_orders['atraso_dias'] = df_orders['atraso'].dt.days
print(df_orders['atraso_dias'].head(10))

analise_atraso = df_orders['atraso_dias'].describe()
print(analise_atraso)
pedidos_atrasados = df_orders[df_orders['atraso_dias'] > 0]
print(len(pedidos_atrasados))


#carregar tabela de clientes e fazer join com pedidos atrasados
df_customers = pd.read_csv(r"C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\dados\olist_customers_dataset.csv")
print(df_customers.info())

df_merged = pd.merge(df_orders, df_customers, on='customer_id')
print(df_merged.info())

#agrupar pedidos atrasados por estado
atraso_por_estado = df_merged[df_merged['atraso_dias'] > 0].groupby('customer_state').size()
print(atraso_por_estado.sort_values(ascending=False))
pedidos_por_estado = df_merged.groupby('customer_state').size()
print(pedidos_por_estado)
porcentagem_atraso = (atraso_por_estado / pedidos_por_estado) * 100
print(porcentagem_atraso.sort_values(ascending=False))

#grafico de barras para visualizar a porcentagem de pedidos atrasados por estado
porcentagem_atraso = porcentagem_atraso.sort_values(ascending=True)
plt.figure(figsize=(12, 6))
plt.barh(porcentagem_atraso.index, porcentagem_atraso.values)
plt.title('Porcentagem de pedidos atrasados por estado')
plt.xlabel('Porcentagem dos pedidos com atraso (%)')
plt.ylabel('Estado')
plt.savefig(r'C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\graficos\porcentagem_pedidos_atrasados_estados.png')
plt.close()

#carregar reviews e fazer join com pedidos atrasados
df_reviews = pd.read_csv(r"C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\dados\olist_order_reviews_dataset.csv")
print(df_reviews.info())

df_completo = pd.merge(df_merged, df_reviews, on='order_id')
print(df_completo.info())

media_score_atrasados = df_completo[df_completo['atraso_dias'] > 0]['review_score'].mean()
print(media_score_atrasados)
media_score_no_prazo = df_completo[df_completo['atraso_dias'] <= 0]['review_score'].mean()
print(media_score_no_prazo)

#grafico de barrras mostrando a diferença entre avaliações

categorias = ['Atrasados', 'No prazo']
medias = [media_score_atrasados, media_score_no_prazo]
plt.figure(figsize=(10, 6))
plt.bar(categorias, medias)
plt.title('Média de avaliações pedidos atrasados vs dentro do prazo')
plt.xlabel('Categoria')
plt.ylabel('Média de avaliações')
plt.savefig(r'C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\graficos\media_avaliacoes_atrasados_no_prazo.png')
plt.close()

#carregar tabela de produtos e tabela de items

df_products = pd.read_csv(r'C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\dados\olist_products_dataset.csv')
print(df_products.info())

df_order_items = pd.read_csv(r'C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\dados\olist_order_items_dataset.csv')
print(df_order_items.info())

#merger de produtos
df_items_products = pd.merge(df_order_items, df_products, on='product_id')
df_final = pd.merge(df_items_products, df_completo, on='order_id')
print(df_final.info())

#performance por categoria

media_score_product = df_final.groupby('product_category_name')['review_score'].mean()
print(media_score_product.sort_values(ascending=False))

#grafico de barras horizontal para categoria de produtos melhores avaliados

top10_melhores = media_score_product.sort_values(ascending=False).head(10)
top10_melhores.index = top10_melhores.index.str.replace('_', ' ').str.capitalize()
top10_melhores.index = top10_melhores.index.str[:25]
plt.figure(figsize=(12, 6))
plt.barh(top10_melhores.index, top10_melhores.values)
plt.title('Top 10 categorias de produtos bem avaliados')
plt.xlabel('Reviews da categoria do produto')
plt.ylabel('Categoria do produto')
plt.savefig(r'C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\graficos\top10_melhores.png')
plt.tight_layout()
plt.close()

#grafico de barras horizontal para categoria de produtos mal avaliados

top10_piores = media_score_product.sort_values(ascending=True).head(10)
top10_piores.index = top10_piores.index.str.replace('_', ' ').str.capitalize()
top10_piores.index = top10_piores.index.str[:25]
plt.figure(figsize=(12, 6))
plt.barh(top10_piores.index, top10_piores.values)
plt.title('Top 10 categorias de produtos mal avaliados')
plt.xlabel('Reviews da categoria do produto')
plt.ylabel('Categoria do produto')
plt.savefig(r'C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\graficos\top10_piores.png')
plt.tight_layout()
plt.close()

from matplotlib.gridspec import GridSpec
plt.style.use('default')
fig = plt.figure(figsize=(12, 6))
gs = GridSpec(1, 2, figure=fig, wspace=0.4)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

ax1.barh(top10_melhores.index, top10_melhores.values)
ax1.set_title('Top 10 categorias de produtos bem avaliados')
ax1.set_xlabel('Reviews da categoria do produto')
ax1.set_ylabel('Categoria do produto')
ax1.tick_params(axis='y', labelsize=7)
ax1.tick_params(axis='x', labelsize=7)

ax2.barh(top10_piores.index, top10_piores.values)
ax2.set_title('Top 10 categorias de produtos mal avaliados')
ax2.set_xlabel('Reviews da categoria do produto')
ax2.set_ylabel('')
ax2.tick_params(axis='y', labelsize=7)
ax2.tick_params(axis='x', labelsize=7)

plt.tight_layout()
plt.savefig(r'C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\graficos\top10_piores_melhores.png', dpi=150, bbox_inches='tight')
plt.close()

df_final.to_csv(r'C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\dados\olist_final.csv')

media_categoria = df_final.groupby('product_category_name')['review_score'].mean().reset_index()
media_categoria.columns = ['categoria', 'media_review']
print(media_categoria.head())
media_categoria['media_review'] = media_categoria['media_review'].round(2)
media_categoria.to_csv(r'C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\dados\media_categoria.csv', index=False, decimal=',')