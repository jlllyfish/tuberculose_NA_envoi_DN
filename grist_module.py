from datetime import datetime

import requests


def get_dossiers_depuis_repetable(base_url, api_token, doc_id, table_repetable):
    headers = {"Authorization": f"Bearer {api_token}"}
    url = f"{base_url}/docs/{doc_id}/tables/{table_repetable}/records"

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    records = response.json().get("records", [])

    dossiers = {}
    for r in records:
        fields = r["fields"]
        dossier_id_dn = fields.get("Ref_dossier_dossier_id")
        if not dossier_id_dn:
            continue

        if dossier_id_dn not in dossiers:
            dossiers[dossier_id_dn] = {
                "record_ids": [],
                "blocs_valeur_marchande": [],
                "blocs_autres_factures": []
            }

        dossiers[dossier_id_dn]["record_ids"].append(r["id"])

        recap_vm = fields.get("Recapitulatif_valeur_marchande", "")
        if recap_vm:
            dossiers[dossier_id_dn]["blocs_valeur_marchande"].append(recap_vm)

        recap_af = fields.get("Recapitulatif_autres_factures", "")
        if recap_af:
            dossiers[dossier_id_dn]["blocs_autres_factures"].append(recap_af)

    return dossiers


def formater_recap_valeur_marchande(blocs):
    blocs_propres = []
    total = 0
    for i, bloc in enumerate(blocs, 1):
        bloc_sans_md = bloc.replace("**", "")
        blocs_propres.append(f"Demande {i}\n{bloc_sans_md}")
        for ligne in bloc_sans_md.split("\n"):
            if "A payer" in ligne:
                try:
                    total += float(ligne.split(":")[1].replace("€", "").strip())
                except Exception:
                    pass
    resultat = "\n----------\n".join(blocs_propres)
    resultat += f"\n\n==========\n🧾 TOTAL A PAYER : {total} €"
    return resultat


def formater_recap_autres_factures(blocs):
    blocs_propres = []
    total = 0
    for i, bloc in enumerate(blocs, 1):
        bloc_sans_md = bloc.replace("**", "")
        blocs_propres.append(f"Facture {i}\n{bloc_sans_md}")
        for ligne in bloc_sans_md.split("\n"):
            if "Montant" in ligne:
                try:
                    total += float(ligne.split(":")[1].replace("€", "").strip())
                except Exception:
                    pass
    resultat = "\n----------\n".join(blocs_propres)
    resultat += f"\n\n==========\n🧾 TOTAL FACTURES : {total} €"
    return resultat


def mettre_a_jour_statut(base_url, api_token, doc_id, table_repetable, record_ids, succes, message=""):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    url = f"{base_url}/docs/{doc_id}/tables/{table_repetable}/records"

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    statut = "OK" if succes else f"Erreur : {message}"

    payload = {
        "records": [
            {"id": rid, "fields": {"statut_envoi": statut, "date_envoi": now}}
            for rid in record_ids
        ]
    }

    response = requests.patch(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()