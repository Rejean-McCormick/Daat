# 05 — Couverture fonctionnelle des 36 familles de sources

**Source** : les 36 familles du registre DaaT et leur association aux 89 profils. Une famille n’équivaut pas à un connecteur unique.

| ID | Famille | Exemples du dépôt | Profils répertoriés | Obligation de couverture cible |
|---|---|---|---:|---|
| 01 | Références bibliographiques | PhilPapers, OpenAlex, Crossref | 8 | Route validée ou refus motivé pour chaque profil |
| 02 | Archives académiques OA | PhilArchive, arXiv, dépôts institutionnels | 10 | Route validée ou refus motivé pour chaque profil |
| 03 | Bibliothèques et catalogues | WorldCat, catalogues universitaires, BAnQ | 3 | Route validée ou refus motivé pour chaque profil |
| 04 | Bases de connaissances publiques | Wikidata, bases RDF, thésaurus SKOS | 2 | Route validée ou refus motivé pour chaque profil |
| 05 | Encyclopédies et wikis | Wikipédia, MediaWiki, wikis internes | 2 | Route validée ou refus motivé pour chaque profil |
| 06 | Sites et articles Web | revues, médias, portails spécialisés | 6 | Route validée ou refus motivé pour chaque profil |
| 07 | Jeux de données ouverts | portails CKAN/DCAT, data.gouv, StatCan | 3 | Route validée ou refus motivé pour chaque profil |
| 08 | PDF et documents locaux | dossiers d’entreprise, littérature grise | 3 | Route validée ou refus motivé pour chaque profil |
| 09 | Archives de documents | dossiers ZIP, tar, disques, GED historiques | 2 | Route validée ou refus motivé pour chaque profil |
| 10 | Cloud documentaire | Google Drive, SharePoint, OneDrive, S3 | 3 | Route validée ou refus motivé pour chaque profil |
| 11 | Dépôts de code | GitHub, GitLab, Bitbucket, Git local | 3 | Route validée ou refus motivé pour chaque profil |
| 12 | Gestion de projets et tickets | GitHub Issues, Jira, Linear, Redmine | 4 | Route validée ou refus motivé pour chaque profil |
| 13 | ERP et comptabilité PME | Acomba, Sage, QuickBooks, Xero | 4 | Route validée ou refus motivé pour chaque profil |
| 14 | ERP/CRM entreprise | SAP, Dynamics, Salesforce, Odoo | 4 | Route validée ou refus motivé pour chaque profil |
| 15 | Commerce et inventaires | Shopify, WooCommerce, POS/WMS | 2 | Route validée ou refus motivé pour chaque profil |
| 16 | Bases relationnelles | PostgreSQL, MySQL, SQL Server, Oracle, SQLite | 2 | Route validée ou refus motivé pour chaque profil |
| 17 | Lacs analytiques | S3, BigQuery, Snowflake, Databricks | 4 | Route validée ou refus motivé pour chaque profil |
| 18 | Graphes d’entreprise | Neo4j, RDF triplestores, taxonomies | 3 | Route validée ou refus motivé pour chaque profil |
| 19 | Courriels et discussions | IMAP, MBOX, Teams, Slack | 3 | Route validée ou refus motivé pour chaque profil |
| 20 | Éducation | Moodle, Canvas LMS, SCORM, xAPI | 2 | Route validée ou refus motivé pour chaque profil |
| 21 | Santé | FHIR, HL7 v2, CDA, DICOM | 2 | Route validée ou refus motivé pour chaque profil |
| 22 | Droit et administration | lois, règlements, jurisprudence, contrats | 2 | Route validée ou refus motivé pour chaque profil |
| 23 | Cartographie/GIS | OpenStreetMap, municipalités, cadastre | 3 | Route validée ou refus motivé pour chaque profil |
| 24 | Climat et observation Terre | NOAA, Copernicus, météo, satellites | 2 | Route validée ou refus motivé pour chaque profil |
| 25 | IoT et industrie | SCADA, MQTT, OPC UA, automates, maintenance | 2 | Route validée ou refus motivé pour chaque profil |
| 26 | Laboratoires scientifiques | LIMS/ELN, instruments, bioinformatique | 1 | Route validée ou refus motivé pour chaque profil |
| 27 | Images/vidéos/audio | médiathèques, fonds patrimoniaux | 2 | Route validée ou refus motivé pour chaque profil |
| 28 | Archives institutionnelles | musées, patrimoine, généalogie | 3 | Route validée ou refus motivé pour chaque profil |
| 29 | Finances/bancaire | API bancaire autorisée, ISO 20022, ERP | 2 | Route validée ou refus motivé pour chaque profil |
| 30 | Registres publics et société | élections, entreprises, indicateurs, démographie | 3 | Route validée ou refus motivé pour chaque profil |
| 31 | Flux d’événements | Kafka, Webhooks, CloudEvents, logs | 3 | Route validée ou refus motivé pour chaque profil |
| 32 | Saisie humaine structurée | formulaires, témoignages, observations terrain | 1 | Route validée ou refus motivé pour chaque profil |
| 33 | Simulation et jumeaux numériques | modèles industriels, scénarios | 1 | Route validée ou refus motivé pour chaque profil |
| 34 | Réseaux sociaux/communautés | plateformes et forums autorisés | 2 | Route validée ou refus motivé pour chaque profil |
| 35 | Flux et catalogues multimédias | podcasts, chaînes, playlists, RSS | 3 | Route validée ou refus motivé pour chaque profil |
| 36 | Références fédérées externes | catalogues d’autres écosystèmes | 2 | Route validée ou refus motivé pour chaque profil |

## Couverture qualitative par famille

### 01 — Références bibliographiques
**Profils rattachés** : PhilPapers, OpenAlex, Crossref, Semantic Scholar, PubMed / NCBI, DOAJ, Zotero, ORCID.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `federated_ref`, `harvest_oai_pmh`, `licensed_batch`, `local_file`, `manual_paste`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 02 — Archives académiques OA
**Profils rattachés** : PhilPapers, PhilArchive, arXiv, PubMed / NCBI, Europe PMC, HAL, Zenodo, OSF, SSRN, bioRxiv.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `federated_ref`, `harvest_oai_pmh`, `licensed_batch`, `local_file`, `manual_paste`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 03 — Bibliothèques et catalogues
**Profils rattachés** : Zotero, WorldCat, BAnQ / catalogues québécois.  
**Méthodes candidates présentes dans le registre** : `api_read`, `federated_ref`, `harvest_oai_pmh`, `licensed_batch`, `local_file`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 04 — Bases de connaissances publiques
**Profils rattachés** : Wikidata, DBpedia / RDF public.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `federated_ref`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 05 — Encyclopédies et wikis
**Profils rattachés** : Wikipedia, MediaWiki autonome.  
**Méthodes candidates présentes dans le registre** : `api_read`, `authenticated_web`, `bulk_export`, `federated_ref`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 06 — Sites et articles Web
**Profils rattachés** : Medium, WordPress, Ghost, Substack, Blogger, Flux RSS/Atom générique.  
**Méthodes candidates présentes dans le registre** : `api_read`, `authenticated_web`, `federated_ref`, `manual_paste`, `rss_atom`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 07 — Jeux de données ouverts
**Profils rattachés** : CKAN, Statistique Canada, Portail données ouvertes municipal.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `local_file`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 08 — PDF et documents locaux
**Profils rattachés** : Zenodo, PDF fourni par utilisateur, DOCX/texte fourni par utilisateur.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `local_file`, `manual_paste`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 09 — Archives de documents
**Profils rattachés** : OSF, Archives ZIP/TAR.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `local_file`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 10 — Cloud documentaire
**Profils rattachés** : Google Drive, Microsoft SharePoint / OneDrive, Amazon S3.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `federated_ref`, `local_file`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 11 — Dépôts de code
**Profils rattachés** : GitHub, GitLab, Bitbucket.  
**Méthodes candidates présentes dans le registre** : `api_read`, `git_snapshot`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 12 — Gestion de projets et tickets
**Profils rattachés** : GitHub, GitLab, Jira, Linear.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `git_snapshot`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 13 — ERP et comptabilité PME
**Profils rattachés** : Acomba, QuickBooks Online, Xero, Sage.  
**Méthodes candidates présentes dans le registre** : `api_read`, `database_read`, `local_file`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 14 — ERP/CRM entreprise
**Profils rattachés** : SAP, Salesforce, Microsoft Dynamics, Odoo.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `database_read`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 15 — Commerce et inventaires
**Profils rattachés** : Shopify, WooCommerce.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 16 — Bases relationnelles
**Profils rattachés** : PostgreSQL / MySQL, SQL Server / Oracle.  
**Méthodes candidates présentes dans le registre** : `bulk_export`, `database_read`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 17 — Lacs analytiques
**Profils rattachés** : Amazon S3, Snowflake, BigQuery, Databricks.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `database_read`, `federated_ref`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 18 — Graphes d’entreprise
**Profils rattachés** : DBpedia / RDF public, Neo4j, RDF / SPARQL endpoint.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `database_read`, `federated_ref`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 19 — Courriels et discussions
**Profils rattachés** : IMAP / MBOX, Slack, Microsoft Teams.  
**Méthodes candidates présentes dans le registre** : `api_read`, `local_file`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 20 — Éducation
**Profils rattachés** : Moodle, Canvas LMS.  
**Méthodes candidates présentes dans le registre** : `api_read`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 21 — Santé
**Profils rattachés** : Serveur FHIR, HL7/DICOM institutionnel.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `federated_ref`, `local_file`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 22 — Droit et administration
**Profils rattachés** : LegisQuébec, CanLII.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `federated_ref`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 23 — Cartographie/GIS
**Profils rattachés** : Portail données ouvertes municipal, OpenStreetMap, WFS/GeoJSON municipal.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `local_file`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 24 — Climat et observation Terre
**Profils rattachés** : NOAA, Copernicus.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 25 — IoT et industrie
**Profils rattachés** : Broker MQTT, Serveur OPC UA.  
**Méthodes candidates présentes dans le registre** : `api_read`, `events`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 26 — Laboratoires scientifiques
**Profils rattachés** : LIMS / ELN.  
**Méthodes candidates présentes dans le registre** : `api_read`, `local_file`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 27 — Images/vidéos/audio
**Profils rattachés** : HL7/DICOM institutionnel, IIIF collections patrimoniales.  
**Méthodes candidates présentes dans le registre** : `api_read`, `federated_ref`, `local_file`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 28 — Archives institutionnelles
**Profils rattachés** : BAnQ / catalogues québécois, IIIF collections patrimoniales, Internet Archive.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `federated_ref`, `harvest_oai_pmh`, `local_file`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 29 — Finances/bancaire
**Profils rattachés** : Open Banking autorisé, ISO 20022 / relevés bancaires.  
**Méthodes candidates présentes dans le registre** : `api_read`, `federated_ref`, `local_file`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 30 — Registres publics et société
**Profils rattachés** : Statistique Canada, Portail données ouvertes municipal, Registres publics d'entreprises.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `federated_ref`, `local_file`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 31 — Flux d’événements
**Profils rattachés** : Broker MQTT, Kafka / CloudEvents, Webhooks métier.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `events`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 32 — Saisie humaine structurée
**Profils rattachés** : Formulaires et enquêtes.  
**Méthodes candidates présentes dans le registre** : `local_file`, `manual_paste`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 33 — Simulation et jumeaux numériques
**Profils rattachés** : Simulation / jumeaux numériques.  
**Méthodes candidates présentes dans le registre** : `api_read`, `local_file`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 34 — Réseaux sociaux/communautés
**Profils rattachés** : Reddit, Stack Exchange.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `federated_ref`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 35 — Flux et catalogues multimédias
**Profils rattachés** : Flux RSS/Atom générique, YouTube, Podcasts RSS.  
**Méthodes candidates présentes dans le registre** : `api_read`, `federated_ref`, `local_file`, `rss_atom`, `user_export`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

### 36 — Références fédérées externes
**Profils rattachés** : RDF / SPARQL endpoint, Référence fédérée externe.  
**Méthodes candidates présentes dans le registre** : `api_read`, `bulk_export`, `federated_ref`.  
**Épreuve de validation** : entrée représentative (ou fixture propriétaire si données privées), choix motivé de méthode, droits, import ou référence, conservation de granularité, scénario négatif, dossier ChatGPT sans fuite.

## Grille universelle de qualification

Pour **chaque famille** : contrôler 1) découvertes, 2) droit, 3) accès/fallback, 4) formats, 5) provenance, 6) révisions, 7) privacy, 8) export ChatGPT, 9) refus, 10) réexécution. L’échec d’un seul volet critique interdit la mention « opérationnel ».
