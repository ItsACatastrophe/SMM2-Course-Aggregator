install:
	cat .python-version | pyenv install --upgrade
	python -m pip install -r requirements.txt

collect-courses:
	python main.py -o 12

get-course:
	python main_db.py

test-unit:
	python -m unittest

test-unit-specific:
	python -m unittest tests.test_utils.TestUtils.test_format_course_code