# 14 — Stratégie intégrale de tests, qualification et définition de terminé

**Statut** : `[PROPOSAL]` — matrice des tests à créer. Aucun résultat vert n'est annoncé pour cette nouvelle cible.

## 1. Hiérarchie des preuves

| Niveau | Preuve permise | Ne prouve pas |
|---|---|---|
| R0 | Documentation de la plateforme | Connecteur fonctionnel |
| R1 | Contrat local + fixtures synthétiques | Permission vraie ou accès API |
| R2 | Tests avec API/propriétaire en sandbox ou compte de test | Production sans incident |
| R3 | Test bilatéral et droits de récupération/divulgation contrôlés | Vérité de l'analyse IA |
| R4 | Corpus multi-source complet en environnement ressemblant à la production; contrôle sécurité, reprise, observabilité | Permission permanente pour chaque futur document |

La **cible intégrale** exige R4 sur les familles/voies effectivement activées, et un **état de refus vérifié** pour toute plateforme dont les droits ou l'accès ne sont pas disponibles. Un profil non vérifié n'est jamais étiqueté `operational`.

## 2. Grille de tests par capacité

- **Registre** : 89 IDs uniques, 36 familles, cohérence méthodes, champs, URLs, états et pistes non certifiées non promues.
- **L1** : PDF, CSV/TSV/JSON/JSONL, archives, fichiers répétés, casse Unicode, invalides, traversée de répertoire, compression malicieuse.
- **L2** : HTTP 200/204/206/304, 401/403/404/409/429/500, pagination, rotation de tokens, appels non désirés et fuite via redirect.
- **L3** : RSS/Atom partiel, OAI resumption, doublons feed, dates et licence, métadonnées seules.
- **L4** : partitions, immutabilité du manifeste, interruption, reprise, limite RAM et taille.
- **L5** : pin Git commit, arbres malicieux, sous-modules autorisés/non autorisés, fichiers supprimés.
- **L6** : export comptable, champs sensibles, locale/units, snapshot isolé, refus d'écriture.
- **L7** : événements réordonnés/dupliqués, webhook forgé, requêtes expirées, idempotence.
- **L8** : référence expirée, permissions révoquées, redirection non autorisée, source injoignable.
- **Provenance** : spans exacts, révisions, hash de dérivé, expression « non vérifiable » si original inaccessible.
- **Dédoublonnage** : DOI exact vs ambiguïté, mise à jour de titre, langues multiples, contradiction conservée.
- **ChatGPT** : JSON correct/falsifié, citations absentes, descriptions inventées à partir d'abstract, injection PDF/README, nouvelles demandes d'outils, refus d'accès, correction ciblée.
- **Consentement** : chaque permission lecture/copier/stocker/transformer/divulguer distincte, expire/revoke, tenant différent, secrets bloqués.
- **DaaT_Diag** : une erreur produit la bonne priorité et une preuve expurgée, comparaison d'états exactes, rapport vérifiable.
- **Windows/CLI** : GUI sans CMD, progression 0..n exacte, annulation, Unicode/fichiers longs, path inventory `C:\mycode` réellement pris en charge.
- **Performance** : stress fichiers/refs/millions d'items simulés; quotas de mémoire/délais décidés avec host, séparation multi-tenant et rétention.

## 3. Cas d'acceptation système (pas des mini-jalons indépendants)

**AT-01** Corpus public multivoie PhilPapers (notice), Medium (RSS), OpenAlex/Crossref (métadonnées), PDF autorisé et Git, résultat `ContextBundle` sans prétendre connaître les textes manquants. **AT-02** ZIP Medium fourni par auteur, centaines de posts simulés, dédoublonnage de RSS, import idempotent, citations et prompts. **AT-03** Bibliographie Zotero mixte publique/privée, refus des documents privés sans permission, export minimal. **AT-04** Export ERP autorisé avec PII, redaction avant IA et aucune lecture écriture de la base. **AT-05** Révocation source après préparation : arrêt et exclusion dans nouvelle version du bundle. **AT-06** Article paywall : metadata only, aucune tentative de contournement. **AT-07** Source qui injecte des instructions à ChatGPT : texte conservé comme données, pas d'exécution. **AT-08** API 429/timeout/révisions : reprise sans doublon et sans perte. **AT-09** Tous les 89 profils classés explicitement par capacité/droits/référence ou blocage, pas 89 annonces de connecteurs. **AT-10** Full diagnostic DaaT_Diag avec preuves au niveau source/segment, sans secrets. **AT-11** Long corpus découpé en prompts sous budget tout en conservant les citations et exclusions. **AT-12** Windows lanceur silencieux/annuler/reprendre/voir feedback.

## 4. Critères quantifiables et méthode de mesure

- **100%** des 36 familles ont une fiche, une route générique validée ou un état de refus documenté; 100% des 89 profils ont un état et une méthode de vérification. **Cela n'implique pas 100% de droits d'accès.**
- **0** promotion silencieuse metadata→full text, tentative de contournement de paywall, secret en rapport/prompt, identité KQ/P créée, bus ou état canonique créé par DaaT.
- **100%** des fragments divulgués ont une source/révision et un droit de diffusion validé ou sont refusés; **100%** des citations marquées exactes sont retrouvables dans la représentation autorisée.
- **0** tests critiques de refus/sécurité en échec à la livraison. Les tests à infrastructure externe indisponible restent `BLOCKED` et empêchent la certification de la voie concernée.
- Tests de performance avec **seuils définis et approuvés** à partir de profils de charge réels, pas chiffres fantaisistes; rapport exact du CPU/RAM/IO/coût.

## 5. Acceptation de la version intégrale

**Une seule revue de libération** avec : matrice EF/ENF, couverture 36/89, résultats R0–R4 par méthode et fournisseur, licences et décisions owner, tests API/rights, preuves de Context Bundle exact, compatibilité DaaT/IK/Konfid/Médiathèque, rapports de sécurité, migration, plan de support et DaaT_Diag. Si un item essentiel échoue, **ne pas annoncer « terminé »** : publier le rapport des blocages. Les fournisseurs impossibles à intégrer peuvent être `reference_only/blocked` comme résultat normal d'une architecture universelle.
