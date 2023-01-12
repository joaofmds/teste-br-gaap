# TESTE TÉCNICO BR GAAP - INFRAESTRUTURA E CLOUD

Para este teste técnico, foram desenvolvidas os seguintes desafios:

- [x] Atividade 1: Automatizar um backup de um banco de dados PostgreSQL  
- [x] Atividade 2: Copiar um banco de dados PostgreSQL para o Azure Cosmos DB

## Atividade 1  
### Automatizar um backup de um banco de dados PostgreSQL 

Para realizar este desafio, criei uma banco de dados com nome, e-mail e idade e desenvolvi um script chamado dados.py (que se encontra dentro de Utils) para popular a tabela com valores aleatórios. 

Após isso, o desenvolvimento do script seguiu esses passos:

1. Conexão com o banco de dados a partir dos dados no arquivo `.env`.
```
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
```
2. Configurações do destinatŕio, remetente, senha, configurações do servidor SMTP e o nome do arquivo de backup.
```
TO = os.environ.get("TO")
FROM = os.environ.get("FROM", "")
FROM_PASS = os.environ.get("FROM_PASS")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = os.environ.get("SMTP_PORT")
BACKUP_FILE = os.environ.get("BACKUP_FILE")
```
3. Comando shell para criar o backup do banco de dados.
```
subprocess.call(
    f"pg_dump -h {DB_HOST} -U {DB_USER} -F t {DB_NAME} -f {BACKUP_FILE}", shell=True
)
```
4. Configurações do e-mail
```
msg = MIMEMultipart()
msg["From"] = FROM
msg["To"] = TO
msg["Subject"] = "Backup do banco de dados"
```
5. Preparação do anexo para ser enviado por e-mail.
```
part = MIMEBase("application", "octet-stream")
part.set_payload(open(BACKUP_FILE, "rb").read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename={BACKUP_FILE}")
msg.attach(part)
```
6. Enviar a mensagem preparada anteriormente via protocolo SMTP e remover o arquivo de backup do diretório local.
```
smtp_obj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
smtp_obj.starttls()
smtp_obj.login(FROM, FROM_PASS)
smtp_obj.sendmail(FROM, TO, msg.as_string())
smtp_obj.quit()

os.remove(BACKUP_FILE)

print("Backup realizado com sucesso e enviado por e-mail.")
```

#### Pré-requisitos para uso

- [x] Subir o banco de dados PotsgreSQL localmente
- [x] Configurar o arquivo `.env` previamente

#### Utilizando o script

No terminal, insira o comando `python script.py`


## Atividade 2
### Copiar um banco de dados PostgreSQL para o Azure Cosmos DB

Para realizar este desafio, utilizei o banco de dados da atividade anterior.

Após isso, o desenvolvimento do script seguiu esses passos:

1. Criar conexão com o banco de dados a partir dos dados no arquivo `.env`.
```
conn = psycopg2.connect(
    host = os.environ.get("DB_HOST"),
    user = os.environ.get("DB_USER"),
    password = os.environ.get("DB_PASS"),
    dbname = os.environ.get("DB_NAME")
)
```
2. Buscar e armazenar os dados de uma tabela de banco de dados em uma lista de tuplas.
```
cursor = conn.cursor()
cursor.execute("SELECT * FROM usuarios")
data = cursor.fetchall()
conn.close()
```
3. Criar conexão com um banco de dados Azure CosmosDB
```
URL = os.environ.get("URL")
COSMOS_KEY = os.environ.get("COSMOS_KEY")

client = CosmosClient(url=URL, credential=COSMOS_KEY)
database = client.create_database_if_not_exists(id="sipef")
container_client = database.create_container_if_not_exists(
    id="financeiro", 
    partition_key=PartitionKey(path="/logs"), 
    offer_throughput=400
)
```
4. Mapear os campos de uma linha de dados para um dicionário de campos.
```
def map_fields(row):
    mapped_fields = {}
    
    mapped_fields["nome"] = row[1]
    mapped_fields["email"] = row[2]
    mapped_fields["idade"] = row[3]
    
    return mapped_fields
```
5. Percorrer uma lista de linhas de dados e inserir cada linha de dados no banco de dados CosmosDB.
```
for row in data:
    
    mapped_fields = map_fields(row)
    mapped_fields["id"] = json.dumps(row[0])
    container_client.create_item(mapped_fields)
```

#### Pré-requisitos para uso

- [x] Subir o banco de dados PotsgreSQL localmente
- [x] Configurar o arquivo `.env` previamente

#### Utilizando o script

No terminal, insira o comando `python script.py`
