.PHONY: clean virtualenv test docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete

virtualenv:
	poetry install
	@echo
	@echo "Poetry Setup Complete. Now run: poetry shell"
	@echo

test:
	python -m pytest \
		-v \
		--cov=wemulate \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/

docker: clean
	docker build -t wemulate:latest .

dist: clean
	rm -rf dist/*
	poetry build	

dist-upload:
	twine upload dist/*
