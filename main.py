from typing import Union
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pymysql.cursors
import csv
import json

app = FastAPI()

# ------------ Lectura de CSV -------------

# Archivos CSV almacenados en raiz
file1 = 'organization_and_zones_dataset.csv'
file2 = 'timeseries_dataset.csv'

# Funcion para leer la data CSV y retornarla como JSON
def csv_to_json(csv_file):
    data = []  

    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        for row in csv_reader:
            data.append(row)
    
    json_data = json.dumps(data, indent=4)
    return json_data

# Llamamos la funcion de acuerdo al archivo CSV
json_data1 = csv_to_json(file1)
json_data2 = csv_to_json(file2)

# ------------ Lectura de JSON -------------

# Archivo JSON de GeoJSON almacenado en raiz
json_file = 'example_polygon.json'

# Funcion para leer JSON desde archivo
def read_json_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

# Llamamos la funcion utilizando el archivo JSON
json_data3 = read_json_file(json_file)

# ------------ Lectura de BD ---------------

# Creamos una conexion para MySQL database
connection = pymysql.connect(
    host='127.0.0.1', # Se utiliza una BD Local
    port=3306,  
    user='root',
    password='',
    database='test_bloom',
    cursorclass=pymysql.cursors.DictCursor
)

# Definimos un modelo para la Data
class Organization(BaseModel):
    id: int
    organization: str
    zone_id: int
    zone: str
    polygon_decoded: str

class DataSet(BaseModel):
    id: int
    timestamp: str
    variable: str
    organization: str
    value: float
    ingestion_time: str

# ------------ Configuraciones -------------

# Configuracion de CORS
origins = ["*"]  # Permitimos conexiones de cualquier origen para esta prueba

# Habilitamos CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ---------- EndPoints --------------

# Entrega los datos rescatados de "organization_and_zones_dataset.csv"
@app.get("/organizations")
def read_organizations():
    return Response(content=json_data1, media_type="application/json")

# Entrega los datos rescatados de "timeseries_dataset.csv"
@app.get("/dataset")
def read_dataset():
    return Response(content=json_data2, media_type="application/json")

# Entrega el JSON cargado desde "'example_polygon.json"
@app.get("/geo")
def read_geo():
    return json_data3    

# Entrega los datos rescatados de "organization_and_zones_dataset.csv" pero a traves de BD
@app.get("/organizations-db", response_model=list[Organization])  
async def read_organizations_db():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM organization"
            cursor.execute(sql)
            items = cursor.fetchall()
            return items
    except Exception as e:
        print(e)
        return {"error": "An error occurred while fetching data."}

# Entrega los datos rescatados de "timeseries_dataset.csv" pero a traves de BD
@app.get("/dataset-db", response_model=list[DataSet])  
async def read_dataset_db():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM data_set"
            cursor.execute(sql)
            items = cursor.fetchall()
            return items
    except Exception as e:
        print(e)
        return {"error": "An error occurred while fetching data."}        