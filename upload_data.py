from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import pandas as pd
import json

uri = "mongodb+srv://anujd:790665@cluster0.pooxr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

df = pd.read_csv("E:\projects\senssor fault detection\Notebooks\wafer_23012020_041211.csv")

df.drop("Unnamed: 0", axis=1, inplace=True)

json_record = list(json.loads(df.T.to_json()).values())

client["sensor_project01_db"]["waferfault"].insert_many(json_record)
