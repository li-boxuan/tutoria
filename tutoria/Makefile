clean:
	python3 manage.py flush ;\
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete ;\
	find . -path "*/migrations/*.pyc" -delete;\

migrate:
	python3 manage.py makemigrations;\
	sleep 1;\
	python3 manage.py migrate

rebuild: 
	rm db.sqlite3;\
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete ;\
	find . -path "*/migrations/*.pyc" -delete;\
	make migrate;\
	sleep 3;\
	python3 manage.py shell -c "import populate_db; populate_db.populate()"

rebuild_empty:
	rm db.sqlite3;\
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete ;\
	find . -path "*/migrations/*.pyc" -delete;\
	make migrate;\
	sleep 3;\
	python3 manage.py shell -c "import populate_db; populate_db.populate_staff()"


PHONY: clean migrate rebuild
