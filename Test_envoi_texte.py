import json

import requests

# --- Config ---
API_TOKEN = "OTk0ZDVhMDYtOTBmYy00NDUwLWE0NzUtMDg0ZGMxZmNlYTliO0RqN01XWFFvVzNBSkJWbWpyRE5UU2RlZA=="
DOSSIER_ID = "RG9zc2llci0zMDcxMzUyOA=="
INSTRUCTEUR_ID = "SW5zdHJ1Y3RldXItMzg2OTE="

# ID de l'annotation texte à modifier (à remplacer par le vrai ID)
ANNOTATION_ID = "Q2hhbXAtNjQwOTc5Nw=="

API_URL = "https://demarche.numerique.gouv.fr/api/v2/graphql"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# --- Mutation ---
mutation = """
mutation ($input: DossierModifierAnnotationsInput!) {
  dossierModifierAnnotations(input: $input) {
    annotations {
      champDescriptorId
      id
      label
      prefilled
      stringValue
      updatedAt
    }
    clientMutationId
    errors {
      message
    }
  }
}
"""

variables = {
    "input": {
        "dossierId": DOSSIER_ID,
        "instructeurId": INSTRUCTEUR_ID,
        "clientMutationId": "test-texte-001",
        "annotations": [
            {
                "id": ANNOTATION_ID,
                "value": {
                    "text": "Test envoi depuis API - OK"
                }
            }
        ]
    }
}

# --- Envoi ---
response = requests.post(
    API_URL,
    headers=headers,
    json={"query": mutation, "variables": variables}
)

data = response.json()
print(json.dumps(data, indent=2, ensure_ascii=False))

# --- Vérification rapide ---
if "errors" in data:
    print("\n❌ Erreurs GraphQL :", data["errors"])
elif data.get("data", {}).get("dossierModifierAnnotations", {}).get("errors"):
    print("\n❌ Erreurs métier :", data["data"]["dossierModifierAnnotations"]["errors"])
else:
    annotations = data.get("data", {}).get("dossierModifierAnnotations", {}).get("annotations", [])
    print(f"\n✅ Succès - {len(annotations)} annotation(s) retournée(s)")
    for a in annotations:
        print(f"  [{a['id']}] {a['label']} = {a['stringValue']}")