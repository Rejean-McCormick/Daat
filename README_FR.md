# DaaT — Documentation fondatrice

**Statut : spécification technique de construction, pas encore service déployé.**

DaaT est la frontière d'interopérabilité des systèmes externes. Chaque application peut se connecter à l'écosystème sans abandonner son architecture : un système déjà aligné utilise un DaaT minimal, un système avec des contrats différents utilise un adaptateur explicite plus élaboré. Le **coût sémantique de l'adaptation** est un indicateur de distance d'alignement, jamais une mesure de qualité ou une raison d'exclure une application.

La documentation technique canonique est en anglais pour faciliter la construction par une IA et la contribution d'autres développeurs; [la vision fondatrice en français](docs/fr/VISION.md) précise l'intention.

## Lecture recommandée

1. [Instructions pour l'IA de construction](AGENTS.md) : contraintes, interdits et validation.
2. [État actuel vérifié dans les snapshots](docs/01-SOURCE-BASELINE.md) : ce qui existe réellement dans IK et Kristal.
3. [Architecture](docs/03-ARCHITECTURE.md) : qui est propriétaire de quoi.
4. [Profils de mapping](docs/06-MAPPING-PROFILES.md) : transformations déterministes et traçables.
5. [Mesure de l'alignement](docs/07-ALIGNMENT-METRICS.md) : couverture, transformations, pertes et conformité.
6. [Sécurité](docs/05-ADMISSION-AND-SECURITY.md) : autorisation et frontières de confiance.
7. [Plan d'implémentation](docs/11-IMPLEMENTATION-PLAN.md) et [backlog pour l'IA](docs/15-AI-BUILD-BACKLOG.md).
8. [Décisions en suspens](docs/14-OPEN-DECISIONS.md) : les sujets à ne pas inventer.

## Point important

Les documents distinguent les contrats **déjà établis** — notamment l'adaptateur DaaT/Kristal d'Interaction Kernel — de l'extension **proposée** vers un DaaT général pour les systèmes externes. Ils n'affirment pas qu'un service DaaT complet existe ou que l'ensemble de l'écosystème est déjà aligné.

## Nouveauté 0.4.0 — Préparation locale de sources

Un catalogue des 36 familles et des lecteurs locaux, en lecture seule, ont été ajoutés pour PDF (pypdf facultatif), archives ZIP, Git par commit immuable, CSV/JSON/JSONL/TSV, métadonnées bibliographiques et exports Acomba. L'extraction produit **des preuves et candidats non canoniques**, sans créer de Kristal ni publier aucune donnée. Les vrais accès aux API/ERP et les contrats IK/Médiathèque/Kit demeurent des autorisations distinctes non livrées. Voir `docs/35-OFFLINE-ONRAMP-IMPLEMENTATION-0.4.md`.

## v0.4.1 — Chaîne Kristal : vérification et proposition locales

`kristal-owner-preflight` inspecte uniquement les sources et empreintes des dépôts Framework, Kit, Kristalizer, diK et Arketype. `kristal-prepare-handoff` produit un paquet de propositions non canoniques depuis un aperçu et une revue validés. **Aucune construction canonique, écriture Kit, autorisation IK ni publication n'est effectuée.** diK draft.3 et le Kit/Framework draft.4 restent à qualifier ensemble. Voir `docs/36-KRISTAL-OWNER-CHAIN-LOCAL-HANDOFF.md`.

## v0.4.2 — Alignement des chemins réels

Les dépôts sont maintenant repérés via `docs/inventory/repositories.json` du dépôt central kOA, sous `C:\mycode`. Le chemin réel de DaAT est `C:\mycode\Interaction-Kernel\Daat`. La nouvelle vérification compare également les **11 schémas v11** de diK et Framework, sans conclure à une compatibilité fonctionnelle ni autoriser la création de Kristals. Voir `docs/37-C0-INVENTORY-AND-DIK-SCHEMA-PARITY.md`.

## v0.4.3 — Audit local de la chaîne

`daat kristal-local-chain-audit --preview P.json --review R.json --handoff H.json` valide les trois artefacts liés, sans création ni publication de Kristal. Ajouter `--root C:\\mycode` pour contrôler les empreintes des dépôts propriétaires, sans les exécuter. Ce n'est pas une admission par le Kit.
