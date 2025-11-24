# Makefile pour Symfony Docker Template
# Usage: make [command]

.PHONY: help
.DEFAULT_GOAL := help

# Variables
DOCKER_COMPOSE = docker-compose
PHP_CONTAINER = backend-php
DB_CONTAINER = backend-postgres
NGINX_CONTAINER = backend-nginx
PGADMIN_CONTAINER = pgadmin

## —— 🐳 Docker ————————————————————————————————————————————————————————————
up: ## Demarrer tous les containers
	$(DOCKER_COMPOSE) up -d

down: ## Arrêter tous les containers
	$(DOCKER_COMPOSE) down

restart: ## Redemarrer tous les containers
	$(DOCKER_COMPOSE) restart

build: ## Construire/reconstruire les images
	$(DOCKER_COMPOSE) build

rebuild: ## Reconstruire complètement (sans cache)
	$(DOCKER_COMPOSE) build --no-cache

ps: ## Voir l'etat des containers
	$(DOCKER_COMPOSE) ps

logs: ## Voir tous les logs (Ctrl+C pour quitter)
	$(DOCKER_COMPOSE) logs -f

logs-php: ## Voir les logs PHP
	$(DOCKER_COMPOSE) logs -f $(PHP_CONTAINER)

logs-nginx: ## Voir les logs Nginx
	$(DOCKER_COMPOSE) logs -f $(NGINX_CONTAINER)

logs-db: ## Voir les logs PostgreSQL
	$(DOCKER_COMPOSE) logs -f $(DB_CONTAINER)

clean: ## Arrêter et supprimer containers + volumes + images
	$(DOCKER_COMPOSE) down -v --rmi all

stop: ## Arrêter les containers (alias de down)
	$(DOCKER_COMPOSE) down

## —— ==> Accès ——————————————————————————————————————————————————————————————
bash: ## Entrer dans le container PHP
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) bash

db-shell: ## Acceder au shell PostgreSQL
	$(DOCKER_COMPOSE) exec $(DB_CONTAINER) psql -U $$(grep POSTGRES_USER .env | cut -d '=' -f2) -d $$(grep POSTGRES_DB .env | cut -d '=' -f2)

pgadmin: ## Ouvrir pgAdmin dans le navigateur
	@echo "Ouverture de pgAdmin..."
	@open http://localhost:5050 || xdg-open http://localhost:5050 || start http://localhost:5050

app: ## Ouvrir l'application dans le navigateur
	@echo "Ouverture de l'application..."
	@open http://localhost:8080 || xdg-open http://localhost:8080 || start http://localhost:8080

## —— 🎵 Symfony ———————————————————————————————————————————————————————————
sf: ## Executer une commande Symfony (usage: make sf cmd="cache:clear")
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console $(cmd)

cache-clear: ## Vider le cache Symfony
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console cache:clear

cache-warmup: ## Prechauffer le cache
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console cache:warmup

routes: ## Voir toutes les routes
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console debug:router

controller: ## Creer un controller (usage: make controller name=Article)
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console make:controller $(name)

entity: ## Creer une entite (usage: make entity name=Article)
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console make:entity $(name)

crud: ## Creer un CRUD (usage: make crud name=Article)
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console make:crud $(name)

form: ## Creer un formulaire (usage: make form name=Article)
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console make:form $(name)

security: ## Verifier les vulnerabilites
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony security:check

## —— 📦 Composer ——————————————————————————————————————————————————————————
composer-install: ## Installer les dependances Composer
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) composer install

composer-update: ## Mettre à jour les dependances
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) composer update

composer-require: ## Installer un package (usage: make composer-require package=symfony/mailer)
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) composer require $(package)

composer-remove: ## Supprimer un package (usage: make composer-remove package=symfony/mailer)
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) composer remove $(package)

composer-dump: ## Regenerer l'autoload
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) composer dump-autoload

## —— ==> Base de donnees ——————————————————————————————————————————————————
db-create: ## Creer la base de donnees
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console doctrine:database:create --if-not-exists

db-drop: ## Supprimer la base de donnees
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console doctrine:database:drop --force --if-exists

db-migrate: ## Executer les migrations
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console doctrine:migrations:migrate --no-interaction

db-migration: ## Creer une nouvelle migration
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console make:migration

db-diff: ## Generer une migration automatiquement
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console doctrine:migrations:diff

db-validate: ## Valider le schema de base de donnees
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console doctrine:schema:validate

db-fixtures: ## Charger les fixtures
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) symfony console doctrine:fixtures:load --no-interaction

db-reset: db-drop db-create db-migrate db-fixtures ## Reinitialiser complètement la base de donnees

db-backup: ## Creer un backup de la base
	@mkdir -p backups
	$(DOCKER_COMPOSE) exec $(DB_CONTAINER) pg_dump -U $$(grep POSTGRES_USER .env | cut -d '=' -f2) $$(grep POSTGRES_DB .env | cut -d '=' -f2) > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "==> Backup cree dans backups/"

db-restore: ## Restaurer un backup (usage: make db-restore file=backups/backup.sql)
	$(DOCKER_COMPOSE) exec -T $(DB_CONTAINER) psql -U $$(grep POSTGRES_USER .env | cut -d '=' -f2) $$(grep POSTGRES_DB .env | cut -d '=' -f2) < $(file)

## —— 🧪 Tests ————————————————————————————————————————————————————————————
test: ## Executer les tests PHPUnit
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) php bin/phpunit

test-coverage: ## Tests avec couverture de code
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) php bin/phpunit --coverage-html var/coverage

## —— ==> Installation ——————————————————————————————————————————————————————
init-symfony-webapp: ## Installer Symfony webapp
	@echo "📦 Installation de Symfony webapp..."
	$(DOCKER_COMPOSE) run --rm $(PHP_CONTAINER) bash -c "composer create-project symfony/skeleton:7.* temp && cd temp && composer require webapp && cd .. && cp -r temp/* . && cp temp/.env . 2>/dev/null || true && rm -rf temp"
	@echo "==> Symfony webapp installe !"
	@echo "==> Correction des permissions..."
	$(MAKE) fix-perms

init-symfony-skeleton: ## Installer Symfony skeleton
	@echo "📦 Installation de Symfony skeleton..."
	$(DOCKER_COMPOSE) run --rm $(PHP_CONTAINER) bash -c "composer create-project symfony/skeleton:7.* temp && cp -r temp/* . && cp temp/.env . 2>/dev/null || true && rm -rf temp"
	@echo "==> Symfony skeleton installe !"
	@echo "==> Correction des permissions..."
	$(MAKE) fix-perms

setup: build up composer-install db-create db-migrate fix-perms ## Installation complète du projet (après avoir installe Symfony)
	@echo ""
	@echo "==> Installation terminee !"
	@echo "==> N'oublie pas de configurer .env"
	@echo "==> Application: http://localhost:8080"
	@echo "==> pgAdmin: http://localhost:5050"

first-install-webapp: build init-symfony-webapp up composer-install db-create fix-perms ## Première installation webapp (clone + Symfony)
	@echo ""
	@echo "==> Symfony webapp installe et containers demarres !"
	@echo "==> edite .env avec tes valeurs"
	@echo "==> Ensuite lance: make db-migrate"
	@echo "==> Application: http://localhost:8080"
	@echo "==> pgAdmin: http://localhost:5050"

first-install-skeleton: build init-symfony-skeleton up composer-install fix-perms ## Première installation skeleton (clone + Symfony)
	@echo ""
	@echo "==> Symfony skeleton installe et containers demarres !"
	@echo "==> edite .env avec tes valeurs"
	@echo "==> Ensuite lance: make db-migrate"
	@echo "==> Application: http://localhost:8080"
	@echo "==> pgAdmin: http://localhost:5050"

## —— ==> Utilitaires ———————————————————————————————————————————————————————
fix-perms: ## Corriger les permissions des fichiers
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) chown -R www-data:www-data var/
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) chmod -R 777 var/

clear-cache: ## Supprimer tout le cache (fichiers)
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) rm -rf var/cache/*

clear-logs: ## Supprimer tous les logs
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) rm -rf var/log/*

phpstan: ## Analyser le code avec PHPStan (si installe)
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) vendor/bin/phpstan analyse src

cs-fixer: ## Formater le code avec PHP-CS-Fixer (si installe)
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) vendor/bin/php-cs-fixer fix src

## —— 📊 Monitoring ————————————————————————————————————————————————————————
stats: ## Voir les stats des containers (CPU, RAM)
	docker stats

health: ## Verifier la sante de tous les services
	@echo "==> Verification des services..."
	@$(DOCKER_COMPOSE) ps
	@echo ""
	@echo "==> PostgreSQL:"
	@$(DOCKER_COMPOSE) exec $(DB_CONTAINER) pg_isready -U $$(grep POSTGRES_USER .env | cut -d '=' -f2) && echo "==> OK" || echo "❌ Erreur"
	@echo ""
	@echo "==> PHP-FPM:"
	@$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) php -v | head -n 1
	@echo ""
	@echo "==> Nginx:"
	@$(DOCKER_COMPOSE) exec $(NGINX_CONTAINER) nginx -v 2>&1

## —— 📚 Aide —————————————————————————————————————————————————————————————
help: ## Afficher cette aide
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'
