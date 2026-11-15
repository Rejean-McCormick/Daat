# 13 — DaaT_Diag, feedback loop et observabilité intégrée

**Statut** : `[PROPOSAL]`. Le diagnostic actuel possède N00–N06, D07–D19, mais vérifie surtout du code local et des contrats. Les tests ci-dessous **n'existent pas automatiquement** parce que leurs noms sont écrits ici.

## 1. Résultat diagnostic attendu

Pour **chaque source, voie, lot et dossier de contexte** : `status`, `subsystem`, `owner`, `evidence_refs`, `version`, `level`, `severity`, `repro`, `expected`, `observed`, `reason`, `fix_owner`, `action`, `privacy_redaction_status`. Les erreurs qui nécessitent un contrat propriétaire doivent être classées `OWNER_GATE`, pas comme un bug DaaT.

## 2. Niveaux recommandés pour le pont

| ID de travail | Diagnostic de la cible | Preuve à produire |
|---|---|---|
| B01 | Catalogue 36/89, maturité, documentation des méthodes | Registre versionné, diff et tests de schéma |
| B02 | Planificateur et repli sûr L1–L8 | Plans/raison-code pour fixtures autorisées/interdites |
| B03 | Connecteurs et sources | Probes bilatéraux, API versions/quotas, pas juste présence |
| B04 | Sécurité/permissions | refus, révocation, scope, tenant, secrets, disclosure |
| B05 | Parsers et multimodal | limites, extraction, positions et corruption |
| B06 | Synchronisation | pages, curseurs, ETag, restart, conflit, doublons |
| B07 | Provenance et dédoublonnage | Ancrages, revisions, identité externe, conflits |
| B08 | Construction du Context Bundle | schéma local, contenu autorisé, hash, redaction, exclusion |
| B09 | ChatGPT boucle | réponse valide/invalide, prompt injection, information insuffisante |
| B10 | Performance et exploitation | volume, annulation, quotas, temps et pertes |
| B11 | UX Windows | pas de console, progression, abandon, reprise, erreurs |
| B12 | Validation transversale | bout en bout multi-source, droits et dossier final |

Ces IDs sont des **noms de travail** pour une future extension DaaT_Diag; ne pas les confondre avec les niveaux N00/Dxx déjà présents.

## 3. Feedback loop pour les développeurs

Générer : `run-summary.json` (résumé, hash, état), `findings.json` (constats structurés), `coverage.csv` (89 profils, 36 familles, voie testée ou bloquée), `compatibility.json` (versions des contrats et outils), `replay-manifest.json` (fixtures expurgées et commandes), `feedback.md` (solutions par propriétaire) et ZIP d'assistance sans données confidentielles. Comparaison `added / fixed / worsened / unchanged / stale` avec le dernier run vérifié.

Exemple de constat :

```json
{"id":"B08-EXCLUDE-001","component":"context_export","verdict":"BLOCKED",
 "evidence":"permission_missing","owner":"source-rights/host",
 "action":"Obtenir preuve de divulgation ou exclure le passage",
 "source_content_included":false}
```

Le constat ci-dessus est une illustration, **pas un résultat observé d'une campagne réelle**.

## 4. Comptage et vérification

Un niveau peut produire plusieurs dizaines de constats. Les compteurs doivent distinguer « tests exécutés », « preuves manquantes », « dossiers bloqués par droits » et « défauts logiciel ». Ne pas résumer 50 refus légitimes en 50 « bugs ». Recalculer l'intégrité des fichiers et le verdict à partir des résultats réels; horodater, conserver versions de code et sources. Les fichiers SHA-256 ne sont pas authentifiés à eux seuls.

## 5. Observabilité sécurisée

Mesurer throughput, latence, succès, taux de refus, limites, erreurs, quotas et progression **sans enregistrer source bytes, prompts secrets, PII ou credentials**. Corréler par IDs aléatoires non secrets et références minimisées. Les logs ChatGPT manuels ne supposent jamais qu'une réponse a réellement été soumise au service par l'utilisateur tant que l'acte n'est pas confirmé.

## 6. Définition d'une boucle puissante

Après un run, le rapport doit répondre à : **quelle source**, **quelle voie**, **quelle permission**, **quel objet/révision**, **où les preuves ont été perdues**, **quel composant propriétaire**, **quelle action exacte**, **comment reproduire avec une fixture expurgée**, **quel impact sur le Context Bundle**, **quel test doit devenir vert**. Les diagnostics sans ces éléments restent incomplets.
