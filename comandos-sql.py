import pandas as pd
import sqlite3

# Passo 1: Leia o arquivo Excel usando pandas
file_path = 'clientes.xlsx'
df = pd.read_excel(file_path)

# Passo 2: Conecte-se ao banco de dados SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Passo 3: Insira os dados na tabela clientes
for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO clientes (nome, endereco, telefone, interesse)
        VALUES (?, ?, ?, ?)
    """, (row['Nome'], row['Endereco'], row['Telefone'], row['Interesse']))


# Passo 4: Commit e feche a conexão
conn.commit()
conn.close()


print("Dados inseridos com sucesso!")
