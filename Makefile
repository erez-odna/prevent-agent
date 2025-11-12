FORMATTER = black
SRC_DIR	= $(CURDIR)/src
TEST_DIR = $(CURDIR)/unit-test
NON_PROD_DIR = $(CURDIR)/non-prod

all: lint coverage

############ LINT ##################
lint:
	$(FORMATTER) --check $(SRC_DIR)
	$(FORMATTER) --check $(TEST_DIR)
	PYTHON_PATH=$(PWD):$(PYTHON_PATH)
	pylint $(SRC_DIR)
	pylint $(TEST_DIR)

lintfix:
	$(FORMATTER) $(SRC_DIR)
	$(FORMATTER) $(TEST_DIR)
	PYTHON_PATH=$(PWD):$(PYTHON_PATH)
	pylint $(SRC_DIR) $(TEST_DIR)

nplintfix:
	$(FORMATTER) $(NON_PROD_DIR)
	PYTHON_PATH=$(PWD):$(PYTHON_PATH)
	pylint $(NON_PROD_DIR)

############ TEST ##################
test:
	nose2 -v -s $(TEST_DIR) -t $(SRC_DIR)

coverage:
	nose2 -v -s $(TEST_DIR) -t $(SRC_DIR) --with-coverage --coverage src
	coverage html --omit=venv/*,unit-test/* --fail-under=90 || (echo 'Coverage Below 90%' && exit 1)

############ DOCS ##################
clean-docs:
	cd docs && $(MAKE) clean

docs: clean-docs
	$(MAKE) -C docs

############ CLEAN ##################
clean: clean-docs
	rm -rf $(CURDIR)/.coverage
	rm -rf $(CURDIR)/htmlcov



