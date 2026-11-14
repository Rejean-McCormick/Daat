# DaAT — Registre des accès aux plateformes (recherche v1)

**Date : 14 novembre 2026 · Statut : RESEARCH_CATALOGUE_ONLY, aucun accès canonique approuvé.**

Ce registre complète `docs/27-SOURCE-TAXONOMY-AND-REGISTRY.md` et les **36 familles existantes**. Il décrit **89 profils de plateformes et types de sources** : 14 avec documentation officielle consultée, 75 pistes à vérifier au cas par cas. **Aucun** des 89 profils ne déclare un connecteur opérationnel DaAT.

## Décision de conception : plusieurs chemins par plateforme

L'utilisateur choisit sa source. Un logiciel propriétaire de collecte/connexion ou un utilisateur authentifié obtient *seulement ce qu'il est autorisé à lire et partager*. DaaT reçoit des références et des propositions bornées, sans voler une session, scraper une paywall ou s'approprier les originaux. Quand la source n'offre que des métadonnées, la boucle ChatGPT produit des propositions *sur ces métadonnées*, jamais une lecture imaginaire du texte complet.

| Priorité de sélection | Voie d'acquisition | Utilisation |
|---|---|---|
| 1 | API/harvesting sous droits explicites | Découverte, métadonnées, lots et synchronisation sans copie manuelle |
| 2 | RSS/Atom et notifications | Surveillance de nouveaux items; souvent résumés seulement |
| 3 | Exports de compte/collection (ZIP/JSON/RIS/CSV) | Lots autorisés; idéal pour auteurs, bibliographies et archives personnelles |
| 4 | Référence fédérée | Garder le contenu chez le propriétaire quand la copie est inutile/interdite |
| 5 | Fichier, extrait ou copier-coller remis par utilisateur | Mode universel de repli, jamais un contournement de droits |

## PhilPapers / PhilArchive : chemins documentés

- **PhilPapers** fournit une API JSON notamment pour les catégories, une API de sous-ensembles bibliographiques *sous conditions*, et un accès OAI-PMH sur le contenu OA décrit. Les autorisations de redistribution substantielle exigent une attention particulière et éventuellement un accord écrit.
- **PhilArchive** et les contenus OA représentent une frontière différente des références commerciales indexées par PhilPapers. Le flux OAI-PMH n'autorise pas automatiquement à redistribuer les textes téléchargés.
- **Plan produit :** synchroniser les références éligibles (identifiants/versions), enrichir par DOI via Crossref/OpenAlex si permis, puis demander la version intégrale à son détenteur sous licence. Ne pas inventer les assertions d'un article à partir de sa seule notice.

Documentation :
- https://philpapers.org/help/api/
- https://philpapers.org/help/api/json.html
- https://philpapers.org/help/oai.html
- https://philpapers.org/help/terms.html

## Medium : chemins documentés

- **RSS** pour profils, publications et sujets; fonctionne pour découvrir plusieurs articles sans les copier un par un. Les textes payants ne sont pas fournis intégralement dans le RSS.
- **Export ZIP/HTML du compte** par son propriétaire; pratique pour ingérer un corpus personnel autorisé en lot.
- **Lecture authentifiée manuelle** et texte/extrait fourni par l'utilisateur, **uniquement si la communication à ChatGPT et la conservation dans kOA sont autorisées**; aucune extraction de cookies ni contournement de paywall.
- **API historique :** Medium indique ne plus émettre de nouveaux jetons d'intégration; ne pas planifier un nouveau connecteur basé sur cette API.

Documentation :
- https://help.medium.com/hc/en-us/articles/214874118-Using-RSS-feeds-of-profiles-publications-and-topics/
- https://help.medium.com/hc/en-us/articles/115004745787-Export-your-account-data
- https://help.medium.com/hc/en-us/articles/213480228-API-Importing

## Contrat de qualité de la source pour la boucle ChatGPT

Toute proposition doit conserver :

1. **Source et droit** : plateforme, URL/identifiant, auteur, propriétaire des droits, consentement/licence applicables et périmètre de transmission.
2. **Granularité** : `reference_only`, `abstract`, `excerpt`, `full_text_authorized` ou `dataset`; pas de glissement silencieux.
3. **Accès** : méthode, utilisateur ou connecteur autorisé, date et identifiant de révision/snapshot; ne jamais enregistrer de cookie, token ou mot de passe.
4. **Preuves** : identifiant de fragment/passage, offsets et hash du contenu *autorisé*, exclusions, incertitude, source externe vs interprétation IA.
5. **Contrôle** : vérification déterministe des citations présentes, revue humaine, test de refus, aucun KQ/KP/KA/KS canonique créé directement.

La citation exacte prouve une présence dans le fragment fourni, pas la véracité de l'assertion ni la licence du fragment.

## Maturité des entrées

`official_docs_checked` signifie que des documents officiels définissant **au moins une voie** ont été consultés, **pas** que chacune des voies du profil a été vérifiée ni qu'une API est actuellement accessible depuis l'installation. `candidate_requires_verification` est un candidat d'architecture non confirmé ici. Le champ `access_paths[].doc_status` aide à éviter de considérer un export ou une connexion comme déjà qualifié. Le champ `daat_connector_status` reste `not_certified` pour tous.

## Où continuer

- `docs/data/platform-access-registry.v1.json` : référence structurée multi-voies.
- `docs/data/platform-access-registry.v1.csv` : inventaire éditable avec filtre/recherche.
- `tools/daat_source_access.py` : consultation **hors ligne**, lecture seule, sans compte ni réseau.
- `tests/test_platform_access_registry.py` : contrôles d'intégrité, voies d'accès valides et couverture des 36 familles.
- `LANCER_REGISTRE_SOURCES.pyw` : consultation Windows avec recherche, sans console ni requête réseau (nécessite Python et Tkinter).

**À ne pas confondre :** ce registre est un catalogue opérationnel de recherche, pas une nouvelle norme IK ni un connecteur installé. La prochaine étape est de vérifier chaque fournisseur prioritaire, sa licence et son TCK avant de coder un adaptateur de collecte chez le bon propriétaire.
