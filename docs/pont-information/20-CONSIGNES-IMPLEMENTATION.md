# 20 — Consignes pour les ingénieurs et agents IA chargés de la construction intégrale

**Statut** : document d'exécution `[PROPOSAL]`. Il ne remplace pas [AGENTS.md](../../AGENTS.md), les ADR approuvés et les contrats propriétaires.

## 1. Mandat strict

Construire **le pont universel de préparation de l'information**, de la découverte des sources au `Context Bundle` utilisable par ChatGPT, avec feedback et sécurité. **Ne pas implémenter la création de Kristal**; si une tâche semble le nécessiter, la signaler comme hors scope, sans la réaliser. DaaT doit préserver les sources et leurs droits, ne pas inventer d'accès, ne pas faire d'épistémologie canonique et ne pas usurper les rôles d'IK, Skope, Médiathèque, Konfid ou Orgo.

## 2. Protocole de travail contrôlable

- Avant code : lire `AGENTS.md`, `docs/03-*`, `docs/25-*`, `docs/27-*`, `docs/28-*`, `docs/37-PLATFORM-*`, `docs/38-*`, le présent dossier, et les versions owner réelles.
- Décomposer les tâches du CSV de W01–W20 **sans réduire le périmètre final**; travailler en branches parallèles intégrables, pas en pilotes présentés comme complétude.
- Pour chaque adaptation : liste des fichiers modifiés, propriétaire, données traitées, droits et risques, version d'interface, fixtures positives/négatives, commande réelle de test, contrat précis; documenter ce qui est simulé ou non testé.
- N'appeler un connecteur externe qu'avec sa capacité testée, une preuve d'identité fiable et le permission scope du host; si aucun vrai host n'existe, fournir interface + fixtures, marquer `BLOCKED`, sans publicité « prêt ».
- Les connecteurs doivent être remplaçables, sandboxés, à sortie validée, avec une provenance par fragment et une limite de taille.
- L'IA est une aide, et **sa sortie n'est pas fiable**; prompts versionnés, citations contrôlées, données sans droits exclues, correction itérative après refus.
- À la fin : exécuter suites existantes + nouvelles, tests bilatéraux, matrice 89/36, test « aucun contenu privé dans l'export », rapports, Windows GUI et revue sécurité.

## 3. Arrêts obligatoires

- Contrat source/IK/Konfid/Médiathèque absent ou contradictoire.
- Permission d'envoi à ChatGPT inconnue ou refusée.
- Protocole/API ou tarif/limite supposé sans preuve.
- Pertes sémantiques importantes, identifiants externes promus en identités canoniques.
- Ressource tierce nécessitant une licence non disponible.
- Test d'authentification, d'audit, de tenancies ou de fuite négatif en échec.
- Fournisseur demandant scraping du paywall, rotation de cookies ou usurpation de compte.

**Comportement exigé** : blocage motivé + alternative légale + action du propriétaire. Ne jamais coder un bypass pour obtenir une démonstration verte.

## 4. Aucune fausse preuve

N'affirmer la réussite que pour les tests **effectivement exécutés**. Les fichiers `*.example.json` sont pédagogiques, les scripts de test synthétiques ne prouvent ni des droits ni des APIs production. Un ZIP de documentation n'est pas l'implémentation finale. L'intégralité du plan est conçue **maintenant**, sa réalisation exige toujours du code, des environnements et des décisions owners avant acceptation.
