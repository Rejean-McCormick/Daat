# 15 — Plan de réalisation intégrale : un seul chantier, une seule version cible

**Statut** : `[PROPOSAL]` — cahier d'implémentation complet, pas exécution déjà faite. **Consigne** : pas de série de « petits livrables définitifs » qui donnent une fausse impression de complétude. Le travail interne peut être parallélisé, avec intégration continue; l’acceptation et la communication de fin sont **uniques** et portent sur l'ensemble du pont.

## 1. Contrat de livraison

**Objectif** : DaaT reçoit et organise des sources autorisées de toutes les familles via des lanes/owners qualifiés; crée des références, fragments et liens fidèles; produit des Context Bundles compatibles avec le travail ChatGPT; supporte le retour de réponse IA contrôlé; expose des diagnostics détaillés et fonctionne sur Windows, CLI et hosts approuvés. **Pas de Kristal, Kit, publication ni activation dans cette livraison.**

## 2. Équipes / responsabilités parallèles

| Lot | Contenu complet | Responsable proposé | Dépend de | Livrable et preuve finale |
|---|---|---|---|---|
| W01 | Gouvernance, frontières et ADRs | DaaT + propriétaires IK/Skope/Médiathèque | Contrats existants | Décisions, interfaces adoptées ou refus explicites |
| W02 | Répertoire 89/36 et recherche documentaire | DaaT catalogue | Sources officielles | Profils, état par voie, dates et liens vérifiables |
| W03 | Moteur de choix et plan de permissions | DaaT core/host | W01,W02 | Choix L1–L8 et reason codes, refus testé |
| W04 | Import fichiers locaux et exports | DaaT + hôte d'import | W03 | Lots fichiers/ZIP/CSV/PDF/JSON et tests de sécurité |
| W05 | API et OAI-PMH | Propriétaires connecteurs | W01,W03 | SDK, quotas, pagination, preuves providers activés |
| W06 | RSS/Atom, CMS et sites autorisés | Propriétaires connecteurs | W01,W03 | Medium RSS, WordPress/flux, niveaux de contenu |
| W07 | Bibliographie et bibliothèques | Propriétaires connecteurs | W04,W05 | PhilPapers, Zotero, OpenAlex/Crossref sous droits |
| W08 | Git, référentiels, SaaS cloud | Propriétaires connecteurs | W03,W05 | Pins, ETag, export et ACL |
| W09 | ERP/bases/jeux de données/événements | Propriétaires sources/host | W03,W10 | Exports permis, schémas, CDC si approuvé |
| W10 | Coffre, Konfid/host, confidentialité | Sécurité et owners | W01 | PEP et droits réels, isolement, audit, rétention |
| W11 | Parsers, tableaux, multimodal, Kintsugi | DaaT/outil hôte | W04,W10 | Extraction bornée, positions, provenance, licences |
| W12 | Modèle documentaire et normalisation | DaaT core | W01,W11 | Références/segments/transforms et schémas internes |
| W13 | Dédoublonnage, versions, rapprochement | DaaT core | W12 | Liens non canoniques, diff, contradictions |
| W14 | Synchronisation, retries, réconciliation | Source owners/host | W05–W09,W10 | Reprise/idempotence/révocation testées |
| W15 | Context Bundle et export multi-format | DaaT core | W10,W12,W13 | Schéma local, redaction, manifestes et packs |
| W16 | Prompts/ChatGPT manuel/API optionnelle | DaaT IA/host | W10,W15 | Gabarits, allers-retours, validations et corrections |
| W17 | Interface unifiée Windows/CLI | DaaT produit | W02,W03,W15,W16 | Progression, annulation, alertes, sans CMD |
| W18 | DaaT_Diag / feedback / observabilité | DaaT_Diag | W03–W17 | Rapports reliés aux tests bilatéraux et droits |
| W19 | Tests de sécurité, de charge, end-to-end | QA + owners | Tous | 36/89, AT-01..AT-12, négatifs, bilatéraux |
| W20 | Packaging, guide, compatibilité et release | Maintenance DaaT | W01–W19 | Un seul candidat final, SBOM, manuel, plan de reprise |

Les 20 lots **ne sont pas 20 phases séquentielles** : ils forment un plan de travail **parallélisé** avec des dépendances techniques. La mise en production attend **tous les critères d'acceptation pertinents**. Le [CSV de travail détaillé](data/travaux-livraison-unique.csv) décompose chaque lot en tâches vérifiables avec propriétaire, entrée, sortie et tests.

## 3. Ordre de construction interne sans jalons livrés incomplets

**Bloc A, fondations communes** : gel de versions et droits, validation des contrats, registre et sécurité, schémas contextuels et ports, harness de tests. **Bloc B, parallélisation des capacités** : L1–L8, parsers, provenance, imports, UX, IA manuelle/API, synchronisation et DaaT_Diag évoluent ensemble sous CI. **Bloc C, intégration globale** : tests bilatéraux, migration, sécurité, charge, cas utilisateurs, droits, version unique et sign-off. Ces blocs servent à coordonner l'équipe; ils **ne sont pas** des produits « partiellement finis » annoncés au public.

## 4. Répertoire cible de code (proposition, pas autorisation de renommer l'existant)

```text
src/daat/
  registry.py                  # existant : extensible
  catalog.py / source.py       # existants : réutiliser
  planner.py                   # nouveau : sélection de voie
  source_ports.py              # nouveau : interfaces host vérifiées
  ingestion/                   # nouveaux workers bornés hors DSL
  representations.py           # nouveau : références et formats
  provenance.py / rights.py    # nouvelles règles déterministes
  normalization.py / linkage.py
  context_bundle.py / prompt_library.py / ai_feedback.py
  diagnostic_events.py
contracts/daat/context/       # schémas locaux proposés après ADR DaaT
profiles/access/              # fiches versionnées et sources officielles
examples/context/            # zéro donnée privée, fixtures illustratives
ui/                            # GUI et adaptation launcher .pyw
```

Les ports hôtes / connecteurs spécialisés peuvent résider dans leurs **propres dépôts** plutôt que dans DaaT. Le code n'a pas le droit de modifier Framework, Kit ou une API IK sans adoption explicite.

## 5. Definition of Ready pour toute implémentation

- Baseline repo 0.4.4 + registre 89/36 vérifiés et figés.
- Owner de la source, conditions, versions, droits, capacité de test et hébergement précisés.
- Schéma/contrat propriétaire réel identifié (pas inventé).
- Fixture positive et négative; si API privée inaccessible, voie `BLOCKED` documentée et alternative testée.
- Modèle de confidentialité, rétention, export IA documentés.
- Éléments de sécurité et de licence OSS au niveau dépendance.

## 6. Barrières d'intégration et d'acceptation finales

**G1** tous les invariants AGENTS/owners respectés; **G2** 36 familles/89 fiches complètes avec leur maturité réelle; **G3** lanes activées testées avec leur host, refus de voies non approuvées; **G4** parcours complet de traitement de lots/synchronisation/reprise; **G5** Context Bundle/ChatGPT avec droits et citations; **G6** performance, sécurité, tests négatifs et UX; **G7** diagnostic vérifiable et reproduction; **G8** documentation/distribution/compatibilité vérifiées. **Sortie** : acceptation uniquement si toutes les barrières applicables sont satisfaites; sinon tableau de lacunes, sans « version finale » trompeuse.

## 7. Risques de calendrier et arbitrages

La durée et le coût **ne peuvent être garantis** avant disponibilité des owners, droits et environnements de tests. Les intégrations non autorisées ou sans API n'imposent pas un contournement : elles sont couvertes par un état sûr et un repli manuel/référence. Définir les budgets et limites auprès des propriétaires au moment de construire; ne pas réduire la sécurité pour respecter une date arbitraire.
