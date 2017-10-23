clean:
	python manage.py flush ;\

migrate:
	python manage.py makemigrations;\
	sleep 1;\
	python manage.py migrate

rebuild: 
	rm db.sqlite3;\
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete ;\
	find . -path "*/migrations/*.pyc" -delete;\
	make migrate;\
	sleep 3;\
	python manage.py shell -c "import populate_db; populate_db.populate()"

.PHONY: clean migrate rebuild
