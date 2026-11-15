# 06 — Traitement, flux par lots, synchronisation, incidents et reprise

**Statut** : `[PROPOSAL]`; design d'états logiques. Ne pas créer un bus ou un ordonnanceur de missions parallèle à IK/Orgo.

## 1. Machine à états d'une demande

```text
DRAFT -> PROFILING -> RIGHTS_REQUIRED -> PLANNED -> OWNER_ACQUIRING
                         |              |                |
                         v              v                v
                       BLOCKED       BLOCKED       OWNER_REPORT_ERROR
                                     |                |
                                     +----> RETRYABLE / RECONCILIATION
OWNER_ACQUIRING -> REFERENCED -> EXTRACTING -> NORMALIZED -> LINKED
                         |              |              |
                         +----> QUARANTINED / PARTIAL / BLOCKED
LINKED -> DISCLOSURE_REVIEW -> CONTEXT_READY -> EXPORTED
                          |          |              |
                        BLOCKED   REDACTED       REVOKED
EXPORTED -> [optional] AI_RESPONSE_RECEIVED -> AI_VALIDATED -> HUMAN_REVIEWED
                                               |                 |
                                            REJECTED          FEEDBACK
```

Tous les états sont **de suivi DaaT**, pas des statuts IK officiels. **`EXPORTED` ne signifie pas `DISCLOSED`** si l'utilisateur n'a pas encore collé la sortie dans ChatGPT. En cas de timeout après effet possible chez un propriétaire, tenir `EFFECT_UNKNOWN` et demander réconciliation; pas de retry aveugle.

## 2. Granularité des enregistrements

Identités distinctes : `source_profile_id`, `external_source_id`, `external_revision`, `retrieval_event_id`, `representation_id`, `segment_id`, `context_bundle_id`, `disclosure_event_id`. Ne pas déduire une identité KQ/KP/KA/KS. Conserver `subject_scope`, `dataset_partition`, `content_kind` parmi `reference_only`, `abstract`, `excerpt`, `full_text_authorized`, `dataset`, `structured_record`, `media_derivative`.

## 3. Lots et pagination

- Planifier un **budget d’opération** : maximum d’items, octets, pages API, coût, fenêtres de temps, quotas source, jetons IA, instances et rétentions; bloquer les budgets non fixés.
- Sous-processus de collecte sous contrôle du host; éviter l'exécution de code de mapping libre. Diviser en shards avec `source_id + revision + partition`, checkpoint persistant du propriétaire, clé d'idempotence de demande + hachage d'intention.
- Pagination par pages, curseurs ou resumption tokens uniquement si officiellement documentés. L’ordre du fournisseur n’est pas une garantie de stabilité; vérifier les omissions, suppressions et doublons par rapport au snapshot.
- Règle d’allègement : si la référence fédérée suffit, ne pas copier l’original. Si la récupération est autorisée, ne garder les octets que là où le custodian l'autorise; DaaT garde références et représentations temporaires nécessaires.
- En cas de 429, respecter `Retry-After`, backoff exponentiel avec jitter, quota journalier et limite des tentatives; un 401/403 n'est pas un signal de retry automatique.

## 4. Synchronisation incrémentale et divergences

- Sources API : `ETag`, `Last-Modified`, versions provider, curseurs natifs selon leur documentation; ne pas présumer leur présence.
- Git : pin du commit, pas seulement nom de branche, inventaire de fichiers modifiés/supprimés.
- Exports ZIP/CSV : nouveau snapshot; compare manifests et clés, aucun « incrémental » inventé.
- Bases SQL : timestamp/high-watermark seulement si le propriétaire garantit la sémantique; sinon snapshot cohérent ou CDC sous contrat.
- Référence fédérée : disponibilité vérifiée à chaque usage; la révocation/expiration peut invalider une réponse antérieure.
- Duplicats : identités stables distinctes des variations de titre/format; les suppressions et changements de droit sont des événements de cycle de vie, pas des ordres de supprimer les documents du propriétaire.

## 5. Extraction multimodale et format

Détection MIME non fondée sur l’extension, UTF-8 normalisé sans effacer l'original, séparateurs conservés, tables avec cellules/colonnes/unités, PDF par pages, HTML sous sanitization, code par chemin/commit/ligne, images/vidéos/audio par dérivés autorisés. OCR et transcription : version de moteur/modèle, langue, score technique/avertissements, coût, droit des données; si indisponibles, laisser `unprocessed_media` plutôt que d'inventer du texte.

## 6. Tolérance aux pannes / reprise

| Échec | Action obligatoire | Ne jamais faire |
|---|---|---|
| Fichier malicieux ou ZIP bomb | Quarantaine owner, limite profondeur/décompression, erreur explicite | Extraire sans borne, suivre chemins `..` |
| Session/source expirée | Suspension et demande de nouveau grant | Aspirer le contenu via navigateur ou cookies |
| Changement de version d'API | Marquer `drift`, recalculer mapping et tests | Basculer silencieusement |
| Conflit de révisions | Création d'une version séparée, comparaison, revue | Fusion silencieuse |
| IA indisponible | Permettre export manuel quand permis | Envoyer automatiquement à un tiers |
| Révocation de droits | Stopper nouveaux usages, expurgation, politique de purge hôte | Continuer sur ancienne autorisation |
| Timeout après effet | Réconciliation avec propriétaire | Réexécuter l'effet aveuglément |

## 7. Métriques cibles (seuils de publication définis en test)

Par source : volume réellement autorisé, items vus/obtenus/refusés, granularité, corrections, latence/quota, ratio de citations contrôlables, couverture d'index, dérive, doublons confirmés/candidats, coûts, permissions à renouveler, incidents par catégorie. Les seuils numériques devront être fixés sur les charges représentatives; ne pas inventer de SLO universel sans infrastructure connue.
