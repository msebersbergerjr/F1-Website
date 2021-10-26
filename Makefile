clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

holy_land:
	pyenv virtualenv 3.9.7 F1
	pyenv virtualenv F1 && pyenv shell F1

follow:
	pyenv shell F1

deciples:
	python3 -m pip install -r requirements.txt

preach:
	python3 F1Website/manage.py runserver 

remove_env:
	pyenv uninstall F1