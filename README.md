# 🚀 Template Docker - Symfony + PostgreSQL + Nginx

<div align="center">

![Symfony](https://img.shields.io/badge/Symfony-8.0-000000?style=for-the-badge&logo=symfony)
![PHP](https://img.shields.io/badge/PHP-8.4-777BB4?style=for-the-badge&logo=php&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-1.27-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![pgAdmin](https://img.shields.io/badge/pgAdmin-4-336791?style=for-the-badge&logo=postgresql&logoColor=white)

[![License](https://img.shields.io/badge/License-Private-red?style=for-the-badge)](LICENSE)
![Maintenance](https://img.shields.io/badge/Maintained-Yes-green?style=for-the-badge)

</div>

Template prêt à l'emploi pour démarrer rapidement un projet Symfony avec Docker, Nginx et PostgreSQL.

**Symfony 8.0 skeleton déjà installé** - Clone, configure et démarre en 5 commandes !

## 📦 Stack technique

- **PHP** 8.4-FPM avec Xdebug
- **Symfony** 8.0 skeleton
- **PostgreSQL** 18
- **pgAdmin** 4 (interface web pour PostgreSQL)
- **Nginx** 1.27+
- **Docker** & Docker Compose
- **Symfony CLI** intégré

---

## 🎯 Fonctionnalités

✅ **Symfony 8.0 skeleton déjà installé** - Clone et démarre !  
✅ Configuration Docker optimisée  
✅ Nginx configuré comme reverse proxy  
✅ PostgreSQL 18 avec persistence des données  
✅ pgAdmin intégré (interface web pour gérer PostgreSQL)  
✅ Makefile avec 70+ raccourcis pratiques  
✅ Xdebug configuré pour le développement  
✅ Health checks intégrés sur tous les services  
✅ Variables d'environnement sécurisées  
✅ Symfony CLI pré-installé  
✅ Upgrade en webapp (site web) en 1 commande  
✅ Upgrade en API (API Platform) en 1 commande

---

## 📋 Prérequis

- Docker >= 20.10
- Docker Compose >= 2.0
- Git

### Configuration du template

Le template utilise :
- PHP 8.4 avec toutes les extensions Symfony 8.0 ✅
- Symfony CLI intégré ✅
- Composer 2.9 ✅
- PostgreSQL 18
- Nginx 1.27

> 💡 Aucune installation locale requise ! Tout tourne dans Docker.

---

## 🚀 Installation rapide

> 💡 **Ce template contient déjà Symfony 8 skeleton installé !** Tu n'as qu'à cloner, configurer et démarrer.

### ⚡ Installation avec Make (Recommandé)

**La méthode la plus rapide - 3 commandes :**

```bash
# 1. Cloner le template
git clone https://github.com/teowaep/docker-spn-template.git mon-projet
cd mon-projet

# 2. Supprimer l'historique Git du template
rm -rf .git
git init

# 3. Configurer l'environnement
cp .env.example .env
nano .env  # Remplis POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB

# 4. Démarrer tout !
make setup

# 5. Lancer le terminal
make bash
```

**C'est tout ! 🎉** Ton projet est prêt à **http://localhost:8080**

### 🔧 Installation classique (Sans Make)

**Si tu n'as pas Make installé :**

```bash
# 1. Cloner le template
git clone https://github.com/teowaep/docker-spn-template.git mon-projet
cd mon-projet

# 2. Supprimer l'historique Git du template
rm -rf .git
git init

# 3. Configurer l'environnement
cp .env.example .env
nano .env  # Remplis POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB

# 4. Ajuster DATABASE_URL dans .env
# Remplace cette ligne :
# DATABASE_URL="postgresql://app:!ChangeMe!@127.0.0.1:5432/app?serverVersion=16&charset=utf8"
# Par :
# DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@backend-postgres:${POSTGRES_PORT}/${POSTGRES_DB}?serverVersion=18&charset=utf8"

# 5. Build et démarrer les containers
docker-compose build
docker-compose up -d

# 6. Corriger les permissions
docker-compose exec backend-php chmod -R 777 var/

# 7. Installer les dépendances
docker-compose exec backend-php composer install

# 8. Créer la base de données (nécessite Doctrine - voir ci-dessous)
docker-compose exec backend-php bash
composer require symfony/orm-pack
symfony console doctrine:database:create
exit
```

**Ton projet est prêt !** Ouvre **http://localhost:8080** 🎉

---

### 🎯 Variables .env importantes

```env
# Symfony
APP_ENV=dev
APP_SECRET=genere-un-secret-avec-openssl-rand-hex-32

# PostgreSQL (pour Docker)
POSTGRES_DB=mon_projet_db
POSTGRES_USER=mon_user
POSTGRES_PASSWORD=mon_password_securise
POSTGRES_PORT=5432

# Database URL (pour Symfony)
DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@backend-postgres:${POSTGRES_PORT}/${POSTGRES_DB}?serverVersion=18&charset=utf8"
```

💡 **Générer APP_SECRET :**
```bash
openssl rand -hex 32
```

---

### 📦 Choisir ta stack (Optionnel)

Le template contient **Symfony skeleton** (version minimale). Tu peux l'upgrader selon tes besoins :

#### Option 1 : Webapp (Site web classique)

**Avec Make :**
```bash
make upgrade-webapp
```

**Sans Make :**
```bash
docker-compose exec backend-php composer require webapp
```

**Inclut :** Twig, Doctrine, Formulaires, Sécurité, Asset Mapper

---

#### Option 2 : API (API REST)

**Avec Make :**
```bash
make upgrade-api
```

**Sans Make :**
```bash
docker-compose exec backend-php composer require api
```

**Inclut :** API Platform, Doctrine, Serializer, Validation

Documentation API disponible à : **http://localhost:8080/api**

---

**Différences skeleton / webapp / api :**

| Fonctionnalité        | Skeleton (inclus) | Webapp | API |
| --------------------- | ----------------- | ------ | --- |
| Framework de base     | ✅                 | ✅      | ✅   |
| Twig (templates)      | ❌                 | ✅      | ❌   |
| Doctrine (ORM)        | ❌                 | ✅      | ✅   |
| Formulaires           | ❌                 | ✅      | ❌   |
| Sécurité              | ❌                 | ✅      | ✅   |
| Asset Mapper          | ❌                 | ✅      | ❌   |
| API Platform          | ❌                 | ❌      | ✅   |
| Documentation OpenAPI | ❌                 | ❌      | ✅   |

---

### 📝 Commandes utiles après installation

```bash
# Entrer dans le container PHP
make bash
# ou
docker-compose exec backend-php bash

# Créer une entité (nécessite Doctrine/webapp)
make entity name=Article

# Voir les logs
make logs-php

# Arrêter les containers
make down
```

---

## 🛠️ Commandes utiles

### 💡 Travailler comme en local

Pour une meilleure expérience de développement, **entre dans le container PHP** et travaille comme si tu étais en local :

```bash
# Entrer dans le container PHP
docker-compose exec backend-php bash

# Maintenant tu es dans le container, tu peux utiliser toutes les commandes directement !
symfony console cache:clear
symfony console make:entity
composer require symfony/mailer
symfony security:check
```

**👉 Toutes les commandes ci-dessous sont présentées comme si tu étais dans le container.**

Si tu préfères exécuter depuis l'hôte sans entrer dans le container, préfixe simplement avec :
```bash
docker-compose exec backend-php [ta-commande]
```

---

### 🔨 Utiliser le Makefile (Raccourcis pratiques)

Un **Makefile** est inclus pour simplifier l'utilisation avec des raccourcis ! 

**Voir toutes les commandes disponibles :**
```bash
make help
# ou juste
make
```

**Top 10 des commandes les plus utiles :**
```bash
make up              # Démarrer tous les containers
make down            # Arrêter tous les containers
make bash            # Entrer dans le container PHP
make logs-php        # Voir les logs PHP en direct
make cache-clear     # Vider le cache Symfony
make db-migrate      # Exécuter les migrations
make entity name=Article      # Créer une entité
make controller name=Article  # Créer un controller
make db-reset        # Reset complet de la DB
make app             # Ouvrir l'app dans le navigateur
```

**Catégories de commandes :**

<details>
<summary>🐳 Docker (10 commandes)</summary>

```bash
make up              # Démarrer les containers
make down            # Arrêter les containers
make restart         # Redémarrer
make build           # Construire les images
make rebuild         # Reconstruire (sans cache)
make ps              # État des containers
make logs            # Tous les logs
make logs-php        # Logs PHP uniquement
make logs-nginx      # Logs Nginx uniquement
make logs-db         # Logs PostgreSQL uniquement
make clean           # Supprimer tout (⚠️ volumes inclus)
```
</details>

<details>
<summary>🔧 Accès rapide (4 commandes)</summary>

```bash
make bash            # Entrer dans le container PHP
make db-shell        # Accéder au shell PostgreSQL
make pgadmin         # Ouvrir pgAdmin dans le navigateur
make app             # Ouvrir l'application dans le navigateur
```
</details>

<details>
<summary>🎵 Symfony (9 commandes)</summary>

```bash
make cache-clear                # Vider le cache
make cache-warmup              # Préchauffer le cache
make routes                     # Voir toutes les routes
make entity name=Article        # Créer une entité
make controller name=Article    # Créer un controller
make crud name=Article          # Créer un CRUD complet
make form name=Article          # Créer un formulaire
make security                   # Vérifier les vulnérabilités
make sf cmd="debug:container"   # Commande Symfony personnalisée
```
</details>

<details>
<summary>📦 Composer (5 commandes)</summary>

```bash
make composer-install                       # Installer les dépendances
make composer-update                        # Mettre à jour
make composer-require package=symfony/mailer  # Ajouter un package
make composer-remove package=symfony/mailer   # Supprimer un package
make composer-dump                          # Régénérer l'autoload
```
</details>

<details>
<summary>🗄️ Base de données (12 commandes)</summary>

```bash
make db-create       # Créer la base de données
make db-drop         # Supprimer la base de données
make db-migrate      # Exécuter les migrations
make db-migration    # Créer une nouvelle migration
make db-diff         # Générer une migration automatiquement
make db-validate     # Valider le schéma
make db-fixtures     # Charger les fixtures
make db-reset        # Reset complet (drop+create+migrate+fixtures)
make db-backup       # Créer un backup dans backups/
make db-restore file=backups/backup.sql  # Restaurer un backup
```
</details>

<details>
<summary>🧪 Tests (2 commandes)</summary>

```bash
make test            # Exécuter les tests PHPUnit
make test-coverage   # Tests avec couverture de code
```
</details>

<details>
<summary>🚀 Installation (4 commandes)</summary>

```bash
make setup              # Installation complete (Symfony deja installe)
make upgrade-webapp     # Passer de skeleton a webapp (site web)
make upgrade-api        # Passer de skeleton a API (API REST)
```
</details>

<details>
<summary>🔧 Utilitaires (7 commandes)</summary>

```bash
make fix-perms       # Corriger les permissions
make clear-cache     # Supprimer var/cache/
make clear-logs      # Supprimer var/log/
make phpstan         # Analyse statique (si installé)
make cs-fixer        # Formater le code (si installé)
make stats           # Voir stats CPU/RAM des containers
make health          # Vérifier la santé de tous les services
```
</details>

**Exemples d'utilisation :**

```bash
# Workflow quotidien
make up && make bash           # Démarrer et entrer dans PHP

# Créer une nouvelle fonctionnalité
make entity name=Product
make crud name=Product
make db-migration
make db-migrate

# Debugging
make logs-php                  # Terminal 1
make logs-db                   # Terminal 2

# Reset complet de la DB
make db-reset

# Backup avant grosse modif
make db-backup
```

💡 **Astuce :** Le Makefile est optionnel. Si tu préfères, tu peux toujours utiliser les commandes Docker classiques ou entrer dans le container avec `make bash` (ou `docker-compose exec backend-php bash`).

---

### Docker (depuis l'hôte)

```bash
# Démarrer les containers
docker-compose up -d

# Arrêter les containers
docker-compose down

# Voir les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f backend-php
docker-compose logs -f backend-nginx
docker-compose logs -f backend-postgres

# Voir l'état des containers
docker-compose ps

# Reconstruire les images
docker-compose build

# Redémarrer un service
docker-compose restart backend-php

# 🔑 Entrer dans le container PHP (recommandé pour le développement)
docker-compose exec backend-php bash

# Supprimer tout (containers + volumes)
docker-compose down -v
```

---

### Symfony (dans le container)

```bash
# Vider le cache
symfony console cache:clear

# Créer une entité
symfony console make:entity

# Créer un controller
symfony console make:controller

# Créer une migration
symfony console make:migration

# Exécuter les migrations
symfony console doctrine:migrations:migrate

# Voir les routes
symfony console debug:router

# Voir les services
symfony console debug:container

# Vérifier les vulnérabilités de sécurité
symfony security:check

# Lancer les tests
symfony php bin/phpunit
```

**💡 Astuce :** Tu peux aussi utiliser `php bin/console` au lieu de `symfony console` :
```bash
php bin/console cache:clear
php bin/console make:entity
```

---

### Composer (dans le container)

```bash
# Installer les dépendances
composer install

# Mettre à jour les dépendances
composer update

# Ajouter un package
composer require [package]

# Exemples courants :
composer require symfony/mailer
composer require symfony/messenger
composer require api-platform/core
composer require doctrine/doctrine-fixtures-bundle --dev

# Supprimer un package
composer remove [package]

# Voir les packages installés
composer show

# Rechercher un package
composer search [mot-clé]
```

---

### Base de données (dans le container)

**Commandes Doctrine :**
```bash
# Créer la base de données
symfony console doctrine:database:create

# Supprimer la base de données
symfony console doctrine:database:drop --force

# Créer une entité
symfony console make:entity

# Créer une migration
symfony console make:migration

# Voir le SQL de la migration (sans l'exécuter)
symfony console doctrine:migrations:migrate --dry-run

# Exécuter les migrations
symfony console doctrine:migrations:migrate

# Annuler la dernière migration
symfony console doctrine:migrations:migrate prev

# Charger des fixtures (si doctrine-fixtures-bundle installé)
symfony console doctrine:fixtures:load

# Valider le schéma de base de données
symfony console doctrine:schema:validate
```

**Accès direct à PostgreSQL :**
```bash
# Sortir du container PHP et accéder à PostgreSQL
# (Ou ouvrir un nouveau terminal)
exit
docker-compose exec backend-postgres psql -U ton_user -d ton_db

# Une fois dans psql :
\l                  # Lister toutes les bases
\dt                 # Lister les tables
\d+ nom_table       # Décrire une table
SELECT * FROM ...;  # Exécuter une requête
\q                  # Quitter psql
```

**Backup et restauration (depuis l'hôte) :**
```bash
# Backup
docker-compose exec backend-postgres pg_dump -U ton_user ton_db > backup.sql

# Restauration
docker-compose exec -T backend-postgres psql -U ton_user ton_db < backup.sql
```

---

## 📝 Workflow de développement typique

Voici un workflow typique pour développer avec ce template :

**Option 1 : Avec le Makefile (recommandé, plus rapide)**
```bash
# 1. Démarrer les services
make up

# 2. Vérifier que tout tourne
make ps

# 3. Entrer dans le container PHP
make bash

# 4. Créer une nouvelle entité
symfony console make:entity Article

# 5. Créer une migration
symfony console make:migration

# 6. Exécuter la migration
symfony console doctrine:migrations:migrate

# 7. Vérifier dans pgAdmin
# Lance: make pgadmin (dans un autre terminal)

# 8. Créer un controller
symfony console make:controller ArticleController

# 9. Installer un nouveau package si besoin
composer require symfony/mailer

# 10. Vérifier la sécurité
symfony security:check
```

**Option 2 : Sans Makefile (commandes Docker classiques)**
```bash
# 1. Démarrer les services
docker-compose up -d

# 2. Vérifier que tout tourne
docker-compose ps

# 3. Entrer dans le container PHP
docker-compose exec backend-php bash

# ... puis les mêmes commandes Symfony/Composer qu'au-dessus
```

### 💡 Pendant le développement

Tu peux garder **3 terminaux ouverts** :
1. **Terminal 1** - Dans le container PHP (pour les commandes Symfony/Composer)
   ```bash
   make bash
   # ou
   docker-compose exec backend-php bash
   ```
2. **Terminal 2** - Pour les logs Docker
   ```bash
   make logs-php
   # ou
   docker-compose logs -f backend-php
   ```
3. **Navigateur** - Onglet avec ton app (http://localhost:8080) + onglet pgAdmin (http://localhost:5050)

---

## ⚙️ Configuration

### Services & Ports

| Service    | Port interne | Port exposé | URL d'accès           |
| ---------- | ------------ | ----------- | --------------------- |
| Nginx      | 80           | 8080        | http://localhost:8080 |
| PHP-FPM    | 9000         | -           | (interne)             |
| PostgreSQL | 5432         | 5432        | localhost:5432        |
| pgAdmin    | 80           | 5050        | http://localhost:5050 |
| Xdebug     | 9003         | 9003        | (IDE)                 |

### Modifier les ports

**Dans `docker-compose.yml` :**
```yaml
backend-nginx:
  ports:
    - "8080:80"  # Change 8080 par le port souhaité

backend-postgres:
  ports:
    - "5432:5432"  # Change 5432 par le port souhaité
```

### Variables d'environnement

**Fichier `.env` (configuration locale) :**
```env
APP_ENV=dev                    # Environnement : dev, prod, test
APP_SECRET=xxx                 # Secret Symfony (32+ caractères)

POSTGRES_DB=nom_db            # Nom de la base de données
POSTGRES_USER=user            # Utilisateur PostgreSQL
POSTGRES_PASSWORD=password    # Mot de passe PostgreSQL
POSTGRES_PORT=5432            # Port PostgreSQL
```

---

## 🗄️ pgAdmin - Interface web pour PostgreSQL

pgAdmin est inclus dans le stack Docker et accessible via le navigateur web.

### Accès à pgAdmin

1. **Ouvre ton navigateur :** http://localhost:5050

2. **Connexion à pgAdmin :**
   ```
   Email: admin@admin.com
   Password: admin
   ```

### Configurer la connexion à ta base de données

Lors de ta première connexion, tu dois ajouter ton serveur PostgreSQL :

1. **Clic droit sur "Servers"** → **"Register"** → **"Server..."**

2. **Onglet "General" :**
   ```
   Name: Mon Projet (ou ce que tu veux)
   ```

3. **Onglet "Connection" :**
   ```
   Host name/address: backend-postgres  ← IMPORTANT ! (nom du service Docker)
   Port: 5432
   Maintenance database: postgres
   Username: ton_user (depuis .env - POSTGRES_USER)
   Password: ton_password (depuis .env - POSTGRES_PASSWORD)
   ```

4. **Coche "Save password"** (optionnel mais pratique)

5. **Clique sur "Save"**

Et voilà ! Tu peux maintenant :
- 📊 Voir toutes tes tables
- 🔍 Parcourir les données
- ✏️ Exécuter des requêtes SQL
- 📈 Visualiser les relations entre tables
- 💾 Faire des backups/imports

### 💡 Astuce

La configuration de pgAdmin est persistée dans le volume `pgadmin_data`. Tu n'auras à configurer la connexion qu'une seule fois !

### ⚠️ Note importante

Pour te connecter depuis pgAdmin (qui est dans Docker), tu **dois utiliser** le nom du service Docker (`backend-postgres`) et **pas** `localhost`. C'est parce que pgAdmin et PostgreSQL sont tous les deux dans le réseau Docker `newproject_network`.

---

## 🐛 Debugging avec Xdebug

Xdebug est pré-configuré dans l'image PHP pour le développement.

### Configuration VSCode

Crée `.vscode/launch.json` :
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Listen for Xdebug",
            "type": "php",
            "request": "launch",
            "port": 9003,
            "pathMappings": {
                "/var/www/html": "${workspaceFolder}"
            }
        }
    ]
}
```

### Configuration PhpStorm

1. **Settings → PHP → Servers**
2. Ajouter un serveur :
   - Name : `localhost`
   - Host : `localhost`
   - Port : `8080`
   - Debugger : `Xdebug`
   - Use path mappings : ✅
   - Project files → `/var/www/html`

### Activer le debug

```bash
# Xdebug est configuré avec start_with_request=trigger
# Ajoute ?XDEBUG_SESSION_START=1 à ton URL
# Ou utilise l'extension navigateur Xdebug Helper
```

---

## 🆘 Troubleshooting

### Les containers ne démarrent pas

```bash
# Voir les logs détaillés
docker-compose logs

# Reconstruire complètement
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Erreur "Permission denied"

```bash
# Depuis l'hôte
sudo chown -R $USER:$USER .

# Depuis le container
chown -R www-data:www-data var/
```

### Nginx retourne 502 Bad Gateway

```bash
# Depuis l'hôte - Vérifier que PHP-FPM tourne
docker-compose ps backend-php

# Vérifier les logs
docker-compose logs backend-php
docker-compose logs backend-nginx

# Redémarrer les services
docker-compose restart backend-php backend-nginx
```

### Impossible de se connecter à PostgreSQL

```bash
# Depuis l'hôte - Vérifier que PostgreSQL est démarré
docker-compose ps backend-postgres

# Vérifier la santé du service
docker-compose exec backend-postgres pg_isready -U ton_user

# Tester la connexion
docker-compose exec backend-postgres psql -U ton_user -d ton_db

# Dans le container PHP - Vérifier les variables d'environnement
env | grep DATABASE
```

### Xdebug ne fonctionne pas

```bash
# Dans le container - Vérifier que Xdebug est installé
php -v
# Tu devrais voir : "with Xdebug v3.x.x"

# Vérifier la configuration
php -i | grep xdebug

# Depuis l'hôte - Reconstruire l'image avec Xdebug
docker-compose build --no-cache backend-php
```

### Symfony retourne 500

```bash
# Dans le container - Vider le cache
symfony console cache:clear

# Voir les logs Symfony (dans le container ou depuis l'hôte)
tail -f var/log/dev.log

# Vérifier les permissions
ls -la var/
```

### Composer install échoue

```bash
# Dans le container - Vider le cache Composer
composer clear-cache

# Réinstaller
rm -rf vendor/
composer install
```

### pgAdmin ne se connecte pas à PostgreSQL

```bash
# Vérifie que tu utilises le bon host
Host: backend-postgres  ← PAS localhost !

# Vérifie que PostgreSQL est accessible
docker-compose exec backend-postgres pg_isready

# Vérifie les credentials dans .env
cat .env | grep POSTGRES

# Redémarre pgAdmin
docker-compose restart pgadmin
```

### Impossible d'accéder à pgAdmin (http://localhost:5050)

```bash
# Vérifier que pgAdmin tourne
docker-compose ps pgadmin

# Voir les logs
docker-compose logs pgadmin

# Redémarrer pgAdmin
docker-compose restart pgadmin

# Si ça ne marche toujours pas, reconstruire
docker-compose up -d --force-recreate pgadmin
```

---

## 🎨 Personnalisation

### Changer le nom du projet

**Dans `docker-compose.yml` :**
```yaml
name: mon-projet  # Change "newproject"

services:
  backend-php:
    container_name: mon-projet-php  # Change les noms
  backend-nginx:
    container_name: mon-projet-nginx
  backend-postgres:
    container_name: mon-projet-postgres
```

### Ajouter un service (Redis, Mailcatcher, etc.)

**Exemple : Ajouter Redis**

Dans `docker-compose.yml` :
```yaml
services:
  redis:
    image: redis:7-alpine
    container_name: newproject-redis
    ports:
      - "6379:6379"
    networks:
      - newproject_network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
```

Dans `.env` :
```env
REDIS_URL=redis://redis:6379
```

Puis dans le container PHP :
```bash
composer require symfony/redis-bundle predis/predis
```

### Modifier la version PHP

**Dans `docker/php/Dockerfile.dev` :**
```dockerfile
FROM php:8.3-fpm  # Change 8.4 par la version souhaitée
```

Puis rebuild :
```bash
docker-compose build --no-cache backend-php
```

### Ajouter des extensions PHP

**Dans `docker/php/Dockerfile.dev`, après les autres extensions :**
```dockerfile
RUN docker-php-ext-install -j$(nproc) gd bcmath soap
```

Puis rebuild :
```bash
docker-compose build --no-cache backend-php
```

### Retirer pgAdmin (si tu ne veux pas l'utiliser)

Si tu préfères utiliser un client local ou pas de visualiseur du tout :

**Dans `docker-compose.yml`, supprime ou commente :**
```yaml
# pgadmin:
#   image: dpage/pgadmin4:latest
#   ...

# Et dans volumes:
# pgadmin_data:
#   name: newproject_pgadmin_data
```

Puis :
```bash
docker-compose down
docker-compose up -d
```

---

## 🔒 Sécurité

### Pour la production

Avant de déployer en production :

1. **Changer `APP_SECRET`** avec une valeur forte et unique
2. **Changer les credentials PostgreSQL**
3. **Passer `APP_ENV=prod`**
4. **Désactiver Xdebug** (utiliser `ARG INSTALL_XDEBUG=false` dans le build)
5. **Utiliser HTTPS** avec des certificats valides
6. **Renforcer les headers de sécurité** dans Nginx
7. **Configurer les CORS** si API
8. **Optimiser le cache OPcache**

### Variables sensibles

⚠️ **Ne commite JAMAIS ton fichier `.env` !**

Le fichier `.gitignore` est configuré pour ignorer `.env`, vérifie avant chaque commit :
```bash
git status
```

---

## 📚 Ressources utiles

- [Documentation Symfony](https://symfony.com/doc/current/index.html)
- [Documentation Docker](https://docs.docker.com/)
- [Documentation PostgreSQL](https://www.postgresql.org/docs/)
- [Documentation Nginx](https://nginx.org/en/docs/)
- [Xdebug Documentation](https://xdebug.org/docs/)
- [Symfony CLI Documentation](https://symfony.com/download)

---

## 🤝 Contribution

Ce template est privé et destiné à un usage personnel/interne.

Si tu veux le partager avec ton équipe :
1. Assure-toi que tous les secrets sont externalisés dans `.env`
2. Documente les spécificités de ton setup
3. Teste l'installation sur une machine vierge

---

## 📝 Changelog

### Version 1.0 (2025-11-24)
- ✨ Configuration initiale
- ✨ Docker Compose avec PHP 8.4, Nginx, PostgreSQL 18
- ✨ pgAdmin 4 intégré (interface web pour PostgreSQL)
- ✨ Makefile avec 70+ raccourcis pratiques
- ✨ Xdebug configuré
- ✨ Symfony CLI intégré
- ✨ Health checks sur tous les services
- ✨ Documentation complète avec commandes "locales"

---

## 📄 License

Projet privé - Tous droits réservés

---

## 🎉 Bon développement !

Si tu rencontres des problèmes ou as des suggestions d'amélioration, n'hésite pas !

**Créé avec ❤️ pour accélérer le développement Symfony avec Docker**
