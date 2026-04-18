import requests


def envoyer_annotation_texte(api_url, api_token, dossier_id, instructeur_id, annotation_id, texte):
    """
    Envoie un texte dans une annotation textarea DN.
    Retourne (succès: bool, message: str)
    """
    headers = {
        "Authorization": f"Bearer {api_token}",
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

    variables = {
        "input": {
            "dossierId": dossier_id,
            "instructeurId": instructeur_id,
            "clientMutationId": f"envoi-{dossier_id}",
            "annotations": [
                {"id": annotation_id, "value": {"textarea": texte}}
            ]
        }
    }

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json={"query": mutation, "variables": variables},
            timeout=30
        )
        
        data = response.json()

        if data.get("data") is None:
            return False, str(data.get("errors", "Réponse null de l'API DN"))

        errors = data.get("errors")
        if errors:
            return False, errors[0]["message"]

        dm = (data.get("data") or {}).get("dossierModifierAnnotations") or {}
        annotations = dm.get("annotations", [])
        if annotations:
            return True, f"OK - mis à jour le {annotations[0]['updatedAt']}"

        return False, "Réponse inattendue de l'API DN"

    except Exception as e:
        return False, str(e)