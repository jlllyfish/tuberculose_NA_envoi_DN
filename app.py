import os

from dn_module import envoyer_annotation_texte
from dotenv import load_dotenv
from grist_module import (formater_recap_autres_factures,
                          formater_recap_valeur_marchande,
                          get_dossiers_depuis_repetable, mettre_a_jour_statut)

load_dotenv()

DN_API_URL        = os.getenv("DN_API_URL")
DN_API_TOKEN      = os.getenv("DN_API_TOKEN")
DN_INSTRUCTEUR_ID = os.getenv("DN_INSTRUCTEUR_ID")
DN_ANNOTATION_ID_VM    = os.getenv("DN_ANNOTATION_ID")
DN_ANNOTATION_ID_AF    = os.getenv("DN_ANNOTATION_ID_AUTRES")

GRIST_BASE_URL  = os.getenv("GRIST_BASE_URL")
GRIST_API_TOKEN = os.getenv("GRIST_API_TOKEN")
GRIST_DOC_ID    = os.getenv("GRIST_DOC_ID")
TABLE_REPETABLE = os.getenv("GRIST_TABLE_REPETABLE")

print("📥 Lecture des données Grist...")
dossiers = get_dossiers_depuis_repetable(GRIST_BASE_URL, GRIST_API_TOKEN, GRIST_DOC_ID, TABLE_REPETABLE)
print(f"   {len(dossiers)} dossier(s) trouvé(s)\n")

for dossier_id_dn, data in dossiers.items():
    record_ids = data["record_ids"]
    blocs_vm = data["blocs_valeur_marchande"]
    blocs_af = data["blocs_autres_factures"]

    print(f"📤 Dossier {dossier_id_dn}")

    # --- Valeur marchande ---
    if blocs_vm:
        texte_vm = formater_recap_valeur_marchande(blocs_vm)
        succes, message = envoyer_annotation_texte(
            DN_API_URL, DN_API_TOKEN,
            dossier_id_dn, DN_INSTRUCTEUR_ID, DN_ANNOTATION_ID_VM,
            texte_vm
        )
        print(f"   Valeur marchande : {'✅ ' + message if succes else '❌ ' + message}")
    else:
        print("   Valeur marchande : ⚠️ aucun bloc, ignoré")

    # --- Autres factures ---
    if blocs_af:
        texte_af = formater_recap_autres_factures(blocs_af)
        succes_af, message_af = envoyer_annotation_texte(
            DN_API_URL, DN_API_TOKEN,
            dossier_id_dn, DN_INSTRUCTEUR_ID, DN_ANNOTATION_ID_AF,
            texte_af
        )
        print(f"   Autres factures  : {'✅ ' + message_af if succes_af else '❌ ' + message_af}")
    else:
        print("   Autres factures  : ⚠️ aucun bloc, ignoré")

    # Log statut global (OK si les deux réussissent)
    succes_global = (not blocs_vm or succes) and (not blocs_af or succes_af)
    mettre_a_jour_statut(
        GRIST_BASE_URL, GRIST_API_TOKEN, GRIST_DOC_ID,
        TABLE_REPETABLE, record_ids, succes_global
    )

print("\n✅ Terminé")
