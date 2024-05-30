install:
	cat .python-version | pyenv install --upgrade
	python -m pip install -r requirements.txt

collect-courses:
	python collector/src/main.py -o 12

get-course:
	python collector/src/db.py

test-unit:
	python -m unittest discover -v -s tests

test-unit-specific:
	python -m unittest tests.test_utils.TestUtils.test_format_course_code