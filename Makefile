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
up: ## Démarrer tous les containers
	$(DOCKER_COMPOSE) up -d

down: ## Arrêter tous les containers
	$(DOCKER_COMPOSE) down

restart: ## Redémarrer tous les containers
	$(DOCKER_COMPOSE) restart

build: ## Construire/reconstruire les images
	$(DOCKER_COMPOSE) build

rebuild: ## Reconstruire complètement (sans cache)
	$(DOCKER_COMPOSE) build --no-cache

ps: ## Voir l'état des containers
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

## —— 🔧 Accès ——————————————————————————————————————————————————————————————
bash: ## Entrer dans le container PHP
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) bash

db-shell: ## Accéder au shell PostgreSQL
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

## —— 🗄️ Base de donnees ——————————————————————————————————————————————————
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

## —— 🚀 Installation ——————————————————————————————————————————————————————
# Fonction pour afficher une barre de progression
define show_progress
	@printf "\033[1;36m"
	@printf "["
	@for i in $$(seq 1 $(1)); do printf "="; done
	@for i in $$(seq 1 $$((50-$(1)))); do printf " "; done
	@printf "]\033[0m "
	@printf "\033[1;32m%3d%%\033[0m " $$(($(1)*2))
	@printf "$(2)\n"
endef

setup: ## Installation complete du projet (Symfony deja installe)
	@echo ""
	@printf "\033[1;34m"
	@echo "=========================================="
	@echo "  Installation du projet Symfony"
	@echo "=========================================="
	@printf "\033[0m"
	@echo ""
	$(call show_progress,10,[1/5] Building Docker images...)
	@$(MAKE) build -s
	$(call show_progress,20,[2/5] Starting containers...)
	@$(MAKE) up -s
	$(call show_progress,30,[3/5] Fixing permissions...)
	@$(MAKE) fix-perms -s
	$(call show_progress,40,[4/5] Installing dependencies...)
	@$(MAKE) composer-install -s
	$(call show_progress,50,[5/5] Setup complete!)
	@echo ""
	@printf "\033[1;32m"
	@echo "=========================================="
	@echo "  Installation terminee !"
	@echo "=========================================="
	@printf "\033[0m"
	@echo ""
	@printf "\033[1;33m"
	@echo "==> Application: http://localhost:8080"
	@echo "==> pgAdmin: http://localhost:5050"
	@printf "\033[0m"
	@echo ""
	@echo "==> Pour ajouter des fonctionnalites :"
	@printf "\033[1;35m"
	@echo "    make upgrade-webapp    # Site web (Twig, Formulaires, etc.)"
	@echo "    make upgrade-api       # API REST (API Platform)"
	@echo "    make db-create         # Creer la base de donnees"
	@printf "\033[0m"
	@echo ""

upgrade-webapp: ## Passer de skeleton a webapp (installe Doctrine, Twig, etc.)
	@echo "==> Installation du pack webapp..."
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) composer require webapp
	@echo "==> Pack webapp installe !"
	@echo "==> Tu peux maintenant creer la DB : make db-create"

upgrade-api: ## Passer de skeleton a API (installe API Platform)
	@echo "==> Installation d'API Platform..."
	$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) composer require api
	@echo "==> API Platform installe !"
	@echo "==> Documentation API disponible a : http://localhost:8080/api"
	@echo "==> Tu peux maintenant creer la DB : make db-create"

## —— 🔧 Utilitaires ———————————————————————————————————————————————————————
fix-perms: ## Corriger les permissions des fichiers
	@echo "==> Correction des permissions..."
	@sudo chown -R $(USER):$(USER) . || chown -R $(USER):$(USER) . 2>/dev/null || true
	@if docker-compose ps | grep -q "backend-php.*Up"; then \
		if [ ! -d "var" ]; then \
			echo "==> Creation du dossier var/..."; \
			mkdir -p var/cache var/log; \
		fi; \
		$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) chown -R www-data:www-data var/ 2>/dev/null || true; \
		$(DOCKER_COMPOSE) exec $(PHP_CONTAINER) chmod -R 775 var/ 2>/dev/null || true; \
	else \
		echo "==> ATTENTION: Containers non demarres. Lance 'make up' puis relance 'make fix-perms'"; \
	fi

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
