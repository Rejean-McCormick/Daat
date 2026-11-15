# DaaT 0.5.0 — état vérifiable du pont d’information

**Candidat d'intégration locale, non version de production certifiée.** Le mandat de cette branche exclut toute création, admission, validation ou publication de Kristals. Les anciens outils Kristal conservés pour compatibilité ne sont pas invoqués par le parcours nouveau `information_bridge`.

## Exécuter et inspecter

Sous Windows, double-cliquer sur `LANCER_DAAT_PONT_INFORMATION.pyw` dans `C:\mycode\Interaction-Kernel\Daat`. Python/Tkinter doivent être installés; `pythonw.exe` évite la console de lancement. Ajouter les sources dans l'onglet **Sources**, confirmer explicitement les permissions, fournir la question et choisir le dossier de sortie. L’application ne contacte pas Medium, PhilPapers, ChatGPT ou un autre serveur et ne recueille aucune session de navigateur.

CLI dans le dépôt après installation (`pip install -e '.[dev,pdf]'` ; `pypdf` optionnel) :

```bash
python -m daat.information_bridge.cli catalog --query phil
python -m daat.information_bridge.cli plan --platform medium
python -m daat.information_bridge.cli diagnose
python -m daat.information_bridge.cli build --job examples/information-bridge/example-job.json --root examples/information-bridge --out /tmp/daat-demo-export
python -m daat.information_bridge.cli verify --dir /tmp/daat-demo-export
python -m daat.information_bridge.cli response-template --dir /tmp/daat-demo-export
python -m daat.information_bridge.cli build-batch --job examples/information-bridge/example-job.json --root examples/information-bridge --out /tmp/daat-demo-shards
```

L'exemple utilise **uniquement des données fictives**, avec déclarations de droits fictives. Il ne doit jamais servir comme preuve de permission pour une vraie publication. Sur Windows, remplacer `/tmp` par un dossier de sortie choisi **hors du dépôt**; chaque export demande un dossier neuf. La GUI collecte directement la sélection en mémoire; elle n’enregistre pas le texte collé dans un manifeste temporaire. Elle prend aussi en charge l’ajout multi-fichiers avec droits explicitement déclarés, la vérification de la réponse JSON de ChatGPT, un prompt de correction et l’export local d’un audit non canonique. Chaque dossier exporte en plus `feedback.json` et `FEEDBACK-DAAT.md` pour les constats actionnables.

## Périmètre réellement codé

| Domaine | État exact de 0.5.0 | Limite de confiance |
|---|---|---|
| Profils et voie d'accès | Registre 89/36, décisions déterministes, refus par défaut | 14 plateformes documentées dans le snapshot de recherche; aucune officiellement certifiée |
| L1 textes/manuels/export | Texte collé, TXT/MD/HTML, bibliographie RIS/JSON/CSV, CSV/TSV/JSON/JSONL, ZIP Medium HTML; PDF optionnel; Office DOCX/XLSX/PPTX/ODT/EPUB et EML | Extraction textuelle approximative pour formats riches; environnement hôte isolé requis pour sources hostiles |
| L5 Git | Lecteur local existant à commit immuable, borné, sans hooks | Aucun clone/fetch implicite, aucun secret ne doit être traité |
| L2/L3 réseau | Transport HTTPS explicite et borné, JSON paginé, RSS/Atom, OAI-PMH et tokens de reprise | **Ports génériques**; contrats propriétaires, droits, comptes, endpoints et réseau hôte non qualifiés; pas de navigateur connecté |
| L4/L6/L7/L8 | Registre, parcours manuels/fédérés et états bloqués explicites | Dumps entreprise, SQL/ERP live, webhooks et custody restent hôtes/propriétaires |
| Droits et confidentialité | Lire/copier/conserver/transformer/divulguer séparés; expiration/révocation; source omise si non permise | Attestation utilisateur non authentifiée; aucune substitution à Konfid, IAM/PEP ou licence de fournisseur |
| Corpus | Identité source/révision, locators, fragments/transformations, dédoublonnage exact/candidat | Dédoublonnage sémantique non certifié, extraction pas garantie sans perte |
| Contexte ChatGPT | Dossier JSON + Markdown + prompt + CSV + rapport de divulgation + empreintes, partage jamais automatique | Schéma **local proposé**, non wire contract IK; SHA-256 n'est pas une signature |
| Lots et synchro | Partition des prompts, metadata-checkpoints SQLite par tenant et refus de réactivation d'une source révoquée | Ordonnancement propriétaire, CDC, quotas réels, restauration/retrait distant non validés |
| ChatGPT manuel | Template de réponse JSON, vérification citations exactes, refus d'identités canoniques, correction | Vérifier une citation ne valide ni la vérité d'une interprétation ni le droit réel de partager |
| Diagnostics | Diagnostic de couverture 89/36 et preuves d'export; tests R1 locaux | DaaT_Diag séparé non actualisé; R2/R3/R4 et GUI Windows nécessitent validation réelle |

## Matrice de 20 chantiers (livraison unique)

Les **160 tâches** du plan restent le backlog de la cible et les **674 cas** sa matrice de tests de conception. La suite `tests/test_information_bridge.py` et la régression historique sont de vrais tests exécutés. Une tâche du backlog ne devient pas `DONE` simplement parce qu'une abstraction de code existe.

| Chantier | Implémentation locale | Qualification externe |
|---|---|---|
| W01 profils/recherche | Présente | Catalogage ≠ accès fournisseur |
| W02 choix et preuve d'accès | Présente, fail-closed | Autorisation hôte manquante |
| W03 ports et adaptateurs | Locaux + ports génériques | Adapters propriétaires en attente |
| W04 import manuel/exports | Présent | UX Windows à certifier |
| W05 flux RSS/OAI | Parser/transport présent | Sandboxes fournisseurs manquantes |
| W06 API REST/JSON | Port générique et pagination | APIs réelles sous contrats manquants |
| W07 Git/documents | Lecteurs locaux présents | Isolation hostile à certifier |
| W08 ERP/bases | Export local existant | Lecture SQL/ERP hôte non qualifiée |
| W09 custody/Médiathèque | Références et limites documentées | Échanges bilatéraux non qualifiés |
| W10 normalisation | Records/texte et transformations locales | Qualité métier/multimodale à valider |
| W11 provenance | Références, révisions, fragments, digests | Attestation fournisseur non obtenue |
| W12 dédoublonnage | Exact/candidats | Match sémantique à approuver |
| W13 droits/disclosure | Refus explicite, expiration, exclusions | Konfid/IAM/PEP non branchés |
| W14 Context Bundle | Export/validation/shards présents | Contrat local proposé |
| W15 prompts et IA | Manuel/JSON audité | API IA et partage hôte non qualifiés |
| W16 revoir et feedback | Validation citations + rapport | Collab multiuser non présente |
| W17 checkpoint/reprise | Local SQLite métadonnées | Orgo/owners à intégrer |
| W18 interface et distribution | CLI + Tkinter + .pyw | Windows GUI non validée visuellement |
| W19 diagnostic | `diagnose`, manifeste/intégrité | DaaT_Diag propriétaire non mis à jour |
| W20 acceptation R4 | Tests R1 synthétiques et régression | **NON TERMINÉ** : sécurité, charges, vrais comptes et contrats bilatéraux |

## Interdits et états sûrs

- Ne jamais inférer le droit de divulgation à partir d'un `200 OK`, login ou reçu de stockage.
- Ne pas contourner un paywall Medium, aspirer une session navigateur ou obtenir des cookies.
- PhilPapers/OAI = **métadonnées disponibles**, pas texte intégral implicite.
- La sélection `manual_paste` exige une attestation de l'utilisateur et ne confère aucune autorité externe.
- La permission `operator_asserted` permet de préparer localement un prompt *manuel*, pas d'activer un fournisseur IA automatiquement. L’interface ne transmet rien.
- Aucune création de KQ/KP/KA/KS ni écriture vers Kit ou publication.
- Les vrais connecteurs ne peuvent être `operational` qu'après tests avec les hôtes et droits associés.

## Statut de validation

Voir `RELEASE-VALIDATION-0.5.0.md` à la racine pour les tests effectivement exécutés, les résultats de l'export synthétique et les vérifications de manifeste. Une sortie `PASS` locale ne transforme pas un test R1 en essai R4.
