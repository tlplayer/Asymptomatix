app:
	docker-compose down
	docker system prune -f
	sudo docker-compose up -d -V --build
	docker-compose exec web flask db upgrade

reset_docker_network:
	docker-machine rm default && docker-machine create -d virtualbox default && eval $(docker-machine env default)

create_ecr_repo:

	aws ecr create-repository --repository-name asymptomatix
	aws ecr get-login --region us-east-1 --no-include-email;

upload:

	docker tag asymptomatix:latest <account-ID>.dkr.ecr.us-east-1.amazonaws.com/
	docker push <account-ID>.dkr.ecr.us-east-1.amazonaws.com/asymptomatix

db_upgrade:

	pip3 install flask-migrate --upgrade
	flask db stamp head
	flask db migrate -m "Next DB iteration / migration."
	flask db upgrade
