# 10 — Sécurité, droits, vie privée et périmètre de confiance

**Statut** : `[PROPOSAL]` + invariants repris de `AGENTS.md`, `docs/20-*`, `docs/23-*`, `docs/25-*`. **Aucun système d'identité ou coffre de secrets déployé par ce document.**

## 1. Matrice des droits : décisions séparées

| Droit | Exemple de preuve | Ne doit pas être inféré depuis |
|---|---|---|
| Découvrir une référence | Catalogue public, RSS permis | Texte intégral lisible |
| Lire une ressource | ACL/compte/scope source validé | URL publique ou login quelconque |
| Copier / extraire | Licence, permission fournisseur ou user source owner | Simple droit de visualisation |
| Conserver / indexer | Politique de rétention et droit d'usage | Téléchargement technique possible |
| Transformer / faire analyser | Licence, accord et finalité | Copie locale |
| Transmettre à ChatGPT / API externe | Permission de divulgation + politique IA + destinataire | Authentification à Medium, receipt Médiathèque, hash |
| Repartager / diffuser | Licence, approbation et périmètre séparé | Analyse interne acceptée |

La décision d'autorisation provient d'un **host/PEP qualifié** et de la source; le champ dans un formulaire utilisateur est un **témoignage**, pas une preuve autonome pour un contenu appartenant à un tiers.

## 2. Frontières de secrets

- OAuth/connecteurs : secrets au coffre hôte, jetons court terme/scopes minimaux, rotation, invalidation, HTTPS, état cryptographiquement validé.
- Ne jamais capturer cookies/session de navigateur; ne pas accepter les tokens collés comme texte d'article; masquer et alerter.
- Ne jamais écrire URL signées longues, bearer, Authorization, cookies ou PII non nécessaires dans les rapports, prompts, traces ou résultats de DaaT_Diag.
- Données sensibles : anonymisation/pseudonymisation sous règle approuvée, isolation tenant, contrôle d'export après redaction.

## 3. Menaces et mitigations obligatoires

| Menace | Protection et test négatif |
|---|---|
| SSRF / accès intranet / DNS rebinding | Egress allowlistée, validation DNS/IP répétée, redirect policy, pas de fetch sur URL fournie librement |
| ZIP bomb, path traversal, symlink | Taille compressée/décompressée, profondeur, chemins sûrs, files count, sandbox |
| PDF/HTML/XML malicieux | Parseurs à versions épinglées, isolation process, XXE désactivé, ressources bornées |
| Plugin/tap tiers compromis | Versions/digests, SBOM, sandbox, non-exécution des mappings utilisateurs |
| Prompt injection dans une source | Séparer instructions et données; ne jamais accorder des outils ou des droits via texte source |
| Fuite par rapport de diagnostic | Redaction et test de canary secrets; envoyer seulement des constats synthétiques |
| Autorisation révoquée | Arrêt de la suite, purge ou restriction selon politique propriétaire |
| Résultat IA qui « s'auto-valide » | Validation déterministe + revue humaine; aucune transition canonique |
| Erreur de tenant ou instance Médiathèque | Refus et aucun octet retourné |
| Changement des conditions d'un fournisseur | Mise en quarantaine du connecteur et réexamen légal |
| CSV formula injection | Neutraliser l'export humain et tester `=`, `+`, `-`, `@` en début de cellules dangereuses |
| DoS par lots | Quotas, backpressure, annulation, budget, timeouts |

## 4. Politique de stockage

- **Source originale** : chez son propriétaire ou un gardien approuvé, jamais dupliquée automatiquement comme source vérité DaaT.
- **Représentation temporaire** : seulement si permise, séparée par tenant et avec TTL documentée.
- **Journal DaaT** : IDs, digest, état et erreurs expurgées, pas de contenu sensible.
- **Index de contexte** : dérivé local et révocable, tenant+purpose scoped; sa légitimité suit les droits de ses sources.
- **Dossier exporté** : version avec contenu **réellement divulgable** à la destination; aucune clé, donnée non autorisée ou texte masqué.

## 5. Gouvernance et propriétaires

Konfid/host décide de l'accès au périmètre autorisé; IK du transport de messages adoptés; Médiathèque de la conservation; Skope/son propriétaire de certaines acquisitions; DaaT de son mapping et de la préparation du contexte; fournisseur IA de ses conditions de service/traitement données; l'opérateur final de l'acte manuel d'envoi. Un changement de propriétaire ou d'API nécessite un ADR/contrat approprié, pas un champ inventé.

## 6. Critère libératoire de sécurité

Tous les tests d'isolation, de révocation, d'injection, de limites de ressources et de fuite doivent passer en environnement représentatif. Les plateformes dont les droits restent indéterminés peuvent être **répertoriées** mais pas déclarées connectées. Les données privées sensibles ne peuvent pas être envoyées à une IA externe simplement pour tester le fonctionnement de la fonctionnalité.
