# 03 — Voies d'accès, choix déterministe et absence de contournement

## 1. Lanes de référence (déjà décrites dans `docs/27-*`)

| Voie | Moyen | Objet | Contrôle préalable | Réponse si indisponible |
|---|---|---|---|---|
| L1 | Fichier local, dossier, collage, ZIP | Octets fournis explicitement | Lire/copier/partager autorisé, antivirus/parser isolé | Référence ou action utilisateur |
| L2 | API de lecture REST/GraphQL/SOAP/OData | Métadonnées ou contenu dans le scope | Jeton hôte, périmètre, licence, quota | RSS/export/fichier autorisé |
| L3 | Harvest, OAI-PMH, RSS/Atom, DCAT | Lots ou alertes | Termes, licence, couverture et granularité | API/metadata-only |
| L4 | Snapshot massif, dump | Collection versionnée | Accord, volume, stockage et coûts | Pagination/partition ou référence |
| L5 | Git, objet versionné | Commit/blob/révision | ACL, immutabilité vérifiée | Archive/fichier fourni |
| L6 | ERP/CRM/base SQL | Export ou lecture SQL bornée | Droits, cohérence transactionnelle, PII, least privilege | Export humain |
| L7 | Webhook/événement propriétaire | Changement, watermark | Authentification de l'émetteur, ordre et répétition | Polling contrôlé |
| L8 | Référence fédérée | URI, manifeste, lien | ACL à chaque consultation, durée de vie et révocation | Snapshot explicitement autorisé |

**Mode transversal** : contribution manuelle par utilisateur (collage de référence, résumé, extrait, fichier). Elle ne transforme pas un accès navigateur en droit de transmettre à l'IA.

## 2. Planificateur — exemple de pseudo-code

```text
proposer_voies(source, finalité, actor, tenant, contenu_voulu):
  fiche = lire_registre_versionné(source)
  exiger preuve de l'identité du host et finalité explicite
  candidats = voies déclarées compatible avec object/format/contenu
  pour voie dans candidats:
    vérifier capacité réellement testée et état fournisseur
    vérifier permissions source: lecture, copie, stockage, transformation
    vérifier séparément permission de transmission à ChatGPT/API
    vérifier version/snapshot, coûts, limites, rétention, quotas
    si capacité ou droit inconnu -> non-éligible / demander preuve
    conserver motif(s), budget, sens de granularité
  classer voies éligibles: sécurité/contrat > fidélité/provenance >
                          coût/quotas > reprise/synchronisation
  retourner plan avec choix, alternatives, blocages et consentements
```

Les méthodes d'acquisition et de divulgation sont **deux décisions séparées**. Une voie qui permet la découverte bibliographique ne donne pas le droit de copier un article; une permission de téléchargement ne donne pas nécessairement celle de l'envoyer à ChatGPT.

## 3. Faits particuliers à honorer

**PhilPapers** : API JSON / informations bibliographiques sous conditions; OAI-PMH sur le périmètre ouvert documenté; réutilisation soumise aux conditions officielles et restrictions de redistribution. Dédupliquer via DOI/titre/ID, conserver `metadata_only` si texte non acquis; rediriger vers version OA autorisée si vérifiée.

**Medium** : RSS d'auteurs/publications/sujets pour découverte; export du compte ZIP/HTML pour son propriétaire; aucune nouvelle intégration basée sur les anciens jetons API; utilisateur peut importer un texte autorisé. Pas d'automatisation du navigateur connecté ni d'extraction de cookies.

**Zotero** : Web API v3 avec entêtes de version et clefs/OAuth selon bibliothèque; ne pas présumer que les fichiers associés sont exportables. **OpenAlex** : API REST de métadonnées, clé nécessaire à certaines fonctions de pagination/volume au moment de la documentation; respecter en-têtes/quotas. **Crossref** : API REST, `mailto`, backoff et cache. **GitHub** : requests conditionnelles (`ETag`) et commit immuable. **WordPress** : API par site, pas API globale unique. **Google Drive** : distinction entre métadonnées, blob et export de document selon droits et `canDownload`. Voir références officielles dans `18-SOURCES-EXTERNES-VERIFIEES.md`.

## 4. Fiche décision de voie (structure interne proposée)

Champs minimum : `decision_id`, `profile_id`, `profile_revision`, `source_kind`, `requested_granularity`, `available_granularity`, `methods_considered[]`, `selected_method|null`, `eligibility_reasons[]`, `permission_evidence_refs[]`, `host_identity_binding_ref`, `scope`, `source_revision`, `ai_disclosure_status`, `owner_of_acquisition`, `quota_estimate`, `checked_at`, `result` parmi `eligible`, `conditional`, `blocked`, `unsupported`. **Aucune clef ni donnée secrète en clair.**

## 5. Repli sûr (sans scraping opportuniste)

Si `full_text` indisponible, produire une notice/abstract **étiquetée**, puis demander un fichier/texte autorisé ou conserver la référence seule. Une fiche `candidate_requires_verification` ne peut pas déclencher un appel réseau; seule la combinaison d'une voie documentée, implémentée, testée et autorisée le peut. Si aucun chemin sûr : `BLOCKED` avec prochaine action, pas `PASS` et pas une interprétation imaginaire.
