# 01 — Mandat, objectifs, utilisateurs et exigences

**Statut** : `[PROPOSAL]` — spécification intégrale, non certification de l'existant.

## 1. Vision de produit

Un utilisateur indique **un sujet, un corpus, une plateforme ou une collection**. DaaT révèle les voies possibles, distingue ce qui est accessible de ce qui ne l'est pas, planifie la collecte par les bons propriétaires, récupère les références/artefacts autorisés, les rend comparables sans déformer le sens, structure la provenance et les prépare dans un paquet portable pour **ChatGPT ou une autre interface explicitement autorisée**. Un opérateur peut employer ChatGPT par copier-coller quand l'API n'est pas disponible ou pas permise. La sortie n'est jamais une vérité canonique ni un Kristal.

## 2. Frontière du produit

**Inclus** : découverte, registre de capacités, plan de collecte, choix justifié, import de lots autorisés, adaptateurs hôtes, validation des entrées, classification des formes, extraction textuelle et structurée, segmentation, enrichissement documentaire autorisé, références, dédoublonnage, révisions, retraits, droits, vue de corpus, recherche/filtrage local (sans devenir un entrepôt autoritaire), paquets contextuels, prompts, boucle IA supervisée, rapports, journal opérationnel minimal, audit, diagnostic.

**Exclus** : génération de KQ/KP/KA/KS, import ou build par Kit, publication/activation, certification sémantique universelle, web scraping d'espaces privés, passage de paywall, collecte de cookies, réutilisation des identifiants de l'utilisateur à son insu, moteur de messages concurrent à IK, ordonnanceur business concurrent à Orgo, bibliothèque documentaire concurrente à Médiathèque, IdP/PEP parallèle à Konfid, stockage durable des originaux sans autorité propriétaire.

## 3. Utilisateurs et parcours

| Acteur | Objectif | Capacités attendues | Limitations |
|---|---|---|---|
| Individu / chercheur | Transformer ses lectures et sources en contexte exploitable | URL/référence, RSS, import Zotero, bibliographies, lot ZIP, prompt ChatGPT | Ne transmet que les contenus permis |
| Auteur Medium | Exploiter ses propres articles | ZIP/HTML exporté, historique, lots, citations | Compte connecté dans le navigateur, aucun vol de session |
| Équipe documentaire | Unifier plusieurs catalogues et exports | Profils de sources, filtres, checkpoints, provenance, rôles | Contrôle tenant/projets et licence |
| Organisation/PME | Préparer des données Acomba/ERP autorisées | Import d'exports, masquage PII, relecture, dossier d'information | Pas d'écritures dans le système comptable |
| Administrateur | Prévoir performances, secret vault, licences et cas bloqués | Diagnostics, rapports par fournisseur, validation hôte | Pas de privilèges automatiques |
| Développeur de connecteur | Implémenter une voie officiellement documentée | SDK de port, jeux de tests, observabilité, versions | Contrat du propriétaire et sandbox obligatoires |

## 4. Exigences fonctionnelles (toutes requises dans la cible)

**EF-01** Recherche et sélection d'une source parmi les 89 profils, avec extension sans code métier spécifique. **EF-02** Affichage pour chaque source des voies, authentifications, contenus accessibles, droits et état vérifié. **EF-03** Plan de résolution multi-sources qui préserve la granularité. **EF-04** Routage vers L1–L8, avec repli expliqué et non contournant. **EF-05** Import utilisateur unitaire et par lots. **EF-06** APIs/feeds/exports selon approbations et implémentations hôtes. **EF-07** Synchronisation déterministe, pagination et reprise. **EF-08** Inspection/parsing des formats déclarés et détection des contenus non traitables. **EF-09** Métadonnées/texte/segments structurés sous forme de références, sans copie interdite. **EF-10** Provenance par fragment, modèle de version et liens entre sources. **EF-11** Détection de doublons exacte et candidate. **EF-12** Recherche, regroupement et comparaison de corpus. **EF-13** Déclaration et application des droits de transmission IA. **EF-14** Génération de prompts et dossiers contextuels sensibles au budget de contexte. **EF-15** Boucle ChatGPT manuelle de soumission/reprise/correction. **EF-16** Route IA connectée optionnelle sous autorisation et contrôles d'exfiltration. **EF-17** Revue humaine des annotations IA et des citations. **EF-18** Export portable JSON + Markdown/texte + manifestes d'intégrité, sans identifiants canoniques. **EF-19** DaaT_Diag et rapports exploités automatiquement. **EF-20** Interface Windows sans console parasite, progression réelle, CLI hors ligne et mode serveur seulement si ADR/host approuvé. **EF-21** États de refus explicites, requêtes d'accès et alternative manuelle permise. **EF-22** Traçabilité des choix et reproducibilité.

## 5. Exigences non fonctionnelles

**ENF-01** Séparation tenant/acteur et source, moindre privilège, révocation. **ENF-02** Pas de mots de passe/tokens/cookies dans les sorties. **ENF-03** Réseau interdit par défaut dans les lecteurs locaux; egress hôte allowlisté pour connecteurs activés. **ENF-04** Toute opération bornée en volume/temps/mémoire; échec sûr. **ENF-05** Aucune élévation automatique d'un résumé à un texte complet ou à une vérité. **ENF-06** Un même snapshot+configuration donne le même résultat déterministe; IA séparée. **ENF-07** Reprise sûre et idempotence sans double effet, par système propriétaire. **ENF-08** Journaux expurgés et durées de conservation appliquées. **ENF-09** Export/provenance vérifiables, SHA-256 sans prétendre à une signature. **ENF-10** Compatibilité avec l'inventaire kOA et les limites des contrats IK/Konfid/Médiathèque. **ENF-11** Diagnostics de couverture et de dérive pour 36 familles et 89 profils. **ENF-12** Mise à jour de la documentation des plateformes et licences versionnée.

## 6. Sens du mot « universel »

Le système **ne promet pas l'accès à tous les contenus**. « Universel » signifie : accueillir toute source décrivable, afficher les voies possibles, obtenir seulement le contenu autorisé, ou s'arrêter proprement en produisant une référence/lacune exploitable. La conformité à 89/89 signifie que chaque fiche offre une décision vérifiable ou un blocage motivé; elle ne signifie pas que 89 connecteurs actifs disposent de toutes les licences.

## 7. Critère produit central

Un lot mixte PhilPapers + Medium + Zotero + PDF local + dépôt Git + export comptable doit aboutir à un **Context Bundle** composé de fragments réellement disponibles, références versionnées, auteur/provenance, droits de partage, avertissements, questions ouvertes, liens et prompts. Si un passage est interdit à la transmission IA, le paquet transmis à ChatGPT l'exclut; le rapport conserve le motif d'exclusion sans divulguer le contenu.
