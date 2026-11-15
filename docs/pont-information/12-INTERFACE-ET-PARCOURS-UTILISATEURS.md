# 12 — DaaT Studio : parcours utilisateur et cahier d'interface

**Statut** : `[PROPOSAL]` — les lanceurs GUI 0.4.4 de registre/ChatGPT existent, **pas** cette interface intégrée.

## 1. Principes UX

Une expérience guidée qui ne demande jamais à l'utilisateur de savoir si une plateforme a une API. L’interface explique : « ce que nous avons trouvé », « ce que nous pouvons légalement utiliser », « ce qui manque », « ce qui sera transmis à ChatGPT ». Pas de fenêtres CMD qui clignotent; la progression correspond à des événements réels, pas une simulation.

## 2. Écrans cibles

**Écran A — Projet/contextualisation.** Nom du projet, question(s), tenant/identité fournie par le host, finalité, sensibilité, budget de source et de contexte IA, conservation, langue.

**B — Catalogue universel.** Recherche sur 89 profils/36 familles, badges « documenté / non vérifié / autorisé ici / indisponible », voie recommandée, portées possibles, documentation officielle et conditions. Permet « ajouter plusieurs sources » sans confusion entre le profil et l'autorisation personnelle.

**C — Plan de collecte.** Vue des sources, voies L1–L8, quota/délai/volume, autorisations requises, dossiers, lot d'exports, plan de secours par format; `Lancer` désactivé si action non autorisée.

**D — Obtention de droits.** Déport vers navigateur/hôte pour OAuth, ou instruction d'export autorisé. DaaT ne saisit aucun mot de passe; ne pas suggérer qu'une case « j'ai accès » constitue le consentement d'un tiers.

**E — Exécution et progression.** Compteur `découverts / accessibles / récupérés / référencés / extraits / exclus`, source active, taille/cout/quotas, vitesse, annuler/reprendre, erreurs spécifiques, rapport en direct. Réserves : la progression des APIs à total inconnu est indéterminée, avec compteur exact, pas pourcentage faux.

**F — Corpus.** Filtre par source, niveau de contenu, auteurs, date, droits, statut et thème; visualisation d'originaux via le custodian si permis, métadonnées, passages, DOI/URL, différences de versions, doublons candidats, contradictions attribuées.

**G — Préparation ChatGPT.** Choisir fragments, format `JSON/MD`, budget de texte, gabarit prompt, destination, effacer PII si requis, voir avant d'envoyer, liste d'exclusions et incertitudes. « Copier le prompt », « Exporter le contexte » et, sous hôte autorisé, « Envoyer » distincts.

**H — Retour ChatGPT.** Coller un JSON, valider les ancrages, signaler les citations inventées, proposer prompt de correction, revue humaine. Résultat = **dossier révisé**, pas Kristal.

**I — Feedback/diagnostic.** Rapport de sources, contrats, rejets, confidentialité, performances, test de connecteurs, export ZIP expurgé pour assistance.

## 3. États UX à représenter sans ambiguïté

`NOT_DOCUMENTED`, `DOCUMENTED_NOT_TESTED`, `AVAILABLE_WITH_PERMISSION`, `METADATA_ONLY`, `USER_ACTION_REQUIRED`, `RESTRICTED`, `BLOCKED_BY_POLICY`, `TEMPORARILY_UNAVAILABLE`, `REVOKED`, `READY_FOR_CHATGPT_MANUAL`, `READY_FOR_APPROVED_AI_HOST` (étiquettes d'interface, **pas de codes IK**). Chaque étiquette porte : explication, preuve, action permise, lien vers source officielle et date du contrôle.

## 4. Accessibilité et intégration Windows

Launcher `.pyw`/`pythonw.exe` ou binaire signé si distribué; aucun CMD parasite. Barre de progression pilotée par événements, bouton Annuler, reprise sûre, statut lisible sans dépendre d'une couleur, navigation clavier, textes français/anglais, erreurs reproductibles, contraste, gros corpus sans gel UI (worker async ou processus hôte isolé). Le GUI ne doit jamais stocker des credentials en fichiers `.json` de projet.

## 5. Parcours simplifié pour débutants

« J'ai une URL Medium » → détecter fiche → proposer RSS pour découvrir les titres → demander export propriétaire ou extrait autorisé pour lire le texte → préparer un dossier de sources → générer prompt → validation. « J'ai une liste PhilPapers » → récupérer les notices éligibles sous conditions documentées → proposer DOI/texte OA autorisé → paquet metadata/abstract explicite. « J'ai mes propres fichiers » → drag/drop avec droits et niveaux de confidentialité.

## 6. Administration

Tableau de licences et sources, consentements expirants, quotas, coût API, systèmes de stockage, health des connecteurs, incidents de sécurité, statut de couverture, charge actuelle et logs minimisés. Historique des versions de registry sans masquer les profils non qualifiés.
