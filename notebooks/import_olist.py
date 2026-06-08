import pandas as pd
from sqlalchemy import create_engine

# Conectar ao MySQL com SQLAlchemy
engine = create_engine("mysql+pymysql://root:nova_senha@localhost/olist_dataset")

# Carregar o CSV
df = pd.read_csv(r"C:\Users\alan_\OneDrive\Área de Trabalho\olist_analise\dados\olist_final.csv")

# Importar para o MySQL
df.to_sql('olist_final', engine, if_exists='replace', index=False)

print("Importado com sucesso!")