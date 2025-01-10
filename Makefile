infra:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	up -d --build

auth: auth_dir
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f auth/app/docker-compose.yml -f auth/app/docker-compose.override.yml \
	up -d --build

auth_dir:
	@:

purchase: purchase_dir
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f purchase/docker-compose.yml -f purchase/docker-compose.override.yml \
	up -d --build

purchase_dir:
	@:

promocodes: promocodes_dir
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f promocodes/docker-compose.yml -f promocodes/docker-compose.override.yml \
	up -d --build

promocodes_dir:
	@:

admin: admin_dir
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f admin/app/docker-compose.yml -f admin/app/docker-compose.override.yml \
	up -d --build

admin_dir:
	@:


front: front_dir
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f front/docker-compose.yml -f front/docker-compose.override.yml \
	up -d --build

front_dir:
	@:

adminka: adminka_dir
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f adminka/docker-compose.yml -f adminka/docker-compose.override.yml \
	up -d --build

adminka_dir:
	@:

test_promocodes:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f promocodes/tests/functional/docker-compose.yml stop db_test_promocodes
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f promocodes/tests/functional/docker-compose.yml rm db_test_promocodes -f
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f promocodes/tests/functional/docker-compose.yml up db_test_promocodes -d
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f promocodes/tests/functional/docker-compose.yml stop test_promocodes test_promocodes_app
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f promocodes/tests/functional/docker-compose.yml rm --force test_promocodes test_promocodes_app
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f promocodes/tests/functional/docker-compose.yml up --build -d
	docker logs graduate_work-test_promocodes-1 -f


all:
	$(MAKE) infra
	$(MAKE) auth
	$(MAKE) purchase
	$(MAKE) promocodes
	$(MAKE) adminka
	$(MAKE) front

remove:
	docker-compose -f docker-compose.yml -f auth/app/docker-compose.yml \
	-f auth/app/docker-compose.yml -f purchase/docker-compose.yml \
	-f promocodes/docker-compose.yml -f adminka/docker-compose.yml \
	-f front/docker-compose.yml down
	docker volume rm graduate_work_pg_data || true
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f promocodes/tests/functional/docker-compose.yml stop test_promocodes test_promocodes_app
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f promocodes/tests/functional/docker-compose.yml rm --force test_promocodes test_promocodes_app
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f promocodes/tests/functional/docker-compose.yml stop db_test_promocodes
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f promocodes/tests/functional/docker-compose.yml rm db_test_promocodes -f