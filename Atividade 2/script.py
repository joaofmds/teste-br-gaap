import os
import json 
import psycopg2
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host = os.environ.get("DB_HOST"),
    user = os.environ.get("DB_USER"),
    password = os.environ.get("DB_PASS"),
    dbname = os.environ.get("DB_NAME")
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM usuarios")
data = cursor.fetchall()
conn.close()

URL = os.environ.get("URL")
COSMOS_KEY = os.environ.get("COSMOS_KEY")

client = CosmosClient(url=URL, credential=COSMOS_KEY)
database = client.create_database_if_not_exists(id="sipef")
container_client = database.create_container_if_not_exists(
    id="financeiro", 
    partition_key=PartitionKey(path="/logs"), 
    offer_throughput=400
)

def map_fields(row):
    mapped_fields = {}
    
    mapped_fields["nome"] = row[1]
    mapped_fields["email"] = row[2]
    mapped_fields["idade"] = row[3]
    
    return mapped_fields

for row in data:
    
    mapped_fields = map_fields(row)
    mapped_fields["id"] = json.dumps(row[0])
    container_client.create_item(mapped_fields)


