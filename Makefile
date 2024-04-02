preview : 
	poetry run python manage.py runserver

mm :
	poetry run python manage.py makemigrations

migrate :
	poetry run python manage.py migrate

# data loading
loadlibraries :
	poetry run python manage.py loaddata libraries