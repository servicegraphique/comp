# Rapport de migration Webflow → sites locaux

**Date de l'audit :** 28 octobre 2026  
**Dossier prêt à lancer :** `migration/sites/`  
**Guide local :** `migration/README-LOCAL.md`

## Résumé de l'avancement

| Mesure | Résultat |
|---|---:|
| Exports HTML identifiés dans l'inventaire GitHub | 138 |
| Pages exportées dans un dossier autonome | **138 / 138** |
| Pages/pages de test converties | 131 LP + 7 templates/tests |
| Dossiers de page avec `index.html`, `style.css`, `script.js`, `img/` | **138 / 138** |
| Références locales HTML/CSS cassées | **0** |
| Fichiers JavaScript vérifiés par Node | **138 / 138 — syntaxe valide** |
| Ressources de présentation externes non résolues | **1 : vidéo YouTube sur Primagaz** |
| Tests visuels navigateur complets | **0 / 138** (bloqués par l'environnement, détails ci-dessous) |

L'export historique `sites/assurance-tns/index.html` est un doublon du pilote et n'est pas compté comme une page supplémentaire. Les exports originaux restent en place; les dossiers autonomes générés sont regroupés sous `migration/sites/<slug>/`.

## Travail réalisé

- Ajout d'une lecture locale prioritaire dans `migration/lp2site.py`, qui réutilise les HTML, CSS, JS et médias déjà présents dans le dépôt au lieu d'exiger l'accès à `raw.githubusercontent.com`.
- Conversion des 7 templates/tests auparavant exclus, avec leur propre HTML, feuille de style, script et ressources.
- Regroupement des bibliothèques nécessaires dans le `script.js` autonome de chaque page. Le projet utilise encore le runtime compatible Webflow **vendu localement** afin de préserver les interactions/export IX2 et la fidélité du rendu; il n'est pas téléchargé depuis un service Webflow.
- Remplacement du helper externe de formulaires multi-étapes par une version native HTML/JavaScript, et rapatriement local des scripts jQuery, Inputmask et ticker rencontrés dans les templates.
- Retrait des appels GTM/gtag et du loader Google Fonts dans les versions locales. Les polices et ressources récupérées sont locales.
- Réécriture des vidéos Webflow transcodées vers les fichiers locaux, remplacement des iframes internes d'ubepro/Comparateurpro par leurs pages sœurs locales et localisation des liens d'ancrage vers les pages légales/confidentialité disponibles dans l'export.
- Correction de collisions de déclarations `const` entre scripts exportés qui faisaient échouer deux bundles JavaScript.
- Ajout du catalogue filtrable `migration/sites/index.html` et de son générateur `migration/generer-catalogue.py`.

## Contrôles exécutés

1. `python3 migration/verifier-autonomie.py` : 138 dossiers audités, aucune structure manquante, aucun chemin local cassé, aucun appel de ressource CDN inattendu, aucune erreur de syntaxe JS. Le script signale explicitement l'iframe YouTube conservée.
2. `python3 migration/docteur-sites.py migration/sites --verifier` : 138 pages, toutes `OK` pour les défauts statiques connus.
3. Contrôle HTTP local sur `index.html`, `style.css` et `script.js` de chacune des 138 pages : **414/414 réponses 200**.
4. Test unitaire isolé du remplacement natif multi-étapes : état initial, validation d'un champ requis, navigation routée `data-go-to` et retour arrière réussis.
5. Vérification Playwright tentée, mais Chromium ne peut pas démarrer dans cet environnement : la bibliothèque système `libnss3.so` manque. Aucune comparaison visuelle réelle, aucun parcours utilisateur navigateur complet et aucun contrôle responsive visuel ne sont donc déclarés comme validés.

## Dépendances encore présentes / limites

- **Formulaires métier :** les URLs CRM, SMS/OTP et Google Apps Script/Sheets restent celles de la production. Elles sont conservées sans simulation; l'envoi réel nécessite réseau, CORS/origine autorisée, configuration des API et données de test autorisées.
- **YouTube :** l'iframe de `primagaz-obtenez-votre-gaz-propane-a-prix-fixe` demeure distante car le média source n'est pas fourni dans les exports. La page et son image de présentation chargent localement, mais la vidéo ne fonctionne pas hors ligne.
- **Liens partenaires :** liens de navigation externes conservés comme tels; ils ne sont pas nécessaires au rendu initial.
- **Runtime Webflow local :** les scripts et styles ne dépendent pas d'un hébergement Webflow pour charger. Néanmoins, le runtime JavaScript Webflow, conservé localement dans chaque bundle, reste une dépendance de compatibilité pour préserver les interactions exportées. Sa réécriture intégrale en composants natifs et sa validation visuelle par page restent un chantier QA, non une tâche que ce rapport prétend achevée.
- **Tracking :** GTM/gtag est désactivé dans les copies locales; les événements ne sont pas expédiés depuis le serveur de test.
- **Navigateurs :** tests visuels, Lighthouse mobile, sliders/modales/parcours conditionnels et tests réels des formulaires à effectuer dans un environnement équipé d'un Chromium compatible et avec des API de préproduction. Aucun faux succès d'envoi de formulaire n'est implémenté.

## Procédure de lancement et d'audit

Depuis la racine du dépôt :

```bash
python3 -m http.server 8000 --directory migration/sites
```

Ouvrir <http://localhost:8000/> pour le catalogue. Pour revalider les ressources et le JavaScript :

```bash
python3 migration/verifier-autonomie.py
python3 migration/docteur-sites.py migration/sites --verifier
```

**Conclusion :** les 138 exports sont désormais isolés par dossier et peuvent être servis depuis le dépôt sans CDN Webflow/Google pour leurs ressources d'affichage. La conversion structurelle et les contrôles statiques sont terminés; la validation navigateur exhaustive et la simulation locale des API métier ne le sont pas, et ne sont pas présentées comme telles.
