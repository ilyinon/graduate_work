infra:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d --build

auth: auth_dir
	$(MAKE) infra
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f auth/app/docker-compose.yml -f auth/app/docker-compose.override.yml \
	up -d --build
	docker logs -f graduate_work-auth-1

auth_dir:
	@:

search: search_dir
	$(MAKE) infra
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f search/app/docker-compose.yml -f search/app/docker-compose.override.yml \
	up -d --build
	docker logs -f graduate_work-search-1

search_dir:
	@:

admin: admin_dir
	$(MAKE) infra
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f admin/app/docker-compose.yml -f admin/app/docker-compose.override.yml \
	up -d --build

admin_dir:
	@:

admin_init:
	. .env
	export PGPASSWORD=${PG_PASSWORD}
	psql -h localhost -U ${PG_USER} < admin/init_database.sql
	$(MAKE) admin

admin_loaddata:
	. .env
	export PGPASSWORD=${PG_PASSWORD}
	psql -h localhost -U ${PG_USER} content < admin/load_data.sql

test_auth:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f auth/tests/functional/docker-compose.yml stop db_test_auth redis_test_auth
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f auth/tests/functional/docker-compose.yml rm db_test_auth redis_test_auth -f
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f auth/tests/functional/docker-compose.yml up db_test_auth redis_test_auth -d
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f auth/tests/functional/docker-compose.yml stop test_auth
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f auth/tests/functional/docker-compose.yml rm --force test_auth
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f auth/tests/functional/docker-compose.yml up --build -d
	docker logs graduate_work-test_auth-1 -f

test_search:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f search/tests/functional/docker-compose.yml stop test_search
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f search/tests/functional/docker-compose.yml rm --force test_search
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f search/tests/functional/docker-compose.yml up -d --build
	docker logs graduate_work-test_search-1 -f



all:
	$(MAKE) infra
	$(MAKE) auth
	$(MAKE) search
	$(MAKE) admin


remove:
	docker-compose -f docker-compose.yml stop db
	docker-compose -f docker-compose.yml rm db -f
	docker volume rm graduate_work_pg_data
	docker stop graduate_work-admin-1
	docker rm graduate_work-admin-1
stop:
	docker-compose -f docker-compose.yml -f auth/app/docker-compose.yml \
	-f search/app/docker-compose.yml -f admin/app/docker-compose.yml down

status:
	docker-compose ps
