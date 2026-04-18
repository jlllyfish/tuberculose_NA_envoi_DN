import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

GRIST_BASE_URL  = os.getenv("GRIST_BASE_URL")
GRIST_API_TOKEN = os.getenv("GRIST_API_TOKEN")
GRIST_DOC_ID    = os.getenv("GRIST_DOC_ID")
TABLE_REPETABLE = os.getenv("GRIST_TABLE_REPETABLE")

headers = {"Authorization": f"Bearer {GRIST_API_TOKEN}"}
url = f"{GRIST_BASE_URL}/docs/{GRIST_DOC_ID}/tables/{TABLE_REPETABLE}/records"

r = requests.get(url, headers=headers)
records = r.json().get("records", [])

if records:
    print("Colonnes disponibles :")
    for k in records[0]["fields"].keys():
        print(f"  {k} = {records[0]['fields'][k]}")
        