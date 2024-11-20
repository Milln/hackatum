.PHONY: install clean

install: requirements.txt
	pip -q install -r requirements.txt

clean:
	$(PIP) freeze | grep -v '^\-e' | cut -d = -f 1 | xargs $(PIP) uninstall -y
