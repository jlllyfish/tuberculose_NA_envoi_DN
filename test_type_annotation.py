import json

import requests

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

mutation = """
mutation ($input: DossierModifierAnnotationsInput!) {
  dossierModifierAnnotations(input: $input) {
    annotations { id label stringValue updatedAt }
    clientMutationId
    errors { message }
  }
}
"""

# Types à tester dans l'ordre
type_candidates = [
    {"textarea": "Test API OK"},
    {"text": "Test API OK"},
    {"integerNumber": 1},
    {"decimalNumber": 1.0},
    {"checkbox": False},
    {"yesNo": False},
    {"email": "test@test.fr"},
    {"date": "2026-04-16"},
    {"dossierLink": ""},
]

for value in type_candidates:
    type_name = list(value.keys())[0]
    variables = {
        "input": {
            "dossierId": DOSSIER_ID,
            "instructeurId": INSTRUCTEUR_ID,
            "clientMutationId": f"test-{type_name}",
            "annotations": [{"id": ANNOTATION_ID, "value": value}]
        }
    }
    r = requests.post(API_URL, headers=headers, json={"query": mutation, "variables": variables})
    data = r.json()
    errors = data.get("data", {}).get("dossierModifierAnnotations", {}).get("errors", [])
    if not errors:
        print(f"✅ TYPE TROUVÉ : {type_name}")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        break
    else:
        print(f"❌ {type_name} → {errors[0]['message']}")