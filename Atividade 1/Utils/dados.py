import psycopg2
import random
import string
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

conn = psycopg2.connect(
    f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"
)

cur = conn.cursor()

num_rows = 50
for i in range(num_rows):
    # Gerando dados aleatórios
    nome = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
    email = nome + "@email.com"
    idade = random.randint(18, 80)

    cur.execute(
        f"INSERT INTO usuarios (nome, email, idade) VALUES ('{nome}', '{email}', {idade})"
    )

conn.commit()
cur.close()
conn.close()

print(f"{num_rows} linhas foram inseridas na tabela com sucesso.")
