init:
	python3 -m venv main_env \
	&& main_env/bin/pip install -r requirements.txt
run:
	./main_env/bin/python app.py