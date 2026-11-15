# 16 — Matrice de gouvernance, décisions ouvertes, risques et traçabilité

**Statut** : `[PROPOSAL]`. Les constats de droits, d’identité et de transport impliquent des **propriétaires**, jamais une approbation implicite par DaaT.

## 1. Décisions propriétaires nécessaires

| ID | Décision | Owner responsable | Impact si non approuvé | Attitude sûre |
|---|---|---|---|---|
| O-01 | Moyen d'authentifier host, acteur et tenant pour les sources | Konfid/IdP/host | Accès connecté | Désactiver connecteurs privés |
| O-02 | Qui possède l'accès source, les jetons et refresh grants | Fournisseur/source owner | API privées | Utiliser export utilisateur permis |
| O-03 | Droit de copier/retention/analyses/IA par fournisseur | Source propriétaire/Legal | Texte intégral et ChatGPT | Mettre référence/metadata seulement |
| O-04 | Contrat de custody si des octets doivent être conservés | Médiathèque et instance cible | Snapshots durables | Garder ref sous système propriétaire |
| O-05 | Transport IK et version de profil si multi-repo | Interaction Kernel | Messages inter-dépôts | Local/in-process seulement, pas profil inventé |
| O-06 | Hébergement et isolation des connectors annexés | Security/source owner | API/ERP/CDC | Sandbox ou voie inactive |
| O-07 | Définition d'audit et de rétention | Sécurité/Legal | PII/trace durable | Minimiser et refuser certaines exports |
| O-08 | Choix d'un fournisseur IA, conditions et locality | Opérateur/Legal/Security | Envoi de contenus | ChatGPT manuel seulement quand autorisé |
| O-09 | Limites budgétaires par projet, source, tenant | Exploitation | Coût/DoS | Quota faible local ou arrêt explicite |
| O-10 | Licence et sécurité de chaque Annex OSS | Mainteneur et Legal | Inclusion d'outillage tiers | Mimic ou reference-only |
| O-11 | Approbation d'une source de santé/éducation/finances | Domaine et sécurité | Risque réglementaire | Profil non actif, metadata expurgée |
| O-12 | Statut des exports Acomba selon édition | Source/partenaire Acomba | Export et schémas | Fichier explicitement exporté |
| O-13 | Règle de purge/retention des dérivés après révocation | Source owner/custodian | Stockage et historique | Blocage nouvelle divulgation |
| O-14 | Règle d'accès partagé et revue collaborative | Host/tenant owner | Multiutilisateur | Projet local individuel seulement |
| O-15 | Schéma officiel éventuel de Context Bundle au-delà du local | DaaT et consommateurs autorisés | Interop externe | Format local expérimental versionné |
| O-16 | Garanties de traitement réel des APIs spécialisées | Source owners | Qualification production | `BLOCKED` + test de contrat simulé |

**Le choix d'éliminer le build Kristal est validé par le mandat produit du présent dossier, mais ne remplace aucun ADR IK antérieur.** Les opérations Kristal historiques restent hors scope de cette cible, pas supprimées du dépôt sans revue de compatibilité.

## 2. Registre de risques

| Risque | Probabilité / impact à estimer | Détection | Mesure préventive | Responsabilité |
|---|---|---|---|---|
| Restriction API ou modification ToS | Dépend de la source | Diff docs et erreurs API | Modes alternatifs légaux, registre versionné | Provider maintainer |
| Licence implicite de texte intégral | Élevé impact juridique | Rights matrix manquante | Fail-closed, référence seule | Legal/source owner |
| Accès privé exposé à ChatGPT | Impact majeur | Tests canary / redaction | Disclosure gate, chiffrement hôte | Security/host |
| Mauvais ancrage citation | Qualité majeure | Check exact et version | Locators et refus | DaaT core |
| Mélange de tenants | Impact critique | Tests multi-tenant | Identité vérifiée, isolation | Host/Konfid |
| Temps API/cout imprévisible | Variable | Quotas/alertes | Budgets et backoff | Operations |
| 89 profils affichés comme 89 connecteurs | Risque produit majeur | UI/Diag et audit registre | États de maturité distincts | Product/Diag |
| Perte de granularité ou de sens | Qualité majeure | Contrôle des transformations | Profils explicites et tests | DaaT |
| Dépendance OSS mal licenciée | Sécurité/licence | SBOM, scan et revue | Annex isolé ou rejet | Mainteneur |
| Faux vert basé sur fixtures | Risque de conformité | Vérification des preuves R0–R4 | Bilateral tests + evidence | QA/owners |

## 3. Matrice de traçabilité

Toutes les EF/ENF de `01-PERIMETRE-ET-EXIGENCES.md` doivent être liées dans la CI à : module réel + exigences de données + test automatique + test négatif + evidence de host/owner si besoin + version + résultat. Un schéma rédigé n'est pas une preuve de réalisation. Utiliser `data/travaux-livraison-unique.csv` et `data/cas-tests-acceptation.csv` comme matrices de pilotage initiales et mettre à jour leurs états seulement selon les résultats réellement exécutés.

## 4. Politique de modification de contrat

Toute communication nouvelle entre DaaT et IK, Médiathèque, Skope ou Konfid exige : proposant, owner, version, schéma/semantics, auth, privacy, migration, tests bilatéraux, refus et code de compatibilité. Si non approuvé, ne pas implémenter une interop réseau « temporaire » se faisant passer pour officielle.
