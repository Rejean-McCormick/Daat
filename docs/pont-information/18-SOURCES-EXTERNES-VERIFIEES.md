# 18 — Documentation officielle externe vérifiée pour la conception

**Date de consultation** : 14 novembre 2026. Les informations ci-dessous sont des faits issus de documentation officielle consultée, **pas une preuve que DaaT possède l'accès/les clés/les licences**. Le registre DaaT de départ contient 14 profils avec au moins une voie officiellement documentée; la liste ci-dessous est une sélection revue pour les décisions architecturales majeures, **non un audit complet des 89**.

## PhilPapers et PhilArchive

- [API PhilPapers — overview](https://philpapers.org/help/api/) : API de tiers et restrictions de redistribution; contacter l'éditeur pour exceptions et utilisation substantielle.
- [API JSON PhilPapers](https://philpapers.org/help/api/json.html) : taxonomie/feeds et sous-ensembles de métadonnées sous conditions.
- [PhilPapers OAI-PMH](https://philpapers.org/help/oai.html) : la portée est le contenu OA; n'inclut pas toutes les entrées sous licences tierces.
- [Conditions PhilPapers](https://philpapers.org/help/terms.html) : restrictions explicites de téléchargement/repartage d'une portion substantielle de citations et données hors OAI de PhilArchive.

**Conséquence** : séparateur `notice bibliographique` / `abstract accessible` / `article OA autorisé`; aucun miroir général PhilPapers présumé légal.

## Medium

- [Flux RSS Medium](https://help.medium.com/hc/en-us/articles/214874118-Using-RSS-feeds-of-profiles-publications-and-topics) : flux profils, publications, sujets; pas de texte intégral des articles derrière paywall dans RSS.
- [Export personnel Medium](https://help.medium.com/hc/en-us/articles/115004745787-Export-your-account-data) : export des données et histoires du compte en archive ZIP contenant HTML.
- [API/Importing Medium](https://help.medium.com/hc/en-us/articles/213480228-API-Importing) : pas de nouveaux jetons d'intégration API historiques.

**Conséquence** : RSS de découverte, export du compte pour contenu utilisateur, sinon texte fourni autorisé; pas d'extraction automatisée du navigateur connecté.

## Fournisseurs bibliographiques et techniques

- [OpenAlex — API reference](https://help.openalex.org/api/) et [authentication/quotas](https://help.openalex.org/api/authentication/) : endpoints REST, clé et limites dépendant du volume/fonctions; revoir les quotas au moment du codage.
- [Crossref REST — access and authentication](https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication) : recommandations de cache, identifiant du client, limites et backoff.
- [Zotero Web API v3](https://www.zotero.org/support/dev/web_api/v3/basics) : clé/version de l'API, lecture publique/privée et API locale, selon environnement.
- [GitHub REST best practices](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api) : requêtes conditionnelles `ETag` / `If-None-Match` pour diminuer charge et quotas.
- [WordPress REST — posts](https://developer.wordpress.org/rest-api/reference/posts/) : API de lecture par site, métadonnées, date et pagination.
- [Google Drive — téléchargements et exports](https://developers.google.com/workspace/drive/api/guides/manage-downloads) : distinguer blobs/export Workspace et vérifier capacités de téléchargement et scopes.

## Procédure obligatoire de revalidation

Pour chaque fiche à activer : consulter la documentation officielle, dater, conserver URL exact, versions/schemes, terms/licences, autorisations, scopes/quotas, granularité, données modifiées/supprimées, test de refus et options de repli. Les détails de tarifs, quotas, versions et endpoints peuvent changer **après** la date de ce dossier. Un résultat web ne vaut jamais consentement d'un propriétaire de contenu.
