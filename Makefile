VENV=venv-workstation
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
LINT=$(VENV)/bin/flake8
TEST=$(VENV)/bin/nosetests
REQ_MIN=requirements-min.txt
REQ_DEV=requirements-devel.txt
REQ_TST=requirements-test.txt

.PHONY: test py-pkg-minimum py-pkg-developer py-pkg-testing


all:
	@echo Hello this is the developer\'s makefile


$(VENV): 
	virtualenv $(VENV)
	$(PIP) install --upgrade pip

py-pkg-minimum: $(VENV) $(REQ_MIN)
	$(PIP) install -r requirements-test.txt

py-pkg-developer: $(DEV) $(REQ_DEV)
	$(PIP) install -r $(REQ_DEV)

py-pkg-testing: $(DEV) $(REQ_TST)
	$(PIP) install -r $(REQ_TST)

lint:
	$(LINT) ts7250v2/ test/

test:
	$(TEST) test/


