preview : 
	poetry run python manage.py runserver

mm :
	poetry run python manage.py makemigrations

migrate :
	poetry run python manage.py migrate

# data loading
loadlibraries :
	poetry run python manage.py loaddata libraries

dumpdata :
	poetry run python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > dumpdata.json

# get data structure
dbml :
	poetry run python manage.py dbml accounts manuscript map > lasfera.dbml

# deploy dbml to dbdocs.io
deploydbml : dbml
	dbdocs build lasfera.dbml

