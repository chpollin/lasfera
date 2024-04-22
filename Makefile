preview : 
	poetry run python manage.py runserver

mm :
	poetry run python manage.py makemigrations

migrate :
	poetry run python manage.py migrate

# data loading
loadlibraries :
	poetry run python manage.py loaddata libraries

# get data structure
dbml :
	poetry run python manage.py dbml accounts manuscript map > lasfera.dbml

# deploy dbml to dbdocs.io
deploydbml : dbml
	dbdocs build lasfera.dbml

