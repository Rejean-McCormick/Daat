# 07 — Modèle documentaire, provenance, ancrage, rapprochements et droits

**Statut** : `[PROPOSAL]` — modèle logique interne illustratif. Il ne constitue **ni schéma IK/Kit officiel ni une nouvelle autorité de stockage**.

## 1. Entités nécessaires

| Entité | Identité / propriétés indispensables | Pourquoi |
|---|---|---|
| `SourceProfile` | ID, version, famille, méthodes, provenance du catalogue, statut | Différencier profil et accès réel |
| `SourceObject` | Namespace externe, ID, URL, producteur, auteur, dates, langue, type | Référence du propriétaire |
| `AccessEvidence` | Principal host vérifié, tenant, usage, portée, décision, échéance, preuve non secrète | Ne pas confondre login et droit |
| `RepresentationRef` | Référence gardien, media type, révision, checksum local éventuel, licence | Identifier un contenu disponible |
| `EvidenceFragment` | Objet/révision, offsets ou page/ligne/ligne temporelle, citation vérifiable, hash de fragment | Ancrer les propos |
| `NormalizedRecord` | Type, schéma local, champs, unités, transformation/version, pertes, parent refs | Rendre comparable sans inventer |
| `MatchCandidate` | Identifiants externes, score technique, règles, état de revue | Dédoublonnage sans identité canonique |
| `HumanAnnotation` | Commentaire, auteur et rôle, décision, justification, horodatage, sources | Contrôle des interprétations |
| `ContextBundle` | Références sélectionnées, fragments divulguables, avertissements, prompts, manifestes | Objet livré à ChatGPT |
| `DisclosureRecord` | Cible (manuel/API), finalité, consentement/décision, items expurgés, acte de transmission | Ne pas présumer divulgation |
| `OperationalCheckpoint` | Clé d'intention, curseur, état et terminal receipt propriétaire si disponible | Reprise contrôlée |

## 2. Invariants non négociables

1. `source_id` externe ne peut pas devenir un KQ/KP. Tout texte IA et toute donnée acquise sont **non fiables** par défaut.
2. Une notice bibliographique n'est pas un résumé; un résumé n'est pas le contenu d'un article. `content_kind` est conservé par fragment et dans chaque synthèse.
3. L'ancrage exact local doit être vérifiable **sur la représentation autorisée fournie**. Si l'original n'est pas dans la portée du paquet, indiquer `anchor_verification: unavailable` et non `verified`.
4. SHA-256 garantit au mieux l'intégrité de bytes observés sous ce calcul; **ne prouve pas l'authenticité**, la licence, le sens, l'exhaustivité ou l'identité du fournisseur.
5. Toute conversion de format produit un `transform_id` + `transform_version` + avertissements, et conserve les champs exigés; pertes dangereuses = refus ou marquage explicite.
6. Un mapping d'unité, date ou quantité nécessite règle déterministe et provenance de l'unité d'origine; ne jamais supprimer un signe débit/crédit, une timezone ou l'incertitude.
7. Le droit de lire, copier, conserver, transformer et envoyer à un fournisseur IA est **dissocié** pour chaque provenance/révision/tenant.
8. Un document peut avoir plusieurs origines et plusieurs licences; utiliser la **restriction effective** tant qu'une revue de droits ne prouve pas une voie plus permissive.

## 3. Dédoublonnage sans effacer les contradictions

- **Exact** : même identifiant externe qualifié (`DOI`, `PMID`, `arXiv`, source-ID+révision, Git commit/blob, hash sous source connue). Les collisions/erreurs d'ID sont contrôlées.
- **Quasi exact** : normalisation conservatrice d'URL, auteur/date, titre, pagination, checksums des dérivés. Une correction de titre n'est pas la preuve d'un contenu identique.
- **Sémantique candidate** : embeddings / similarité lexicale proposés seulement à la revue; conserver les deux objets et le lien `possibly_same_as` local sans déclaration canonique.
- **Conflits** : éditions divergentes, thèses opposées, résumés différents, titres traduits. Présenter côte à côte et garder les assertions attribuées; ne pas les fusionner.

## 4. Provenance par type de source

| Type | Locator recommandé | Avertissement |
|---|---|---|
| PhilPapers / DOI | ID bibliographique/DOI + provenance de notice + date d'observation | Ne pas prétendre avoir lu l'article |
| Medium | URL/post ID, auteur, flux/ZIP/révision, origine réelle du texte | RSS peut être partiel; paywall ne donne pas de permission |
| PDF | Empreinte du fichier fourni, page, numéro de bloc, offsets | Représentation peut varier avec l'extracteur |
| Git | Repo/remote autorisé, commit, chemin, ligne, blob hash | Branche mutable ne suffit pas |
| Tableur/ERP | Export ID, nom feuille/table, ligne, clé et schéma, date du snapshot | Désidentification nécessaire avant IA |
| Audio/vidéo | Hash média custodian, timecodes, modèle de transcription | Transcription = dérivé non garanti exact |
| Page HTML | URL + timestamp + snapshot/ETag si obtenu, sélecteur/offset | Page mutable; ne pas réutiliser des sélecteurs comme preuve durable |

## 5. Licences / retrait / contamination croisée

Un Context Bundle est **construit pour une destination et finalité précises**. Une source autorisée pour la recherche locale peut être exclue de l'envoi ChatGPT. Les résumés et annotations dérivées d'une source révoquée passent par revue de rétention et de suppression approuvée. Si les fragments sources sont cachés, le système doit conserver des *références de provenance expurgées* ou supprimer conformément au custodian; il ne doit pas inventer une « preuve publique » en remplacement.

## 6. Compatibilité à l'écosystème

Médiathèque conserve les octets selon ses propres autorisations; DaaT transporte des références qualifiées et des dérivés temporaires autorisés. Skope/EncyK peut alimenter certaines références selon contrat réel. Une réception Médiathèque non signée ne transforme pas un contenu en assertion vérifiée. Le lot construit pour ChatGPT n'est **pas** un paquet Kit ni un artefact Kristal.
