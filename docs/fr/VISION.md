# DaaT — Vision fondatrice (français)

**DaaT permet l'interopérabilité sans imposer l'uniformité.** Un système externe peut se connecter à l'écosystème tel qu'il est aujourd'hui, en utilisant un adaptateur plus ou moins élaboré. La quantité de transformations nécessaires exprime sa **distance aux contrats natifs** pour une capacité déterminée; elle ne mesure ni sa valeur, ni sa qualité, ni son intelligence.

## Principe architectural

Les composants internes doivent tendre vers des contrats partagés, explicitement versionnés et testés. Il n'est pas souhaitable de maintenir des traductions internes artificielles : Kristal définit les connaissances, Interaction Kernel transporte les interactions, Orgo orchestre, Ekole gère les apprentissages et leurs preuves, Kontexte définit les situations, SemantiK réalise des formulations contrôlées.

Pour les **systèmes externes**, DaaT reste toujours disponible comme frontière d'entrée : admission, identité et autorisations, contrats, mapping lorsque nécessaire, livraison, références d'artefacts et diagnostic.

## Trois expériences légitimes

1. **Application déjà alignée :** DaaT minimal; aucune transformation sémantique, mais les contrôles de sécurité demeurent.
2. **Application partiellement alignée :** quelques conversions de structure ou de vocabulaire, explicites et validées.
3. **Application utilisant une architecture différente :** adaptateur plus étendu, mais participant parfaitement légitime dès lors que ses échanges satisfont les contrats choisis et leurs contrôles.

## L'incitation implicite

Un développeur externe peut constater, version après version, que certaines transformations deviennent inutiles s'il adopte spontanément des représentations déjà compatibles. Il n'y a **ni obligation de se conformer à l'intérieur de son application**, ni pénalité publique pour posséder un DaaT plus élaboré. La mesure doit être reproductible, contextualisée et indépendante du simple nombre de lignes de code.

## Ce que DaaT n'est pas

DaaT n'est pas un deuxième Interaction Kernel, un deuxième Kristal, un moteur d'Orgo, un entrepôt de données, un acquéreur de sources ou une autorité sémantique. Il ne peut inventer une identité canonique, reconnaître automatiquement une connaissance, attribuer des droits ou prendre possession de l'état d'une autre application.

## Statut technique actuel

Le snapshot d'Interaction Kernel contient un adaptateur DaaT de référence centré sur Kristal, et des contrats IK existants. Un service générique d'intégration externe complet **n'est pas démontré comme existant**. La documentation technique anglaise de ce dépôt constitue un **plan de construction** à mettre en œuvre et à valider par étapes.

## Formulation à retenir

> **DaaT garantit l'interopérabilité sans imposer l'uniformité. La complexité de ses adaptations constitue une mesure contextualisée de l'écart entre les contrats, et une référence de convergence volontaire.**
