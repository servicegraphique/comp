# Lancer les landing pages localement

Les pages statiques prêtes à tester se trouvent dans `migration/sites/` : **131 pages**, chacune dans son propre dossier avec `index.html`, `style.css`, `script.js`, `img/` et, si nécessaire, `fonts/` et `videos/`. Le dépôt source (les exports Webflow d'origine) reste intact.

## Démarrage — le plus simple

Depuis la racine du dépôt :

```bash
python3 -m http.server 8000 --directory migration/sites
```

Puis ouvrir <http://localhost:8000/>. La page d'accueil est un catalogue filtrable; cliquez sur une LP. Pour arrêter le serveur, faites `Ctrl+C` dans le terminal.

Autre possibilité : ouvrir directement `migration/sites/<slug>/index.html` dans le navigateur. **Le serveur local est recommandé** : certains navigateurs bloquent les scripts, polices ou formulaires sur `file://`.

## Ce qui est déjà local

- Le HTML des pages converties, le CSS (dont les styles Webflow nécessaires), le JavaScript, les images, les polices et les vidéos disponibles sont embarqués au niveau de chaque page.
- jQuery et le runtime Webflow nécessaires aux interactions exportées sont servis depuis les fichiers locaux; les fichiers ne chargent pas jQuery ni le runtime depuis un CDN Webflow.
- Les références d'affichage aux CDN Webflow / Google Fonts ont été rapatriées. Le catalogue et le code de recherche fonctionnent aussi sans CDN.
- Chaque LP peut être copiée et hébergée indépendamment depuis son dossier.

## Limites à connaître

« Fonctionner localement » couvre le rendu et les interactions front-end exportées, mais ne transforme pas les services en ligne en services locaux. Les formulaires pouvant envoyer des leads, SMS/OTP, CRM, Google Sheets/Apps Script, Google Tag Manager/analytics, vidéos hébergées par des tiers et liens de partenaires dépendent encore de leurs services distants; certains nécessitent Internet, une configuration d'origine/CORS ou un compte. Ils n'ont pas été remplacés par des réponses simulées, afin de ne pas perdre ni falsifier des soumissions réelles. **Ne testez pas un formulaire de production avec des données réelles.** Une vraie exécution hors ligne de ces fonctions nécessiterait des API de remplacement locales et un environnement de test dédié.

Les 7 templates/pages de test du dépôt source ne sont pas convertis en LP : `nicolas/ayvens.html`, `nicolas/form-test.html`, `nicolas/formly.html`, `temlpate-webflow/comparateur-2.html`, `comparateur-3.html`, `comparateur-4.html` et `webflow/template-1.html`. L'export source `sites/assurance-tns/index.html` est un doublon du pilote déjà converti sous `migration/sites/assurance-tns/`. Les vidéos citées dans `MISSING.txt` n'ont pas pu être embarquées; les rapports par site consignent les alertes connues.

## Vérification

Depuis la racine du dépôt :

```bash
python3 migration/docteur-sites.py migration/sites --verifier
```

Le diagnostic contrôle les références locales et les défauts connus du JavaScript. Le rapport est écrit dans `migration/sites/DIAGNOSTIC-SITES.md`. Une page `OK` signifie que les références locales contrôlées sont présentes; cela ne garantit pas le parcours réel d'un formulaire ou l'accès aux API tierces.

Pour régénérer les sites après une modification source, voir `migration/PLAN-MIGRATION.md` et `migration/lp2site.py`. Après conversion, relancer le diagnostic et vérifier à la main les interactions critiques du rapport de chaque site.
