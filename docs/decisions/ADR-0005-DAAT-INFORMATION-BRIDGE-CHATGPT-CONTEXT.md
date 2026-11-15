# ADR-0005 (PROPOSÉ) — DaaT : sortie Context Bundle, aucune construction Kristal

**Date** : 2026-11-14. **Statut** : `PROPOSED_NOT_ADOPTED`. **Portée** : DaaT et ses consommateurs de contexte, **pas** changement d'un contrat IK/Kristal.

## Contexte

Le dépôt DaaT inclut une voie offline vers des candidats non canoniques et un registre de 36 familles/89 profils. Le mandat désormais demandé est de construire un **pont d'information** allant des sources aux dossiers prêts à utiliser avec ChatGPT; la construction de Kristals et la publication en sont explicitement exclues. L'usage du terme « Kristal » dans certains chemins historiques ne doit pas suggérer une autorité ou une nécessité du build.

## Décision proposée

1. Définir une **sortie contextuelle locale versionnée** et portable, dont le contenu est borné par les droits de divulgation au destinataire IA.
2. Garder la collecte sous source/host propriétaire et le stockage sous custodian approuvé; DaaT choisit et vérifie l'admission/transformation, sans créer un double bus, IdP ou entrepôt.
3. Préserver la différence entre notice, résumé, extrait, texte intégral et données structurées; sources/révisions/fragments/citations vérifiables.
4. Maintenir deux voies AI (manuel et host API approuvé) soumises à même règle de divulgation; l'IA ne décide pas des droits ou de la vérité.
5. Réutiliser les 36 familles/89 fiches comme **recherche**, puis qualifier les capacités réelles; repli bloqué/manuel légal.
6. Conserver les commandes historiques sous compatibilité explicitement étiquetée si nécessaire, mais pas dans le contrat nouveau.
7. Déclarer la livraison complète seulement lorsque les barrières G1–G8 du dossier `docs/pont-information/15-*` passent.

## Alternatives examinées

- Tout construire dans DaaT, y compris stockage brut, bus et IAM : **rejeté** (violation des responsabilités owners).
- Automatiser le scraping de Medium/PhilPapers : **rejeté** (droits et capacité non garantis).
- Forcer une conversion immédiate vers Kit/Kristal : **rejeté pour ce mandat**, hors périmètre.
- Un mode purement copier-coller sans API/feeds : **rejeté** (impossible de traiter les lots et les mises à jour à l'échelle).

## Conséquences et approbations

Nécessite modèle de données local, interfaces hôtes, contrôles de droits, tests bilatéraux et nouvelle couverture DaaT_Diag. **Ne propose aucun nouvel ID de profil réseau IK**. Les owners IK/Konfid/Skope/Médiathèque et sources doivent adopter leurs propres modifications, s'il en faut, avant effets externes. Aucune approbation n'est déduite de ce fichier.
