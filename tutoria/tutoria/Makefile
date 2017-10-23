clean:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete ;\
	find . -path "*/migrations/*.pyc" -delete
	python manage.py flush ;\


migrate:
	python manage.py makemigration ;\
	python manage.py migrate


.PHONY: clean migrate
