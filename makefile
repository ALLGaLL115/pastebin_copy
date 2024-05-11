restart:
	docker rm dd
	docker rmi fsi
	docker build . -t fsi
	docker run -d -p 1000:8000 --name dd fsi

stop:

	docker container rm $(docker ps -aq)
	# docker image rmi $(docker images -aq)	

comp:
	docker-compose up --build



preparate_test:
	cd src && uvicorn main:app --reload & celery -A tasks.verification_task:celery worker --loglevel=INFO --pool=solo

