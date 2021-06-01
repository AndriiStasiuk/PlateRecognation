.PHONY: setup
setup:
	sudo apt-get -y install python3-dev python3-pip libpq-dev supervisor shellcheck
	make setup_venv

.PHONY: setup_mac
setup_mac:
	brew update && brew install git python pkg-config shellcheck
	make setup_venv

.PHONY: setup_venv
setup_venv:
	sudo pip3 install --upgrade pip pip-tools virtualenv
	virtualenv -p python3.8 --always-copy --system-site-packages venv
	venv/bin/pip install -e .'[dev,test]'

.PHONY: compile-versions
compile-versions:
	pip-compile -v --rebuild requirements/requirements.in
	pip-compile -v --rebuild requirements/test_requirements.in
