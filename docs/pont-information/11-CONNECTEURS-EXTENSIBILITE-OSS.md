# 11 — Connecteurs, SDK hôte, catalogue, licences et Kintsugi

**Statut** : `[PROPOSAL]` pour les connecteurs réseau; les modules locaux de DaaT 0.4.4 doivent être conservés et qualifiés au cas par cas.

## 1. Les 89 profils ne signifient pas 89 implémentations indépendantes

Concevoir **huit capacités d'accès (L1–L8)**, des parseurs/routages par format et des **profiles providers** propres à une plateforme (endpoint, quotas, auth, termes, structure des réponses). Un profil peut être `documented`, `fixture_tested`, `bilateral_tested`, `operational`, `conditional`, `blocked`. Les 36 familles représentent la **couverture de forme des données**, et non 36 protocoles. Un fournisseur peut imposer plusieurs stratégies et niveaux d'accès différents selon son abonnement/identité.

## 2. Contrat de plugin/adapter hôte (concept)

Un adapter candidat déclare : `name`, `version`, `source_profile_id`, `families`, `lanes`, `api_versions`, `auth_method` (référence à l'hôte, jamais secret), `read_scopes`, `data_types`, `granularities`, `term_ref`, `owner`, `license_review`, `refresh_policy`, `pagination`, `cursors`, `max_bytes`, `max_records`, `reliability`, `negative_fixture_set`, `support_state`. **Interdire les scripts arbitraires** fournis par l'utilisateur; mapping DaaT déclaratif en liste blanche.

Actions admissibles chez le propriétaire : `probe` (capacités sans lire de contenu privé), `enumerate` (références permises), `fetch` (représentations bornées, si droits), `checkpoint` (curseur propriétaire), `verify_revision` (contrôle), `revoke` (arrêt et purge). Ce sont des responsabilités internes hôtes, **pas** des verbes HTTP/IK officiellement adoptés.

## 3. Réutilisation OSS selon Kintsugi

Reprendre la stratégie documentée dans `docs/28-KINTSUGI-OSS-INTEGRATION.md` :

| Stratégie | Exemple d'usage cible | Mesures exigées |
|---|---|---|
| **Mimic** | Contract de connecteur, UX de rapprochement, patterns de checkpoint | Recréer le principe, ne pas copier du code sous licence contraire |
| **Annex** | Outil documentaire (Docling/Tika), connecteur Singer soigneusement choisi, service CDC si légitime | Licence exacte + dépendances + image + versions + SBOM + isolation + tests |
| **Reference-only** | Marketplace de connecteurs non qualifiée, fournisseurs propriétaires, documents techniques | Ne pas embarquer code ni octets; signaler les droits |

Candidats de la documentation existante : Docling, Apache Tika, Meltano Singer SDK, dlt, OpenRefine, Debezium, Airbyte, Ontop, NiFi/Apache Hop. **Aucun n'est déclaré préapprouvé par cette liste**. Ne pas introduire automatiquement un nouveau moteur de workflow, un data lake ou une base sémantique.

## 4. Règles de connecteurs par forme

| Classe | Capacité réutilisable | Piège à éviter |
|---|---|---|
| Bibliographie | DOI, ORCID, OAI-PMH, RIS, BibTeX, Dublin Core, paginations | Texte complet supposé à partir du DOI |
| Publication Web | RSS/Atom, WordPress REST, Ghost Content API, export ZIP/HTML | Scraping de paywall et instructions HTML non fiables |
| Archives et fichiers | PDF, DOCX, XML, JSONL, ZIP/TAR, tableaux, provenance de pages | ZIP bomb, PDF actif, perte de tableaux |
| Code/version | Git, commit, API repos, diff, licence dépôt | Branche mutable et autorité implicite |
| ERP/CRM | CSV/JSON/export SDK approuvé/SQL lecture seule | Extraction non transactionnelle ou PII diffusée |
| Collaboration | Drive, SharePoint, Zotero, tickets, messagerie | Scopes trop larges, propagation d'ACL ignorée |
| Données spécialisées | Santé, juridique, géo, IoT, média | Unit/consent/standards spécifiques non vérifiés |

## 5. Lifecycle d'une fiche/connector

`RESEARCH -> DOCUMENTED -> IMPLEMENTED_IN_SANDBOX -> TESTED_WITH_FIXTURES -> RIGHTS_CONFIRMED -> BILATERAL_TESTED -> OPERATIONALLY_QUALIFIED`. Le passage à un état final exige les preuves référencées. Un provider dont la licence restreint l'accès peut rester `REFERENCE_ONLY` ou `CONDITIONAL` tout en étant **correctement pris en charge du point de vue du routage**.

## 6. Dépendances à revoir avant inclusion

Pin exact Git tag/digest, droits de redistribution du logiciel et de ses modèles, transitive dependencies, inventaire SPDX/CycloneDX, notices, modifications, sécurité CVE, risque de télémetrie, déploiement Windows/Linux, CPU/RAM/GPU, coût et plan de retrait. Les obligations d’attribution des composants **sélectionnés** sont archivées dans `THIRD-PARTY-REFERENCES.md` ou le registre OSS propriétaire.
