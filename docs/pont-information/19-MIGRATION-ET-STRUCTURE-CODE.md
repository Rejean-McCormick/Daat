# 19 — Migration de DaaT 0.4.4 vers la cible de pont d'information

**Statut** : `[PROPOSAL]` — ce pack **n'altère pas le code** de DaaT 0.4.4; il décrit les adaptations à effectuer lors de l'implémentation intégrale.

## 1. Base observée dans le dépôt fourni

| Composants déjà présents | Réemploi cible | Manque identifié |
|---|---|---|
| `src/daat/catalog.py`, `registry.py`, `source.py` | Registre/profils et familles | Autorisation et statut opérationnel par voie/compte |
| `src/daat/pipeline.py`, `adapter.py`, `mapping.py` | Préparation déterministe locale | Normalisation multi-source et types/versions stables |
| `src/daat/hosted.py`, `ports.py` | Ports du host et de l'admission | Interfaces connecteurs propriétaires en production |
| `src/daat/journal.py` | Journalisation opérationnelle locale | Checkpoints/reprise durables, sans nouveau scheduler |
| `src/daat/review.py`, `candidates.py`, `verification.py` | Revue, validations et refus | Corpus multi-sources et décisions sur annotations ChatGPT |
| `src/daat/chatgpt_loop.py`, `tools/DaAT_ChatGPT_Loop.pyw` | Boucle prompt-réponse hors ligne | **Cible Context Bundle**, non brouillon de Kristal |
| `docs/data/platform-access-registry.v1.json` | 89 profils, 36 familles | Recherche par voie, révisions, status et contrats qualifiés |
| `tools/daat_source_access.py`, `LANCER_REGISTRE_SOURCES.pyw` | Navigation catalogue hors ligne | Parcours intégré Studio avec droit/progression |
| `src/daat/kristal_chain.py`, `chain_audit.py` | Fonctionnalités **historiques, hors nouveau mandat** | Ne plus confondre avec livrable ChatGPT |
| `tools/verify_manifest.py`, DaaT_Diag externe | Intégrité et rapports | Tests réel de sources, droits et Context Bundles |

## 2. Migration sans rupture

1. Geler un snapshot/sha des sources 0.4.4 + régression existante.
2. Garder les anciennes commandes/format de candidats disponibles avec label `legacy_noncanonical` si les tests et utilisateurs en dépendent; pas d'appel automatique vers Kit.
3. Ajouter des modèles locaux versionnés de `Context Bundle`, `AccessDecision`, `SourceReference` et `EvidenceFragment` dans **une namespace DaaT interne** après ADR, sans imiter les IDs d'IK.
4. Conserver les `source_family`/`platform_id` et chemins 36/89 existants; migration additive avec validation des vieux registres et états `unknown` explicites.
5. Faire pointer l'interface principale vers le plan de collecte et le dossier contextuel; conserver le registre simple et la boucle manuelle comme sous-vues.
6. Ajouter les vrais ports hôtes sans faire d'import dynamique de scripts non approuvés; tester les propriétaires avec leurs exacts contrats.
7. Maintenir `REPOSITORY-MANIFEST.json` en cohérence avec les fichiers du snapshot final; ce fichier est un **contrôle d'intégrité non signé**, et une installation avec fichiers locaux modifiés doit recalculer sa propre baseline.
8. Installer un mode de compatibilité si l'ancien `kristal-review-handoff` est attendu par un consommateur historique; ne jamais le générer comme effet secondaire du nouveau Dossier contextuel.
9. Documenter la migration des projets/exports existants (versions, perte de champ, compatibilité, propriété), préserver les droits et le retrait.
10. Après intégration unique, exécuter **ensemble** les suites existantes, la nouvelle matrice de tests, bilatéraux owners, sécurité et GUI Windows.

## 3. Placement physique de la documentation

Ce dossier se situe dans `docs/pont-information/` et complète les documents `docs/26-*` à `docs/38-*`. La demande actuelle **représente un recentrage du projet**, pas un remplacement silencieux des ADR et fichiers existants. Une modification normative exige revue/approbation des propriétaires.

## 4. Compatibilité opérationnelle

Chemin réel recensé : `C:\mycode\Interaction-Kernel\Daat`. Les dépôts Konfid, IK, Skope, Médiathèque, Framework, Kit et diK peuvent fournir des frontières nécessaires, mais **n'ont pas besoin d'être modifiés dans ce pack documentaire**. L'ancienne solution `DaaT_Diag` est un dépôt distinct; ses nouveaux B01–B12 sont une spécification non livrée.
