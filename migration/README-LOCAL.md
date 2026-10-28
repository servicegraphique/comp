# Lancer les landing pages localement

Les pages statiques prêtes à tester se trouvent dans `migration/sites/` : **138 pages**, chacune dans son propre dossier avec `index.html`, `style.css`, `script.js`, `img/` et, si nécessaire, `fonts/` et `videos/`. Le dépôt source (les exports Webflow d'origine) reste intact. Les 7 pages de template/test du dépôt sont également exportées sous `migration/sites/`.

## Démarrage — le plus simple

Depuis la racine du dépôt :

```bash
python3 -m http.server 8000 --directory migration/sites
```

Puis ouvrir <http://localhost:8000/>. La page d'accueil est un catalogue filtrable; cliquez sur une LP. Pour arrêter le serveur, faites `Ctrl+C` dans le terminal.

Autre possibilité : ouvrir directement `migration/sites/<slug>/index.html` dans le navigateur. **Le serveur local est recommandé** : certains navigateurs bloquent les scripts, polices ou formulaires sur `file://`.

## Ce qui est déjà local

- Le HTML des pages converties, le CSS (dont les styles Webflow nécessaires), le JavaScript, les images, les polices et les vidéos disponibles sont embarqués au niveau de chaque page.
- Les interactions historiques Webflow continuent de fonctionner à partir du runtime compatible livré dans le `script.js` propre à chaque page; jQuery et ce runtime ne sont pas chargés depuis un CDN.
- Les ressources d'affichage Webflow/Google Fonts sont locales. Les loaders Google Fonts et Google Tag Manager/analytics ont été désactivés dans la copie locale. Le catalogue et sa recherche fonctionnent sans CDN.
- Chaque LP peut être copiée et hébergée indépendamment depuis son dossier.

## Limites à connaître

Le rendu et les interactions front-end sont locaux, mais les services en ligne ne deviennent pas des services locaux. Les envois CRM, SMS/OTP et Google Sheets/Apps Script gardent leurs API réelles et exigent réseau, configuration d'origine/CORS et autorisation. Ils ne sont pas simulés; **ne testez pas un formulaire avec des données réelles**. Le tracking GTM/gtag est retiré localement. Une vidéo YouTube sur Primagaz reste la seule ressource d'affichage distante identifiée et ne sera pas lisible hors ligne. Les liens de navigation partenaires restent externes par nature.

L’export source `sites/assurance-tns/index.html` correspond au pilote historique déjà présent sous `migration/sites/assurance-tns/`; il n’est pas compté deux fois. Les médias absents de l’export original restent notés dans `MISSING.txt` et les rapports individuels.

## Vérification

Depuis la racine du dépôt :

```bash
python3 migration/docteur-sites.py migration/sites --verifier
```

Le diagnostic contrôle les références locales et les défauts connus du JavaScript. Le rapport est écrit dans `migration/sites/DIAGNOSTIC-SITES.md`. Une page `OK` signifie que les références locales contrôlées sont présentes; cela ne garantit pas le parcours réel d'un formulaire ou l'accès aux API tierces.

Pour régénérer les sites après une modification source, voir `migration/PLAN-MIGRATION.md` et `migration/lp2site.py`. Après conversion, relancer le diagnostic et vérifier à la main les interactions critiques du rapport de chaque site.
