# 09 — Boucle ChatGPT et IA connectée optionnelle : comportement complet

**Statut** : `[PROPOSAL]` pour le moteur cible; `[TESTED]` limité au prototype `src/daat/chatgpt_loop.py` hors ligne 0.4.4. **Aucune liaison API ChatGPT existante n'est affirmée.**

## 1. Deux voies, même protocole fonctionnel

| Voie | Transmission | Autorité / journal | Cas d'usage |
|---|---|---|---|
| **A : ChatGPT manuel** | Prompt et contexte copié par l'utilisateur après confirmation | L'export n'est pas preuve que l'utilisateur a envoyé le texte; demander un retour structuré | Medium/PhilPapers, compte personnel, pas de connexion automatisée |
| **B : IA via host autorisé** | Client de fournisseur configuré et approuvé, jamais clé dans DaaT | Vérification source, finalité, policy, coûts, journal d'appel expurgé et révocation | Lots et analyses automatisées quand contractuellement permis |

Le prompt ne doit pas contenir de secrets, cookies, jetons ou champs confidentiels non autorisés. Le mode API **ne doit pas exister** sans décisions Konfid/host et conditions de données du prestataire.

## 2. Constructeur de prompts spécialisés (gabarits versionnés)

- `discover_questions` : transformer un corpus en axes de recherche sans prétendre répondre.
- `extract_attributed_statements` : extraire des énoncés attribués, avec ID et citation/source.
- `compare_sources` : accords et divergences sans arbitrage automatique.
- `extract_entities_and_relations` : noms/relations **externes et candidats non canoniques**.
- `identify_missing_evidence` : quels textes complets/annexes seraient nécessaires.
- `summarize_with_scope` : synthèse par niveau (notice/abstract/extrait/texte intégral).
- `audit_answer` : chercher citations absentes, conflits, unités, limites.
- `correct_response` : prompt de correction après échec déterministe.

Chaque gabarit a un ID local, une version, des paramètres, un schéma de sortie et des fixtures. On interdit aux gabarits de demander la construction d'un Kristal dans ce chantier.

## 3. Réponse de ChatGPT : format interne proposé

```json
{
  "answer_kind": "source_grounded_analysis",
  "bundle_id": "bundle-example-001",
  "claims": [
    {"text": "Assertion explicitement attribuée", "source_fragment_ids": ["frag-01"],
     "support": "direct_quote|paraphrase|interpretation|unverified", "uncertainty": "..."}
  ],
  "comparisons": [],
  "unanswered_questions": ["Le texte complet manque"],
  "not_a_kristal": true
}
```

C'est un **modèle illustratif de réponse**, non un schéma validé ou un contrat réseau. Le validateur réel doit vérifier JSON/schema/identifiants exacts, droits, ancrages textuels, éventuelles citations via dérivés légaux, et limites de contenu. Les assertions peuvent demeurer fausses malgré une bonne citation; elles sont soumises à revue.

## 4. Machine de contrôle de réponse

`RECEIVED -> PARSED -> SCHEMA_VALID -> ANCHORS_VALID -> DISCLOSURE_RECHECK -> HUMAN_REVIEW -> ACCEPTED_AS_DRAFT`.

Rejets exemplaires : réponse non JSON, champ inattendu, citation absente, passage d'une autre révision, ID inconnu, assertion fondée sur une simple notice mais présentée comme preuve d'article, injection d'identifiant canonique, tentatives d'obtenir plus de données, contenu non autorisé ou absence de consentement IA.

## 5. Correction et suivi

Si une réponse échoue, produire un **prompt de réparation** qui contient uniquement : les erreurs expurgées, les fragments encore autorisés et les règles; ne pas renvoyer tout le corpus par défaut. Conserver `attempt_id`, version de gabarit, résultat et choix humain sans publier les passages privés dans DaaT_Diag. En cas d'injection de prompt depuis une source, mettre la source comme **donnée** entourée d'une séparation explicite, jamais comme instruction système.

## 6. Comparaisons, qualités et limites

IA peut proposer regroupements, thèmes, paraphrases et contradictions; elle ne peut pas décider des droits, garantir la véracité, ni transformer une référence en article intégral. Le score d'un modèle est un signal technique, **pas une preuve**. L'objectif qualité : citations traçables, absence de fuite, différenciation du niveau de lecture, capacité à répondre « inconnu » et reproductibilité des étapes déterministes.

## 7. Boucle avec utilisateur et gestion des comptes

La connexion à Medium, Zotero ou PhilPapers s'effectue auprès du **fournisseur via le mécanisme officiel** ou dans un navigateur externe. DaaT n'ouvre pas de navigateur automatisé pour lire des articles derrière abonnement; l'utilisateur peut fournir un export/texte dont la réutilisation est licite. Un login ne vaut ni licence, ni droit de diffusion à ChatGPT.
