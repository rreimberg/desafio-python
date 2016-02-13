coverage:
	.venv/bin/nosetests --with-cover --cover-package=restfull_api

clean:
	find -iname *.pyc -delete
	find -iname *.pyo -delete

run:
	.venv/bin/python manage.py runserver

setup:
	if [ ! -d .venv ]; then virtualenv -p python2.7 .venv; fi

	.venv/bin/pip install -r requirements.txt

	.venv/bin/python manage.py create_db

test:
	.venv/bin/nosetests --rednose -s
