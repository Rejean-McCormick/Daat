# DaaT — Pont universel de l'information : dossier de construction intégral

**CODE 0.5.0 DISPONIBLE** : le [rapport d’implémentation](IMPLEMENTATION-0.5.0.md) documente les modules exécutables, leur périmètre de tests et les dépendances encore bloquées. Le texte ci-dessous reste la spécification cible initiale de novembre 2026; l’intégration de code 0.5.0 ne qualifie pas encore la cible complète.

**Version documentaire** : `DaaT-information-bridge-target/1.0-draft.1` (identifiant de travail, **pas** un protocole officiel).  
**Établi le** : 14 novembre 2026. **Statut** : `[PROPOSAL] TARGET_DESIGN`, **documentation intégrale, implémentation de la cible NON livrée**.  
**Dépôt visé** : `C:\mycode\Interaction-Kernel\Daat`. **Nom humain** : DaaT; **ID système** : `daat`.

## Mandat exact

DaaT constitue le **pont d'entrée et de préparation de connaissances** : permettre de découvrir des sources, sélectionner des voies autorisées, recevoir des artefacts ou références via des propriétaires compétents, normaliser l'information, conserver la provenance et composer des **dossiers de contexte utilisables par ChatGPT**, avec une boucle humaine ou une API autorisée. **AUCUNE production, validation, publication ou activation d'un Kristal n'est dans le périmètre de cette livraison.** Les anciens outils `kristal-*` et le prototype `chatgpt_loop.py` restent factuellement présents dans le code 0.4.4 : ils ne sont pas le contrat de sortie de la nouvelle cible et ne doivent pas être présentés comme équivalents.

## Statut factuel et légende

- `[UPSTREAM-FACT]` : constat observable dans les snapshots et contrats propriétaires existants.
- `[TESTED]` : comportement effectivement testé, uniquement dans son périmètre indiqué.
- `[PROPOSAL]` : design de cette documentation, à implémenter et faire approuver selon son propriétaire.
- `[OWNER-DECISION]` : point que DaaT ne peut pas décider seul.
- `[BLOCKED]` : chemin non autorisé, non démontré ou dépendance absente.

**Faits 2026-11-14** : le dépôt 0.4.4 dispose de lecteurs locaux, de l'outillage de mapping, d'un registre de **36 familles**, de **89 profils de plateformes**, d'une boucle manuelle ChatGPT hors ligne et d'outils de preuve de chaîne non canonique. Les **89** sont des descriptions, **pas des connecteurs qualifiés**; 14 profils ont une documentation officielle consultée pour au moins une voie, 75 restent à vérifier. Aucun bus externe, IAM, scraping Medium, service d'acquisition universelle ou livraison ChatGPT production n'est certifié dans ce socle.

## Parcours de lecture du dossier

1. [01 — Mandat et exigences](01-PERIMETRE-ET-EXIGENCES.md).
2. [02 — Architecture et responsabilités](02-ARCHITECTURE-ET-RESPONSABILITES.md).
3. [03 — Méthodes d'accès et moteur de décision](03-ACCES-ET-SELECTION.md).
4. [04 — Registre détaillé des 89 profils](04-REGISTRE-89-PLATEFORMES.md) et [05 — matrice des 36 familles](05-COUVERTURE-36-FAMILLES.md).
5. [06 — Flux, lots, synchronisation et lifecycle](06-FLUX-LOTS-SYNCHRONISATION.md).
6. [07 — Données, provenance, droits, dédoublonnage](07-MODELE-DONNEES-ET-PROVENANCE.md).
7. [08 — Dossier contextuel ChatGPT et export](08-DOSSIER-CONTEXTUEL-CHATGPT.md).
8. [09 — Boucle IA et prompts](09-BOUCLE-IA-ET-PROMPTS.md).
9. [10 — Sécurité, vie privée et licences](10-SECURITE-DROITS-ET-CONFIANCE.md).
10. [11 — Connecteurs, plugins et stratégie Kintsugi](11-CONNECTEURS-EXTENSIBILITE-OSS.md).
11. [12 — UX et besoins utilisateurs](12-INTERFACE-ET-PARCOURS-UTILISATEURS.md).
12. [13 — Observabilité et DaaT_Diag](13-DIAGNOSTIC-FEEDBACK-OBSERVABILITE.md).
13. [14 — Qualification et tests](14-TESTS-ET-DEFINITION-DE-TERMINE.md).
14. [15 — Plan d'exécution en une seule livraison](15-PLAN-DE-REALISATION-INTEGRALE.md).
15. [16 — Matrice de responsabilités, risques, décisions](16-TRACABILITE-RISQUES-DECISIONS.md).
16. [17 — Scénarios complets et incidents](17-SCENARIOS-BOUT-EN-BOUT.md).
17. [18 — Recherche externe vérifiée et révision documentaire](18-SOURCES-EXTERNES-VERIFIEES.md).
18. [19 — Migration de l'existant et plan de fichiers](19-MIGRATION-ET-STRUCTURE-CODE.md).
19. [20 — Tâches pour agents et maîtrise de scope](20-CONSIGNES-IMPLEMENTATION.md).
20. [ADR proposé](../decisions/ADR-0005-DAAT-INFORMATION-BRIDGE-CHATGPT-CONTEXT.md).

- [Validation documentaire et résultats réellement exécutés](VALIDATION-DOCUMENTATION-2026-11-14.md).

## Artefacts techniques de conception

- [Inventaire de couverture des 89 profils](data/plateformes-89-couverture.csv), **non qualifié en production**.
- [Matrice de travail de la livraison unique](data/travaux-livraison-unique.csv) et [matrice de tests](data/cas-tests-acceptation.csv).
- [Schéma illustratif du dossier contextuel](schemas/context-bundle.example.schema.json) et [exemple de dossier](examples/context-bundle.example.json). Ces fichiers ne sont **ni des contrats IK ni des contrats kOA adoptés**.
- [Exemple de prompt ChatGPT](examples/prompt-chatgpt.example.md) et [exemple de décision d'accès](examples/decision-acces.example.json), entièrement synthétiques.

## Ordre normatif et conditions d'arrêt

Les contrats propriétaires approuvés (`IK`, `Konfid`, source, `Médiathèque`, etc.) priment les ADR approuvés de DaaT, qui priment les designs dans ce dossier. En cas de conflit, **bloquer la voie affectée** et poursuivre uniquement ce qui reste sûr. Une documentation complète n'est ni un permis de collecte, ni une promesse de traitement de tous les paywalls, ni une preuve d'intégration bilatérale.

## Livrable « en entier d'un coup »

Un seul périmètre produit et un **seul verdict final** sur l'ensemble des fonctions essentielles; les équipes peuvent travailler en parallèle à l'intérieur de la livraison. Les modules ne sont pas considérés « terminés » isolément si le corpus final, les droits, le parcours ChatGPT et les tests de bout en bout ne passent pas. Les voies interdites/indisponibles doivent toujours produire un état explicite `BLOCKED` + alternative permise : c'est une couverture complète **des décisions**, pas une promesse d'accès universel.
