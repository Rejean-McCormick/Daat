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
