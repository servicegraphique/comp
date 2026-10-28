# Bibliothèques locales utilisées par le convertisseur

Le générateur intègre ces ressources dans le `script.js` de chaque dossier de page; les sites ne chargent pas `migration/vendor/` à l'exécution.

- `jquery-3.5.1.min.js` — jQuery 3.5.1, licence MIT/OpenJS Foundation (notice inclus dans le fichier).
- `jquery.inputmask-5.0.9.min.js` — Inputmask 5.0.9, licence MIT (notice upstream inclus dans le bundle).
- `lumious-ticker.min.js` — composant ticker Lumious 1.0.8, licence jointe (`LUMIOUS-LICENSE.txt`); nécessite jQuery, déjà intégré.
- `native-multistep.js` — remplacement local maintenu dans ce dépôt pour `videsigns/webflow-tools/multi-step.js`.
- `webflow-static/` — assets Webflow communs réutilisés localement pour compléter les exports incomplets.

Le runtime Webflow/IX2 utilisé pour compatibilité est le fichier source local `js/webflow.js`, inclus dans les bundles générés; aucune requête réseau n'est faite vers Webflow pour son chargement.
