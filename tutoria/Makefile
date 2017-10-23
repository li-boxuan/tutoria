clean:
	python manage.py flush ;\

migrate:
	python manage.py makemigrations;\
	python manage.py migrate

rebuild: 
	rm db.sqlite3;\
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete ;\
	find . -path "*/migrations/*.pyc" -delete;\
	make migrate

.PHONY: clean migrate rebuild
