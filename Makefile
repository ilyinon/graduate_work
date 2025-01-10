infra:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	up -d --build

auth: auth_dir
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f auth/app/docker-compose.yml -f auth/app/docker-compose.override.yml \
	up -d --build
	docker logs -f graduate_work-auth-1

auth_dir:
	@:

purchase: purchase_dir
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f purchase/docker-compose.yml -f purchase/docker-compose.override.yml \
	up -d --build
	docker logs -f graduate_work-purchase-1

purchase_dir:
	@:

promocodes: promocodes_dir
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f promocodes/docker-compose.yml -f promocodes/docker-compose.override.yml \
	up -d --build
	docker logs -f graduate_work-promocodes-1

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


all:
	$(MAKE) infra
	$(MAKE) auth
	$(MAKE) purchase
	$(MAKE) adminka
	$(MAKE) front

remove:
	docker-compose -f docker-compose.yml -f auth/app/docker-compose.yml \
	-f auth/app/docker-compose.yml -f purchase/docker-compose.yml \
	-f promocodes/docker-compose.yml -f adminka/docker-compose.yml \
	-f front/docker-compose.yml down
	docker volume rm graduate_work_pg_data || true

