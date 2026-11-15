# 02 — Architecture cible : responsabilités, composants et frontières

**Statut** : `[PROPOSAL]`. L'architecture ci-dessous est un **assemblage de capacités**. Elle ne déclare aucun nouveau message IK, aucune API Médiathèque ou aucun transport Konfid comme déjà accepté.

## 1. Topologie logique

```text
Utilisateur / organisation / navigateur connecté / dépôt autorisé
                |
                v
[DaaT Studio: intention, choix, vue de corpus, revue]
                |
                v
[DaaT catalogue 36 familles/89 profils + plan de voie + droits]
                |
     +----------+-----------------+
     |                            |
[source-owner connectors]       [import local explicite]
[API / RSS / OAI / export]       [fichiers, ZIP, collage]
     |                            |
     +----------+-----------------+
                |
[contrôle du host : identité, permission, egress, quotas, audit]
                |
[représentations et références sous garde propriétaire / Médiathèque si adoptée]
                |
[DaaT : validate -> normalize -> link -> evidence -> context selection]
                |
        [Context Bundle versionné]
            /                 [ChatGPT manuel]     [IA API autorisée optionnelle]
            \                /
     [retours non fiables + citations vérifiées + revue humaine]
                |
  [dossier contextuel révisé + annotations + rapport]
                X  aucun Kristal/Kit, aucune publication
```

## 2. Répartition des responsabilités

| Fonction | Responsable de fait ou cible | DaaT fait | DaaT ne fait pas |
|---|---|---|---|
| Découverte et collecte externe | Source et connecteur/propriétaire, Skope/EncyK lorsque sa voie est adoptée | Choix, préparation du plan, consommation de références | Scraping ou appropriation des données |
| Conservation d'originaux | Médiathèque/instance ou custodian approuvé | Maintien de l'identifiant de référence et des limites | Nouvel entrepôt d'originaux |
| Identité, consentement, PEP | Source, Konfid, host, politique receiver | Demande de preuves et arrêt si refus | Créer un IdP, traiter un login navigateur comme consentement IA |
| Enveloppes inter-systèmes | Interaction Kernel | Implémenter des adapters **sur contrats adoptés** | Forger un `kristal.build.request/2.0.0` pour une collecte générique |
| Préparation, mapping, admission | DaaT | Normalisation déterministe, provenance, dossier contextuel | Définir la vérité, assigner KQ/KP/KA/KS |
| Enrichissement / IA | Hôte IA explicitement autorisé, utilisateur ChatGPT | Prompts, validation de sortie non fiable, revue | Donner à l'IA une autorité de lecture ou une permission |
| Création Kristal | Framework/Kit, hors chantier | **Aucune opération** dans la cible présente | Construction, publication, activation |
| Diagnostic | DaaT_Diag | Événements et preuves sans secrets | Affirmer conformité sur simple présence de modules |

## 3. Modules cibles dans le dépôt (noms proposés, non implémentés)

`registry` (existant; étendre validation des fiches), `planner` (nouveau : routage), `source_ports` (interfaces au host), `ingestion` (formats/streaming bornés), `content_profile` (granularité), `normalization` (types et unités explicites), `provenance` (références et positions), `linkage` (identité externe et rapprochements), `rights` (décision et export), `context_builder` (sélection et paquets), `prompt_service` (modèles versionnés), `response_validation` (contrôles), `feedback` (rapports d'écart), `operational_journal` (métadonnées minimales), `diagnostic_emitter` (mesures), `gui` (Windows, accessible), `cli` (toutes fonctions sûres). Les noms exacts seront validés contre les fichiers existants au moment du code.

## 4. Ports proposés — Python pseudo-interfaces, pas des APIs déployées

```python
class SourceProviderPort(Protocol):
    def capabilities(self, source_profile: str, actor_context) -> CapabilityReport: ...
    def plan(self, selection, declared_rights) -> SourcePlan: ...
    def acquire(self, approved_plan, cancellation) -> Iterator[BoundedEvidenceRef]: ...

class CustodyReferencePort(Protocol):
    def verify_access(self, evidence_ref, actor, purpose) -> VerifiedRef: ...
    def read_representation(self, verified_ref, byte_limit) -> BoundedRepresentation: ...

class AiDisclosurePort(Protocol):
    def authorize_disclosure(self, selections, target_ai, purpose) -> Decision: ...

class ContextExporter(Protocol):
    def build(self, reviewed_sources, policy, limits) -> LocalContextBundle: ...
```

Ces interfaces sont un **design interne**. Le host fournit les preuves d'acteur, l'environnement d'exécution, les credentials et les décisions. Aucun objet entrant ne peut s'auto-certifier comme `VerifiedRef`.

## 5. Séparation des plans

- **Control plane** : registre, politiques, versions, droits, capacités, plan, tâches et résultats (peu ou pas d'octets sources).
- **Data plane** : source sous sa responsabilité, connecteur sandboxé, représentation temporaire bornée, custodian/référence. Les copies de travail suivent une TTL et les obligations de suppression.
- **Knowledge preparation plane** : normalisation, segments, citations, index dérivé local sous consentement, regroupements et context bundle.
- **AI exchange plane** : prompt et retour explicitement traités comme données non fiables; aucun moyen de deviner des informations non lues.

## 6. Décisions d'architecture incontournables

Avant le déploiement : identité et séparation multi-tenant; emplacement du custodian pour chaque source; contrat source/consumer et profils IK si communication inter-repo; rétention, suppression, secrets, type de service; permission de diffusion ChatGPT; connecteurs externes qualifiés; coût des modèles et protection des données. Une démo locale ne règle pas ces décisions.

## 7. Compatibilité

Le code `src/daat/chatgpt_loop.py` produit aujourd'hui des candidats orientés « parties de Kristal ». Ne pas le supprimer abruptement. Ajouter une **nouvelle cible de contexte non canonique** indépendante, garder l'ancien format derrière une compatibilité explicitement marquée `legacy`, puis migrer l'interface pour ne plus suggérer que la construction Kristal fait partie du mandat.
