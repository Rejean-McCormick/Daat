# 04 — Registre détaillé des 89 plateformes et types de sources

**Source du tableau** : `docs/data/platform-access-registry.v1.json` de DaaT 0.4.4, repris sans promouvoir son niveau de maturité. **Document cible, pas connecteurs livrés.**

**Inventaire** : 89 profils, 36 familles; 14 avec au moins une voie documentée officiellement, 75 à vérifier; **0 connecteur certifié dans le registre de départ**.

Les mots *API*, *export* ou *connexion* décrivent une **piste du registre** et non un accès accordé. `official_docs_checked` concerne **au moins une voie**; chaque `access_paths[].doc_status` détaille la qualification documentaire propre à la méthode.

| ID | Plateforme | Familles | Voie préférée dans le registre | Documentation | Connecteur DaaT |
|---|---|---|---|---|---|
| `philpapers` | PhilPapers | 01, 02 | `harvest_oai_pmh` | doc. officielle partielle | non certifié |
| `philarchive` | PhilArchive | 02 | `harvest_oai_pmh` | doc. officielle partielle | non certifié |
| `medium` | Medium | 06 | `rss_atom` | doc. officielle partielle | non certifié |
| `openalex` | OpenAlex | 01 | `api_read` | doc. officielle partielle | non certifié |
| `crossref` | Crossref | 01 | `api_read` | doc. officielle partielle | non certifié |
| `semantic-scholar` | Semantic Scholar | 01 | `api_read` | doc. officielle partielle | non certifié |
| `arxiv` | arXiv | 02 | `harvest_oai_pmh` | à vérifier | non certifié |
| `pubmed-ncbi` | PubMed / NCBI | 01, 02 | `api_read` | doc. officielle partielle | non certifié |
| `europe-pmc` | Europe PMC | 02 | `api_read` | à vérifier | non certifié |
| `doaj` | DOAJ | 01 | `api_read` | à vérifier | non certifié |
| `hal` | HAL | 02 | `harvest_oai_pmh` | à vérifier | non certifié |
| `zenodo` | Zenodo | 02, 08 | `api_read` | à vérifier | non certifié |
| `osf` | OSF | 02, 09 | `api_read` | à vérifier | non certifié |
| `ssrn` | SSRN | 02 | `federated_ref` | à vérifier | non certifié |
| `biorxiv` | bioRxiv | 02 | `api_read` | à vérifier | non certifié |
| `zotero` | Zotero | 01, 03 | `api_read` | doc. officielle partielle | non certifié |
| `orcid` | ORCID | 01 | `api_read` | à vérifier | non certifié |
| `worldcat` | WorldCat | 03 | `api_read` | à vérifier | non certifié |
| `banq-catalogues-qu-b-cois` | BAnQ / catalogues québécois | 03, 28 | `federated_ref` | à vérifier | non certifié |
| `wikidata` | Wikidata | 04 | `api_read` | à vérifier | non certifié |
| `dbpedia-rdf-public` | DBpedia / RDF public | 04, 18 | `bulk_export` | à vérifier | non certifié |
| `wikipedia` | Wikipedia | 05 | `api_read` | à vérifier | non certifié |
| `mediawiki-autonome` | MediaWiki autonome | 05 | `api_read` | à vérifier | non certifié |
| `wordpress` | WordPress | 06 | `api_read` | doc. officielle partielle | non certifié |
| `ghost` | Ghost | 06 | `api_read` | doc. officielle partielle | non certifié |
| `substack` | Substack | 06 | `rss_atom` | à vérifier | non certifié |
| `blogger` | Blogger | 06 | `rss_atom` | à vérifier | non certifié |
| `flux-rss-atom-g-n-rique` | Flux RSS/Atom générique | 06, 35 | `rss_atom` | à vérifier | non certifié |
| `ckan` | CKAN | 07 | `api_read` | doc. officielle partielle | non certifié |
| `statistique-canada` | Statistique Canada | 07, 30 | `api_read` | à vérifier | non certifié |
| `portail-donn-es-ouvertes-municipal` | Portail données ouvertes municipal | 07, 23, 30 | `api_read` | à vérifier | non certifié |
| `pdf-fourni-par-utilisateur` | PDF fourni par utilisateur | 08 | `local_file` | à vérifier | non certifié |
| `docx-texte-fourni-par-utilisateur` | DOCX/texte fourni par utilisateur | 08 | `local_file` | à vérifier | non certifié |
| `archives-zip-tar` | Archives ZIP/TAR | 09 | `local_file` | à vérifier | non certifié |
| `google-drive` | Google Drive | 10 | `api_read` | à vérifier | non certifié |
| `microsoft-sharepoint-onedrive` | Microsoft SharePoint / OneDrive | 10 | `api_read` | à vérifier | non certifié |
| `amazon-s3` | Amazon S3 | 10, 17 | `api_read` | à vérifier | non certifié |
| `github` | GitHub | 11, 12 | `git_snapshot` | doc. officielle partielle | non certifié |
| `gitlab` | GitLab | 11, 12 | `git_snapshot` | doc. officielle partielle | non certifié |
| `bitbucket` | Bitbucket | 11 | `git_snapshot` | à vérifier | non certifié |
| `jira` | Jira | 12 | `api_read` | à vérifier | non certifié |
| `linear` | Linear | 12 | `api_read` | à vérifier | non certifié |
| `acomba` | Acomba | 13 | `user_export` | à vérifier | non certifié |
| `quickbooks-online` | QuickBooks Online | 13 | `api_read` | à vérifier | non certifié |
| `xero` | Xero | 13 | `api_read` | à vérifier | non certifié |
| `sage` | Sage | 13 | `user_export` | à vérifier | non certifié |
| `sap` | SAP | 14 | `api_read` | à vérifier | non certifié |
| `salesforce` | Salesforce | 14 | `api_read` | à vérifier | non certifié |
| `microsoft-dynamics` | Microsoft Dynamics | 14 | `api_read` | à vérifier | non certifié |
| `odoo` | Odoo | 14 | `api_read` | à vérifier | non certifié |
| `shopify` | Shopify | 15 | `api_read` | à vérifier | non certifié |
| `woocommerce` | WooCommerce | 15 | `api_read` | à vérifier | non certifié |
| `postgresql-mysql` | PostgreSQL / MySQL | 16 | `database_read` | à vérifier | non certifié |
| `sql-server-oracle` | SQL Server / Oracle | 16 | `database_read` | à vérifier | non certifié |
| `snowflake` | Snowflake | 17 | `database_read` | à vérifier | non certifié |
| `bigquery` | BigQuery | 17 | `api_read` | à vérifier | non certifié |
| `databricks` | Databricks | 17 | `api_read` | à vérifier | non certifié |
| `neo4j` | Neo4j | 18 | `database_read` | à vérifier | non certifié |
| `rdf-sparql-endpoint` | RDF / SPARQL endpoint | 18, 36 | `api_read` | à vérifier | non certifié |
| `imap-mbox` | IMAP / MBOX | 19 | `user_export` | à vérifier | non certifié |
| `slack` | Slack | 19 | `api_read` | à vérifier | non certifié |
| `microsoft-teams` | Microsoft Teams | 19 | `api_read` | à vérifier | non certifié |
| `moodle` | Moodle | 20 | `api_read` | à vérifier | non certifié |
| `canvas-lms` | Canvas LMS | 20 | `api_read` | à vérifier | non certifié |
| `serveur-fhir` | Serveur FHIR | 21 | `api_read` | à vérifier | non certifié |
| `hl7-dicom-institutionnel` | HL7/DICOM institutionnel | 21, 27 | `local_file` | à vérifier | non certifié |
| `legisqu-bec` | LegisQuébec | 22 | `federated_ref` | à vérifier | non certifié |
| `canlii` | CanLII | 22 | `federated_ref` | à vérifier | non certifié |
| `openstreetmap` | OpenStreetMap | 23 | `bulk_export` | à vérifier | non certifié |
| `wfs-geojson-municipal` | WFS/GeoJSON municipal | 23 | `api_read` | à vérifier | non certifié |
| `noaa` | NOAA | 24 | `api_read` | à vérifier | non certifié |
| `copernicus` | Copernicus | 24 | `api_read` | à vérifier | non certifié |
| `broker-mqtt` | Broker MQTT | 25, 31 | `events` | à vérifier | non certifié |
| `serveur-opc-ua` | Serveur OPC UA | 25 | `api_read` | à vérifier | non certifié |
| `lims-eln` | LIMS / ELN | 26 | `user_export` | à vérifier | non certifié |
| `iiif-collections-patrimoniales` | IIIF collections patrimoniales | 27, 28 | `api_read` | à vérifier | non certifié |
| `internet-archive` | Internet Archive | 28 | `api_read` | à vérifier | non certifié |
| `open-banking-autoris` | Open Banking autorisé | 29 | `api_read` | à vérifier | non certifié |
| `iso-20022-relev-s-bancaires` | ISO 20022 / relevés bancaires | 29 | `local_file` | à vérifier | non certifié |
| `registres-publics-d-entreprises` | Registres publics d'entreprises | 30 | `api_read` | à vérifier | non certifié |
| `kafka-cloudevents` | Kafka / CloudEvents | 31 | `events` | à vérifier | non certifié |
| `webhooks-m-tier` | Webhooks métier | 31 | `events` | à vérifier | non certifié |
| `formulaires-et-enqu-tes` | Formulaires et enquêtes | 32 | `user_export` | à vérifier | non certifié |
| `simulation-jumeaux-num-riques` | Simulation / jumeaux numériques | 33 | `user_export` | à vérifier | non certifié |
| `reddit` | Reddit | 34 | `api_read` | à vérifier | non certifié |
| `stack-exchange` | Stack Exchange | 34 | `api_read` | à vérifier | non certifié |
| `youtube` | YouTube | 35 | `api_read` | doc. officielle partielle | non certifié |
| `podcasts-rss` | Podcasts RSS | 35 | `rss_atom` | à vérifier | non certifié |
| `r-f-rence-f-d-r-e-externe` | Référence fédérée externe | 36 | `federated_ref` | à vérifier | non certifié |

## Fiches intégrales héritées du registre existant

Chaque fiche conserve explicitement le périmètre des informations, les prérequis et limites; les URL sont des **références documentaires**, pas des consentements.

### 01. PhilPapers — `philpapers`

**Familles** : Références bibliographiques, Archives académiques OA (`01, 02`).  
**Portée déclarée** : Bibliographie et taxonomie; corpus OA distinct.  
**Préconditions déclarées** : Clé/accord selon flux; OAI ouvert uniquement sur périmètre disponible.  
**Limites déclarées** : API JSON des sous-ensembles sous conditions; redistribution massive restreinte.  
**Voie de préférence (recherche)** : `harvest_oai_pmh`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `official_docs_checked` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `official_docs_checked`.
- `harvest_oai_pmh` / Moissonnage OAI-PMH (lanes L3) — `official_docs_checked`.
- `licensed_batch` / Lot sous licence/accord spécifique (lanes L3, L4) — `candidate_requires_verification`.
- `manual_paste` / Copier-coller autorisé (lanes L1) — `candidate_requires_verification`.
**Références du registre** : <https://philpapers.org/help/api/>, <https://philpapers.org/help/api/json.html>, <https://philpapers.org/help/oai.html>, <https://philpapers.org/help/terms.html>.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 02. PhilArchive — `philarchive`

**Familles** : Archives académiques OA (`02`).  
**Portée déclarée** : Références et dépôts OA autorisés.  
**Préconditions déclarées** : Vérifier licence du texte, version et source.  
**Limites déclarées** : OAI donne des métadonnées; disponibilité d'un PDF ne confère pas licence de redistribution.  
**Voie de préférence (recherche)** : `harvest_oai_pmh`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `official_docs_checked` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `harvest_oai_pmh` / Moissonnage OAI-PMH (lanes L3) — `official_docs_checked`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Références du registre** : <https://philpapers.org/help/oai.html>, <https://philpapers.org/help/terms.html>.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 03. Medium — `medium`

**Familles** : Sites et articles Web (`06`).  
**Portée déclarée** : RSS découverte/extraits; ZIP HTML du titulaire; texte fourni.  
**Préconditions déclarées** : RSS public; export du propre compte; accès navigateur détenu par utilisateur.  
**Limites déclarées** : Paywall exclu du texte intégral RSS; pas de nouveaux jetons API; partage du texte dépend des droits.  
**Voie de préférence (recherche)** : `rss_atom`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `official_docs_checked` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `rss_atom` / Flux RSS/Atom (lanes L3) — `official_docs_checked`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `official_docs_checked`.
- `authenticated_web` / Lecture navigateur connecté, sans extraction automatisée de session (lanes L8) — `candidate_requires_verification`.
- `manual_paste` / Copier-coller autorisé (lanes L1) — `candidate_requires_verification`.
**Références du registre** : <https://help.medium.com/hc/en-us/articles/214874118-Using-RSS-feeds-of-profiles-publications-and-topics/>, <https://help.medium.com/hc/en-us/articles/115004745787-Export-your-account-data>, <https://help.medium.com/hc/en-us/articles/213480228-API-Importing>.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 04. OpenAlex — `openalex`

**Familles** : Références bibliographiques (`01`).  
**Portée déclarée** : Métadonnées de travaux, auteurs, institutions, accès OA.  
**Préconditions déclarées** : API publique avec budget d'usage; vérifier conditions et coûts.  
**Limites déclarées** : Métadonnées/abstracts != licence de texte intégral.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `official_docs_checked` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `official_docs_checked`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Références du registre** : <https://help.openalex.org/api/>.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 05. Crossref — `crossref`

**Familles** : Références bibliographiques (`01`).  
**Portée déclarée** : DOI, éditeurs, métadonnées, liens, licences, corrections.  
**Préconditions déclarées** : API publique; utiliser identification et pagination raisonnable.  
**Limites déclarées** : Certains résumés peuvent relever de droits tiers.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `official_docs_checked` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `official_docs_checked`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Références du registre** : <https://www.crossref.org/documentation/retrieve-metadata/rest-api>.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 06. Semantic Scholar — `semantic-scholar`

**Familles** : Références bibliographiques (`01`).  
**Portée déclarée** : Métadonnées, références, graphes de citation.  
**Préconditions déclarées** : Quota et clés selon endpoints.  
**Limites déclarées** : Accès aux données ne signifie pas droit au texte intégral.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `official_docs_checked` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `official_docs_checked`.
- `bulk_export` / Export massif / dump (lanes L4) — `official_docs_checked`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Références du registre** : <https://webflow.semanticscholar.org/product/api>.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 07. arXiv — `arxiv`

**Familles** : Archives académiques OA (`02`).  
**Portée déclarée** : Préprints, métadonnées, versions.  
**Préconditions déclarées** : Règles de débit et licences par document.  
**Limites déclarées** : Les versions et droits varient; ne pas assimiler préprint et article revu.  
**Voie de préférence (recherche)** : `harvest_oai_pmh`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `harvest_oai_pmh` / Moissonnage OAI-PMH (lanes L3) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 08. PubMed / NCBI — `pubmed-ncbi`

**Familles** : Références bibliographiques, Archives académiques OA (`01, 02`).  
**Portée déclarée** : Citations biomédicales, résumés; liens PMC.  
**Préconditions déclarées** : E-utilities, identifiants PMID/PMCID et restrictions de débit.  
**Limites déclarées** : PubMed != accès libre universel aux textes intégraux.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `official_docs_checked` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `official_docs_checked`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Références du registre** : <https://www.ncbi.nlm.nih.gov/books/NBK25500/>.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 09. Europe PMC — `europe-pmc`

**Familles** : Archives académiques OA (`02`).  
**Portée déclarée** : Références et sous-ensemble OA texte intégral.  
**Préconditions déclarées** : Vérifier licences, sources et conditions API.  
**Limites déclarées** : Seuls certains documents ont du texte complet réutilisable.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 10. DOAJ — `doaj`

**Familles** : Références bibliographiques (`01`).  
**Portée déclarée** : Répertoire de revues et articles OA.  
**Préconditions déclarées** : Vérifier version API et licences d'articles.  
**Limites déclarées** : Open access ne signifie pas droits uniformes.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 11. HAL — `hal`

**Familles** : Archives académiques OA (`02`).  
**Portée déclarée** : Dépôts et versions institutionnelles.  
**Préconditions déclarées** : API/OAI selon collections; droits par fichier.  
**Limites déclarées** : Embargo et métadonnées vs textes.  
**Voie de préférence (recherche)** : `harvest_oai_pmh`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `harvest_oai_pmh` / Moissonnage OAI-PMH (lanes L3) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 12. Zenodo — `zenodo`

**Familles** : Archives académiques OA, PDF et documents locaux (`02, 08`).  
**Portée déclarée** : Enregistrements, DOI, données et fichiers.  
**Préconditions déclarées** : Déclaration de licence par record.  
**Limites déclarées** : Métadonnées vs contenu et versions.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 13. OSF — `osf`

**Familles** : Archives académiques OA, Archives de documents (`02, 09`).  
**Portée déclarée** : Projets, préprints, dépôts collaboratifs.  
**Préconditions déclarées** : Jeton/espace privé si requis.  
**Limites déclarées** : Droits et partage selon projet.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 14. SSRN — `ssrn`

**Familles** : Archives académiques OA (`02`).  
**Portée déclarée** : Références, abstracts et textes autorisés.  
**Préconditions déclarées** : Droits individuels et accès institutionnel.  
**Limites déclarées** : Pas de moissonnage automatique assumé.  
**Voie de préférence (recherche)** : `federated_ref`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
- `manual_paste` / Copier-coller autorisé (lanes L1) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 15. bioRxiv — `biorxiv`

**Familles** : Archives académiques OA (`02`).  
**Portée déclarée** : Métadonnées de préprints.  
**Préconditions déclarées** : Vérifier les flux officiels et licences.  
**Limites déclarées** : Préprints non revus et versions changeantes.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `harvest_oai_pmh` / Moissonnage OAI-PMH (lanes L3) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 16. Zotero — `zotero`

**Familles** : Références bibliographiques, Bibliothèques et catalogues (`01, 03`).  
**Portée déclarée** : Bibliothèques, collections, citations et pièces autorisées.  
**Préconditions déclarées** : Compte, clé personnelle, API v3 / local API.  
**Limites déclarées** : Pièces jointes régies par leurs droits d'origine.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `official_docs_checked` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `official_docs_checked`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
**Références du registre** : <https://www.zotero.org/support/dev/web_api/v3/basics>, <https://www.zotero.org/support/dev/web_api/v3/syncing>.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 17. ORCID — `orcid`

**Familles** : Références bibliographiques (`01`).  
**Portée déclarée** : Identifiants chercheurs, affiliations, travaux.  
**Préconditions déclarées** : Scopes et visibilité par champ.  
**Limites déclarées** : Identité déclarée n'est pas garantie de qualité.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 18. WorldCat — `worldcat`

**Familles** : Bibliothèques et catalogues (`03`).  
**Portée déclarée** : Notices de catalogues.  
**Préconditions déclarées** : Accord/licence bibliographique, accès OCLC.  
**Limites déclarées** : Pas de redistribution par défaut.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `licensed_batch` / Lot sous licence/accord spécifique (lanes L3, L4) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 19. BAnQ / catalogues québécois — `banq-catalogues-qu-b-cois`

**Familles** : Bibliothèques et catalogues, Archives institutionnelles (`03, 28`).  
**Portée déclarée** : Notices et objets patrimoniaux selon service.  
**Préconditions déclarées** : Vérifier interface exacte par collection.  
**Limites déclarées** : Les droits varient par document et collection.  
**Voie de préférence (recherche)** : `federated_ref`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `harvest_oai_pmh` / Moissonnage OAI-PMH (lanes L3) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 20. Wikidata — `wikidata`

**Familles** : Bases de connaissances publiques (`04`).  
**Portée déclarée** : Entités, propriétés, références, qualifiers.  
**Préconditions déclarées** : API SPARQL/dumps selon quotas.  
**Limites déclarées** : Q/P externes ne sont jamais des KQ/KP internes.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 21. DBpedia / RDF public — `dbpedia-rdf-public`

**Familles** : Bases de connaissances publiques, Graphes d’entreprise (`04, 18`).  
**Portée déclarée** : Triplets RDF et ontologies.  
**Préconditions déclarées** : Endpoint public ou export versionné.  
**Limites déclarées** : Dérivé externe, provenance et inférences à contrôler.  
**Voie de préférence (recherche)** : `bulk_export`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 22. Wikipedia — `wikipedia`

**Familles** : Encyclopédies et wikis (`05`).  
**Portée déclarée** : Pages, révisions, wikitext.  
**Préconditions déclarées** : MediaWiki API et dumps; attribution.  
**Limites déclarées** : Texte collaboratif n'est pas validation canonique.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 23. MediaWiki autonome — `mediawiki-autonome`

**Familles** : Encyclopédies et wikis (`05`).  
**Portée déclarée** : Pages et historiques internes.  
**Préconditions déclarées** : Authentification selon wiki.  
**Limites déclarées** : Permissions wiki et ACL.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `authenticated_web` / Lecture navigateur connecté, sans extraction automatisée de session (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 24. WordPress — `wordpress`

**Familles** : Sites et articles Web (`06`).  
**Portée déclarée** : Articles, pages, médias, révisions selon site.  
**Préconditions déclarées** : REST API pour publications; accès protégé selon site.  
**Limites déclarées** : API ne garantit pas réutilisation des textes tiers.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `official_docs_checked` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `official_docs_checked`.
- `rss_atom` / Flux RSS/Atom (lanes L3) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `authenticated_web` / Lecture navigateur connecté, sans extraction automatisée de session (lanes L8) — `candidate_requires_verification`.
**Références du registre** : <https://developer.wordpress.org/rest-api/reference/posts/>.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 25. Ghost — `ghost`

**Familles** : Sites et articles Web (`06`).  
**Portée déclarée** : Articles publiés et métadonnées.  
**Préconditions déclarées** : Content API clé de lecture et site configuré.  
**Limites déclarées** : Clé de lecture ne confère pas licence sur contenu tiers.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `official_docs_checked` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `official_docs_checked`.
- `rss_atom` / Flux RSS/Atom (lanes L3) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Références du registre** : <https://ghost.org/docs/content-api/>.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 26. Substack — `substack`

**Familles** : Sites et articles Web (`06`).  
**Portée déclarée** : Flux et publications accessibles.  
**Préconditions déclarées** : RSS lorsque exposé; export du propriétaire à vérifier.  
**Limites déclarées** : Abonnements et contenus restreints; API générale non présumée.  
**Voie de préférence (recherche)** : `rss_atom`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `rss_atom` / Flux RSS/Atom (lanes L3) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `manual_paste` / Copier-coller autorisé (lanes L1) — `candidate_requires_verification`.
- `authenticated_web` / Lecture navigateur connecté, sans extraction automatisée de session (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 27. Blogger — `blogger`

**Familles** : Sites et articles Web (`06`).  
**Portée déclarée** : Articles de blogs.  
**Préconditions déclarées** : Flux publics; API selon compte.  
**Limites déclarées** : Accès privé non implicite.  
**Voie de préférence (recherche)** : `rss_atom`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `rss_atom` / Flux RSS/Atom (lanes L3) — `candidate_requires_verification`.
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 28. Flux RSS/Atom générique — `flux-rss-atom-g-n-rique`

**Familles** : Sites et articles Web, Flux et catalogues multimédias (`06, 35`).  
**Portée déclarée** : Nouveaux titres, auteurs, dates, extraits ou contenu offert.  
**Préconditions déclarées** : Flux public et droits de réutilisation.  
**Limites déclarées** : Feed n'assure jamais texte complet.  
**Voie de préférence (recherche)** : `rss_atom`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `rss_atom` / Flux RSS/Atom (lanes L3) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 29. CKAN — `ckan`

**Familles** : Jeux de données ouverts (`07`).  
**Portée déclarée** : Catalogues et ressources CSV/JSON/Parquet.  
**Préconditions déclarées** : API Action v3 selon portail, licences par jeu.  
**Limites déclarées** : Un portail peut héberger ressources externes avec conditions propres.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `official_docs_checked` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `official_docs_checked`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
**Références du registre** : <https://docs.ckan.org/en/latest/api/>.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 30. Statistique Canada — `statistique-canada`

**Familles** : Jeux de données ouverts, Registres publics et société (`07, 30`).  
**Portée déclarée** : Indicateurs, tableaux statistiques et métadonnées.  
**Préconditions déclarées** : Portails/API spécifiques; citer millésime et unités.  
**Limites déclarées** : Méthodes révisées et agrégations.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 31. Portail données ouvertes municipal — `portail-donn-es-ouvertes-municipal`

**Familles** : Jeux de données ouverts, Cartographie/GIS, Registres publics et société (`07, 23, 30`).  
**Portée déclarée** : Données géographiques/statistiques locales.  
**Préconditions déclarées** : API CKAN/Socrata/DCAT selon municipalité.  
**Limites déclarées** : Conditions d'utilisation propres à chaque portail.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 32. PDF fourni par utilisateur — `pdf-fourni-par-utilisateur`

**Familles** : PDF et documents locaux (`08`).  
**Portée déclarée** : PDF texte/pages/figures.  
**Préconditions déclarées** : Fichier autorisé et consignes PII.  
**Limites déclarées** : OCR peut être nécessaire; conserver références de page.  
**Voie de préférence (recherche)** : `local_file`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
- `manual_paste` / Copier-coller autorisé (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 33. DOCX/texte fourni par utilisateur — `docx-texte-fourni-par-utilisateur`

**Familles** : PDF et documents locaux (`08`).  
**Portée déclarée** : Texte, sections, tableaux.  
**Préconditions déclarées** : Droit d'accès et de partage.  
**Limites déclarées** : Déstructuration des tableaux et notes.  
**Voie de préférence (recherche)** : `local_file`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
- `manual_paste` / Copier-coller autorisé (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 34. Archives ZIP/TAR — `archives-zip-tar`

**Familles** : Archives de documents (`09`).  
**Portée déclarée** : Fichiers regroupés et index interne.  
**Préconditions déclarées** : Limites de taille/profondeur et contrôle anti-bombe ZIP.  
**Limites déclarées** : Chaque fichier garde ses propres droits.  
**Voie de préférence (recherche)** : `local_file`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 35. Google Drive — `google-drive`

**Familles** : Cloud documentaire (`10`).  
**Portée déclarée** : Fichiers, commentaires, versions selon scopes.  
**Préconditions déclarées** : Consentement Google, OAuth et autorisations fichier.  
**Limites déclarées** : Scopes minimaux; ne pas copier contenu privé vers ChatGPT sans permission.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 36. Microsoft SharePoint / OneDrive — `microsoft-sharepoint-onedrive`

**Familles** : Cloud documentaire (`10`).  
**Portée déclarée** : Fichiers, sites, métadonnées et versions.  
**Préconditions déclarées** : Microsoft Graph et autorisations tenant.  
**Limites déclarées** : Respecter ACL et frontières de tenants.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 37. Amazon S3 — `amazon-s3`

**Familles** : Cloud documentaire, Lacs analytiques (`10, 17`).  
**Portée déclarée** : Objets et versions, métadonnées.  
**Préconditions déclarées** : IAM scoped read-only; versions S3 facultatives.  
**Limites déclarées** : Objet accessible ne garantit pas droit de transformation/partage.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 38. GitHub — `github`

**Familles** : Dépôts de code, Gestion de projets et tickets (`11, 12`).  
**Portée déclarée** : Dépôts, commits, issues, discussions.  
**Préconditions déclarées** : Git clone/REST/GraphQL selon permissions.  
**Limites déclarées** : Licences de code, jetons, données privées.  
**Voie de préférence (recherche)** : `git_snapshot`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `official_docs_checked` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `git_snapshot` / Clone ou archive Git à révision fixe (lanes L5) — `candidate_requires_verification`.
- `api_read` / API de lecture officielle (lanes L2) — `official_docs_checked`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Références du registre** : <https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api>.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 39. GitLab — `gitlab`

**Familles** : Dépôts de code, Gestion de projets et tickets (`11, 12`).  
**Portée déclarée** : Dépôts, merges, tickets.  
**Préconditions déclarées** : Git et API projet; scopes .  
**Limites déclarées** : Instances auto-hébergées peuvent différer.  
**Voie de préférence (recherche)** : `git_snapshot`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `official_docs_checked` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `git_snapshot` / Clone ou archive Git à révision fixe (lanes L5) — `candidate_requires_verification`.
- `api_read` / API de lecture officielle (lanes L2) — `official_docs_checked`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Références du registre** : <https://docs.gitlab.com/api/projects/>.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 40. Bitbucket — `bitbucket`

**Familles** : Dépôts de code (`11`).  
**Portée déclarée** : Code, commits, tickets.  
**Préconditions déclarées** : Accès projet/branch; API selon édition.  
**Limites déclarées** : Restrictions dépôt privé et licences.  
**Voie de préférence (recherche)** : `git_snapshot`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `git_snapshot` / Clone ou archive Git à révision fixe (lanes L5) — `candidate_requires_verification`.
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 41. Jira — `jira`

**Familles** : Gestion de projets et tickets (`12`).  
**Portée déclarée** : Tickets, commentaires, statuts.  
**Préconditions déclarées** : OAuth/API token ou export approuvé.  
**Limites déclarées** : PII, champs personnalisés, restrictions de projet.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 42. Linear — `linear`

**Familles** : Gestion de projets et tickets (`12`).  
**Portée déclarée** : Issues, workflows et équipes.  
**Préconditions déclarées** : API GraphQL et droits d'espace.  
**Limites déclarées** : Données de projet privées.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 43. Acomba — `acomba`

**Familles** : ERP et comptabilité PME (`13`).  
**Portée déclarée** : Grand livre, écritures, clients, factures.  
**Préconditions déclarées** : Exports utilisateur; SDK/ODBC selon édition et licence à vérifier.  
**Limites déclarées** : Données comptables sensibles; facture != paiement.  
**Voie de préférence (recherche)** : `user_export`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `database_read` / Requête SQL/ODBC en lecture seule (lanes L6) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 44. QuickBooks Online — `quickbooks-online`

**Familles** : ERP et comptabilité PME (`13`).  
**Portée déclarée** : Transactions, comptes, factures.  
**Préconditions déclarées** : API Intuit OAuth et scopes dédiés.  
**Limites déclarées** : PII et données financières; droit de partage distinct.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 45. Xero — `xero`

**Familles** : ERP et comptabilité PME (`13`).  
**Portée déclarée** : Ledger, journaux, factures.  
**Préconditions déclarées** : OAuth/API Xero et scopes.  
**Limites déclarées** : Limites d'API et confidentialité.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 46. Sage — `sage`

**Familles** : ERP et comptabilité PME (`13`).  
**Portée déclarée** : Écritures et documents selon produit.  
**Préconditions déclarées** : SDK/API varie fortement selon édition.  
**Limites déclarées** : Ne pas présumer une API uniforme Sage.  
**Voie de préférence (recherche)** : `user_export`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `database_read` / Requête SQL/ODBC en lecture seule (lanes L6) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 47. SAP — `sap`

**Familles** : ERP/CRM entreprise (`14`).  
**Portée déclarée** : ERP et objets métier.  
**Préconditions déclarées** : OData/BAPI/IDoc selon modules et licences.  
**Limites déclarées** : Processus et ACL propriétaires.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `database_read` / Requête SQL/ODBC en lecture seule (lanes L6) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 48. Salesforce — `salesforce`

**Familles** : ERP/CRM entreprise (`14`).  
**Portée déclarée** : CRM, relations et activités.  
**Préconditions déclarées** : API SOQL/OAuth et permissions objet/champ.  
**Limites déclarées** : Données personnelles et métadonnées custom.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 49. Microsoft Dynamics — `microsoft-dynamics`

**Familles** : ERP/CRM entreprise (`14`).  
**Portée déclarée** : ERP/CRM, Dataverse.  
**Préconditions déclarées** : API selon produit et tenant.  
**Limites déclarées** : Sécurité et champs sensibles.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 50. Odoo — `odoo`

**Familles** : ERP/CRM entreprise (`14`).  
**Portée déclarée** : Objets ERP, ventes, stocks.  
**Préconditions déclarées** : API selon version/plan.  
**Limites déclarées** : ACL par modèle et droits de données.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 51. Shopify — `shopify`

**Familles** : Commerce et inventaires (`15`).  
**Portée déclarée** : Produits, commandes, inventaire.  
**Préconditions déclarées** : API admin sous scopes et consentement commerçant.  
**Limites déclarées** : Données consommateurs et quotas.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 52. WooCommerce — `woocommerce`

**Familles** : Commerce et inventaires (`15`).  
**Portée déclarée** : Produits, commandes, variations.  
**Préconditions déclarées** : REST API avec clé du magasin.  
**Limites déclarées** : Données clients privées.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 53. PostgreSQL / MySQL — `postgresql-mysql`

**Familles** : Bases relationnelles (`16`).  
**Portée déclarée** : Tables, vues, métadonnées relationnelles.  
**Préconditions déclarées** : Compte read-only, TLS, snapshot cohérent.  
**Limites déclarées** : Ne pas exécuter requêtes non bornées.  
**Voie de préférence (recherche)** : `database_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `database_read` / Requête SQL/ODBC en lecture seule (lanes L6) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 54. SQL Server / Oracle — `sql-server-oracle`

**Familles** : Bases relationnelles (`16`).  
**Portée déclarée** : Tables, procédures, vues.  
**Préconditions déclarées** : ODBC/JDBC/driver et permissions explicites.  
**Limites déclarées** : PII, charge serveur, cohérence transactionnelle.  
**Voie de préférence (recherche)** : `database_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `database_read` / Requête SQL/ODBC en lecture seule (lanes L6) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 55. Snowflake — `snowflake`

**Familles** : Lacs analytiques (`17`).  
**Portée déclarée** : Tables analytiques et vues.  
**Préconditions déclarées** : Rôles lecture et warehouse/quota.  
**Limites déclarées** : Frais de requêtes, gouvernance catalogue.  
**Voie de préférence (recherche)** : `database_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `database_read` / Requête SQL/ODBC en lecture seule (lanes L6) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 56. BigQuery — `bigquery`

**Familles** : Lacs analytiques (`17`).  
**Portée déclarée** : Tables et datasets analytiques.  
**Préconditions déclarées** : IAM datasets et limites de coût.  
**Limites déclarées** : Coût, données sensibles, résidences.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 57. Databricks — `databricks`

**Familles** : Lacs analytiques (`17`).  
**Portée déclarée** : Lakehouse, Delta tables.  
**Préconditions déclarées** : Jeton/compte scoped.  
**Limites déclarées** : Contrôle UC et gouvernance.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 58. Neo4j — `neo4j`

**Familles** : Graphes d’entreprise (`18`).  
**Portée déclarée** : Graphes de nœuds et relations.  
**Préconditions déclarées** : Cypher READ-only, rôle/base dédiés.  
**Limites déclarées** : Graphes sensibles, sémantique non équivalente à Kristal.  
**Voie de préférence (recherche)** : `database_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `database_read` / Requête SQL/ODBC en lecture seule (lanes L6) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 59. RDF / SPARQL endpoint — `rdf-sparql-endpoint`

**Familles** : Graphes d’entreprise, Références fédérées externes (`18, 36`).  
**Portée déclarée** : RDF, ontologies, vocabulaires.  
**Préconditions déclarées** : Endpoint/documentation et droits de requête.  
**Limites déclarées** : Identifiants externes pas canoniques.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 60. IMAP / MBOX — `imap-mbox`

**Familles** : Courriels et discussions (`19`).  
**Portée déclarée** : Messages, pièces jointes, conversations.  
**Préconditions déclarées** : Consentement propriétaire et autorisations boîte.  
**Limites déclarées** : Très fortes contraintes confidentialité.  
**Voie de préférence (recherche)** : `user_export`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 61. Slack — `slack`

**Familles** : Courriels et discussions (`19`).  
**Portée déclarée** : Canaux, fils et réactions.  
**Préconditions déclarées** : App scopes et export légal.  
**Limites déclarées** : Données d'équipes et personnes.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 62. Microsoft Teams — `microsoft-teams`

**Familles** : Courriels et discussions (`19`).  
**Portée déclarée** : Messages, réunions et fichiers.  
**Préconditions déclarées** : Graph API et politiques administrateur.  
**Limites déclarées** : PII, transcriptions privées, rétention.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 63. Moodle — `moodle`

**Familles** : Éducation (`20`).  
**Portée déclarée** : Cours, ressources, évaluations.  
**Préconditions déclarées** : Webservices par rôle.  
**Limites déclarées** : Dossiers étudiants protégés.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 64. Canvas LMS — `canvas-lms`

**Familles** : Éducation (`20`).  
**Portée déclarée** : Cours, devoirs, inscriptions.  
**Préconditions déclarées** : API Canvas et jetons de compte.  
**Limites déclarées** : Confidentialité scolaire.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 65. Serveur FHIR — `serveur-fhir`

**Familles** : Santé (`21`).  
**Portée déclarée** : Resources santé FHIR.  
**Préconditions déclarées** : SMART on FHIR/OAuth et consentement.  
**Limites déclarées** : Données hautement sensibles; pas d'envoi à ChatGPT par défaut.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `not_recommended`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 66. HL7/DICOM institutionnel — `hl7-dicom-institutionnel`

**Familles** : Santé, Images/vidéos/audio (`21, 27`).  
**Portée déclarée** : Messages, imagerie, dossiers cliniques.  
**Préconditions déclarées** : Accord institutionnel, anonymisation, intégrité.  
**Limites déclarées** : Données cliniques; préserver étude/patient.  
**Voie de préférence (recherche)** : `local_file`. **Politique IA du registre** : `not_recommended`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 67. LegisQuébec — `legisqu-bec`

**Familles** : Droit et administration (`22`).  
**Portée déclarée** : Lois et règlements.  
**Préconditions déclarées** : Examiner accès officiel et licences.  
**Limites déclarées** : Version à date, texte consolidé vs historique.  
**Voie de préférence (recherche)** : `federated_ref`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 68. CanLII — `canlii`

**Familles** : Droit et administration (`22`).  
**Portée déclarée** : Jurisprudence et références.  
**Préconditions déclarées** : Accès/licences propres aux collections.  
**Limites déclarées** : Restrictions sur collecte et redistribution.  
**Voie de préférence (recherche)** : `federated_ref`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 69. OpenStreetMap — `openstreetmap`

**Familles** : Cartographie/GIS (`23`).  
**Portée déclarée** : Objets géographiques et versions.  
**Préconditions déclarées** : Overpass/planet/replication selon charge.  
**Limites déclarées** : ODbL, attribution, limites de requête.  
**Voie de préférence (recherche)** : `bulk_export`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 70. WFS/GeoJSON municipal — `wfs-geojson-municipal`

**Familles** : Cartographie/GIS (`23`).  
**Portée déclarée** : Données géospatiales, couches.  
**Préconditions déclarées** : WFS/WMS/API locale et licences.  
**Limites déclarées** : CRS, version géographique, géodonnées sensibles.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 71. NOAA — `noaa`

**Familles** : Climat et observation Terre (`24`).  
**Portée déclarée** : Données météo/climat.  
**Préconditions déclarées** : Catalogues et APIs selon produit.  
**Limites déclarées** : Unités, période, qualité de mesures.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 72. Copernicus — `copernicus`

**Familles** : Climat et observation Terre (`24`).  
**Portée déclarée** : Imagerie satellite et séries.  
**Préconditions déclarées** : Accès selon service Copernicus.  
**Limites déclarées** : Volumes, résolution, licence de produit.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 73. Broker MQTT — `broker-mqtt`

**Familles** : IoT et industrie, Flux d’événements (`25, 31`).  
**Portée déclarée** : Télémétrie de dispositifs.  
**Préconditions déclarées** : Identité du broker et droits topics.  
**Limites déclarées** : Horodatage, doublons et secrets IoT.  
**Voie de préférence (recherche)** : `events`. **Politique IA du registre** : `not_recommended`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `events` / Webhooks ou flux d’événements (lanes L7) — `candidate_requires_verification`.
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 74. Serveur OPC UA — `serveur-opc-ua`

**Familles** : IoT et industrie (`25`).  
**Portée déclarée** : Mesures et événements industriels.  
**Préconditions déclarées** : Certificats et autorisation de nœuds.  
**Limites déclarées** : Environnement opérationnel critique.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `not_recommended`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `events` / Webhooks ou flux d’événements (lanes L7) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 75. LIMS / ELN — `lims-eln`

**Familles** : Laboratoires scientifiques (`26`).  
**Portée déclarée** : Expériences, échantillons, journaux.  
**Préconditions déclarées** : Export laboratoire ou API fournisseur.  
**Limites déclarées** : PII et propriété intellectuelle.  
**Voie de préférence (recherche)** : `user_export`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 76. IIIF collections patrimoniales — `iiif-collections-patrimoniales`

**Familles** : Images/vidéos/audio, Archives institutionnelles (`27, 28`).  
**Portée déclarée** : Manifests images et métadonnées.  
**Préconditions déclarées** : IIIF Presentation/Image selon collection.  
**Limites déclarées** : Images protégées; attribution et droits.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 77. Internet Archive — `internet-archive`

**Familles** : Archives institutionnelles (`28`).  
**Portée déclarée** : Collections numérisées et métadonnées.  
**Préconditions déclarées** : API/exports selon collection.  
**Limites déclarées** : Droits variables sur items archivés.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 78. Open Banking autorisé — `open-banking-autoris`

**Familles** : Finances/bancaire (`29`).  
**Portée déclarée** : Transactions et comptes utilisateurs.  
**Préconditions déclarées** : API réglementée, consentement, fournisseurs agréés.  
**Limites déclarées** : Données très sensibles.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `not_recommended`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 79. ISO 20022 / relevés bancaires — `iso-20022-relev-s-bancaires`

**Familles** : Finances/bancaire (`29`).  
**Portée déclarée** : Fichiers de paiements et relevés.  
**Préconditions déclarées** : Export par utilisateur autorisé.  
**Limites déclarées** : Jamais de transfert sensible par défaut.  
**Voie de préférence (recherche)** : `local_file`. **Politique IA du registre** : `not_recommended`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 80. Registres publics d'entreprises — `registres-publics-d-entreprises`

**Familles** : Registres publics et société (`30`).  
**Portée déclarée** : Entités légales et statuts.  
**Préconditions déclarées** : Accès national/provincial spécifique.  
**Limites déclarées** : Périodicité et provenance.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 81. Kafka / CloudEvents — `kafka-cloudevents`

**Familles** : Flux d’événements (`31`).  
**Portée déclarée** : Flux d'événements structurés.  
**Préconditions déclarées** : ACL topics, protocole et version.  
**Limites déclarées** : Replay, ordre et idempotence.  
**Voie de préférence (recherche)** : `events`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `events` / Webhooks ou flux d’événements (lanes L7) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 82. Webhooks métier — `webhooks-m-tier`

**Familles** : Flux d’événements (`31`).  
**Portée déclarée** : Notifications d'applications.  
**Préconditions déclarées** : Authentification de signature et permissions.  
**Limites déclarées** : Webhook n'est pas preuve de vérité.  
**Voie de préférence (recherche)** : `events`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `events` / Webhooks ou flux d’événements (lanes L7) — `candidate_requires_verification`.
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 83. Formulaires et enquêtes — `formulaires-et-enqu-tes`

**Familles** : Saisie humaine structurée (`32`).  
**Portée déclarée** : Déclarations humaines structurées.  
**Préconditions déclarées** : Consentement des répondants et finalité.  
**Limites déclarées** : Données subjectives/PII; ne pas transformer en faits.  
**Voie de préférence (recherche)** : `user_export`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
- `manual_paste` / Copier-coller autorisé (lanes L1) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 84. Simulation / jumeaux numériques — `simulation-jumeaux-num-riques`

**Familles** : Simulation et jumeaux numériques (`33`).  
**Portée déclarée** : Modèles, paramètres, résultats simulés.  
**Préconditions déclarées** : Licence de modèle et schéma versionné.  
**Limites déclarées** : Simulation != observation réelle.  
**Voie de préférence (recherche)** : `user_export`. **Politique IA du registre** : `local_only_until_privacy_review`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 85. Reddit — `reddit`

**Familles** : Réseaux sociaux/communautés (`34`).  
**Portée déclarée** : Posts, commentaires, métadonnées.  
**Préconditions déclarées** : API et accords selon usage.  
**Limites déclarées** : Identité/PII et conditions de réutilisation.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 86. Stack Exchange — `stack-exchange`

**Familles** : Réseaux sociaux/communautés (`34`).  
**Portée déclarée** : Questions, réponses, votes.  
**Préconditions déclarées** : API/licence d'attribution.  
**Limites déclarées** : Votes et réponses ne garantissent pas vérité.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
- `bulk_export` / Export massif / dump (lanes L4) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 87. YouTube — `youtube`

**Familles** : Flux et catalogues multimédias (`35`).  
**Portée déclarée** : Vidéos et métadonnées; sous-titres selon droits.  
**Préconditions déclarées** : API Google, OAuth et quotas pour opérations protégées.  
**Limites déclarées** : API vidéos != accès libre à toutes transcriptions.  
**Voie de préférence (recherche)** : `api_read`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `official_docs_checked` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `api_read` / API de lecture officielle (lanes L2) — `official_docs_checked`.
- `rss_atom` / Flux RSS/Atom (lanes L3) — `candidate_requires_verification`.
- `user_export` / Export du compte utilisateur (lanes L1, L4) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Références du registre** : <https://developers.google.com/youtube/data/getting-started>.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 88. Podcasts RSS — `podcasts-rss`

**Familles** : Flux et catalogues multimédias (`35`).  
**Portée déclarée** : Épisodes, enclosures, descriptions.  
**Préconditions déclarées** : Flux et licence audio.  
**Limites déclarées** : Transcription à obtenir/créer avec droit.  
**Voie de préférence (recherche)** : `rss_atom`. **Politique IA du registre** : `permitted_text_only`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `rss_atom` / Flux RSS/Atom (lanes L3) — `candidate_requires_verification`.
- `local_file` / Fichier remis localement (lanes L1) — `candidate_requires_verification`.
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

### 89. Référence fédérée externe — `r-f-rence-f-d-r-e-externe`

**Familles** : Références fédérées externes (`36`).  
**Portée déclarée** : Référence et pointeur vers système propriétaire.  
**Préconditions déclarées** : Disponibilité, ACL, version et politique source.  
**Limites déclarées** : Lien n'est pas licence ou autorité.  
**Voie de préférence (recherche)** : `federated_ref`. **Politique IA du registre** : `metadata_only_by_default`.  
**Niveau de documentation** : `candidate_requires_verification` ; **connecteur** : `not_certified` ; **autorisation propriétaire** : `not_established`.  
**Voies envisagées** :
- `federated_ref` / Référence fédérée / lien stable (lanes L8) — `candidate_requires_verification`.
- `api_read` / API de lecture officielle (lanes L2) — `candidate_requires_verification`.
**Critère d’activation cible** : obtenir la permission adéquate, vérifier les capacités et limites sur un compte/snapshot de test, exécuter les tests positifs/négatifs et l’export ChatGPT permis; sinon conserver `BLOCKED` avec une alternative sans contournement.

## Règles de maintenance

La découverte et les modifications de termes de service imposent la revalidation d’une fiche. Conserver : URL officielle, date, version API, licence/conditions par usage, type de données, quotas, consentement des utilisateurs, fixtures, tests de refus, mainteneur, date de révision. Aucune nouvelle version de registre ne doit transformer `candidate_requires_verification` en `implemented` automatiquement.
