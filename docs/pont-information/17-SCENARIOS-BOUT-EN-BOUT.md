# 17 — Parcours de référence intégrés à tester dans la livraison unique

**Statut** : `[PROPOSAL]` — scénarios fonctionnels et fixtures à créer, non preuve d'accès effectif aux fournisseurs.

## SC-01 — PhilPapers → sources de philosophie → contexte ChatGPT

**Entrée** : thème « conscience », mots-clefs, limites de période; identité et finalité. **Découverte** : consulter l'API JSON/OAI-PMH seulement suivant la portée et les termes actuels autorisés; rapporter catégories/DOI/références. **Enrichissement** : recouper avec Crossref/OpenAlex pour métadonnées autorisées, puis associer un texte OA seulement si le contenu et sa licence sont accessibles. **Provenance** : distinguer catalogue PhilPapers, DOI, abstract et texte source, ID du fournisseur, date et révision. **Sortie** : bibliographie, abstract identifiés, passages de texte OA légalement utilisés, questions de recherche et non-réponses. **Refus** : redistribution massive PhilPapers non autorisée ou accès à un article restreint = aucune copie, référence seule. **Tests** : pseudo-DOI, mauvaise licence, faux abstract, duplication et citation inexistante.

## SC-02 — Medium → RSS et export utilisateur → corpus d'articles

**Entrée** : URL de publication/auteur; type d'accès « public RSS » et éventuellement ZIP HTML exporté par le propriétaire. **Découverte** : RSS liste titres, liens, dates et extraits; paywall non interprété comme texte complet. **Import** : l'utilisateur fournit son export ZIP ou contenu autorisé; scanner, extraire et identifier les révisions; pas de connexion automatisée à son compte. **Rapprochement** : articles RSS et ZIP reliés par URL/ID + preuve; conserver les textes seulement sous droits. **Sortie** : corpus différenciant `metadata_only` / `excerpt` / `full_text_authorized`, citation exacte, gabarit comparatif ChatGPT. **Refus** : RSS payant incomplet; utilisateur connecté ne donne pas un droit de redistribution ou de soumission IA. **Tests** : multi-posts, RSS dupliqués, ZIP malicieux, HTML injection, textes sans droit.

## SC-03 — Zotero + DOI / OpenAlex

**Entrée** : export RIS/BibTeX/JSON ou autorisation API Zotero. **Collecte** : bibliothèque, pages/versions, pièce jointe uniquement si droits. **Rapprochement** : DOI exact, traductions et rééditions distinctes, ORCID éventuel sans inférer identité canonique. **Sortie** : bibliographie enrichie, relations et lacunes. **Refus** : accès privé sans token/permission ou pièces jointes interdites. **Tests** : pagination, bibliothèque privée, suppression/retrait, duplications, versions API.

## SC-04 — PDF, DOCX, images, audio

**Entrée** : dossiers et médias explicitement fournis. **Traitement** : détection type, parsers sandboxés, PDF pages, tables, OCR/transcription optionnelle sous droits et modèle versionné, fragments. **Sortie** : citations par page/timecode, avertissements sur extraction non fiable. **Refus** : fichier corrompu, archive bomb, modèle OCR non approuvé. **Tests** : colonnes, tableaux, OCR douteux, fonts, contenu caché, macros, budget.

## SC-05 — GitHub / Git et documentation logicielle

**Entrée** : repository/commit ou snapshot explicitement autorisé. **Collecte** : Git sous révision figée, lecture fichiers/textes/commits, exclusions de secrets. **Traitement** : parse code README/issues seulement si droits API; provenance chemin-ligne-commit. **Sortie** : contexte d'architecture et citations de code autorisées. **Refus** : repo privé sans grant, diffusion de secrets détectés, branche mutable sans snapshot. **Tests** : commits, fichiers déplacés, sous-modules, provenance de diff, token expiré.

## SC-06 — Acomba et comptabilité entreprise

**Entrée** : export CSV/Excel/JSON de l'utilisateur ou connecteur approuvé selon édition. **Traitement** : schéma source exact, unités/devises/dates et débits-crédits, partition par compagnie/année, désidentification avant IA. **Sortie** : tables agrégées/documentées, métadonnées source et questions; jamais écriture ERP. **Refus** : champ critique perdu, PII non masquée, permission de transfert externe absente. **Tests** : devises, TVA, locale FR, négatifs, double transaction, fichiers incohérents.

## SC-07 — Source de santé/éducation privée

**Entrée** : fichier/record privé explicitement autorisé; conformité locale et scope. **Traitement** : contrôle d'identité hôte, minimisation, refus d'envoi IA sans permission documentée, évitement de tout log sensible. **Sortie** : possible dossier local anonymisé validé; sinon `BLOCKED` avec justification. **Tests** : retrait de consentement, fuite de nom, mélange de tenants, délai d'expiration.

## SC-08 — Corpus mixte contradictoire et mise à jour

**Entrée** : une source PhilPapers notice, deux articles Medium dont un complet autorisé, un PDF et un repo Git. **Traitement** : deux theses opposées conservées, citation ancrée, révision du PDF, doublon Media/RSS, manque de texte d'un article répertorié, résumé IA étiqueté. **Sortie** : dossier ChatGPT structuré avec accords/désaccords attribués, questions sans réponse et preuves par segment. **Refus** : tentative de faire passer une notice pour le texte intégral, citation IA inventée, prompt injection. **Tests** : changement de droits entre deux exports, comparer bundles versionnés et exclusion obligatoire.

## SC-09 — Référence seule / source inaccessible

**Entrée** : ressource payante ou URL périmée. **Traitement** : enregistrer les seules métadonnées permises et la date d'observation; proposer action utilisateur compatible. **Sortie** : référence et blocage, aucune fiction. **Tests** : 401/403, paywall, URL non autorisée, licence inconnue.

## SC-10 — Diagnostic de la livraison unique

**Entrée** : corpus de fixtures, source rights et mocks hôtes + tests bilatéraux pour connecteurs activés. **Traitement** : DaaT_Diag doit produire tous les résultats par source/capacité. **Sortie** : preuve expurgée, matrice 89/36, gains/échecs entre campagnes. **Tests** : résultat faux PASS rejeté, manifest modifié rejeté, mauvais tenant refusé, running timeout signalé et non masqué.

## Qualité transversale à prouver

Tous ces scénarios alimentent le **même format contextuel**, les mêmes règles de droits et le même registre. La séparation en scénarios n'est pas un découpage en livraisons successives : ils doivent être réussis ou explicitement et légitimement bloqués lors de **la même revue de fin de projet**.
