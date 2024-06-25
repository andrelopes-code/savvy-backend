.PHONY: run test

run:
	@fastapi dev --reload

test:
	@SAVVY_DATABASE_NAME=savvy_test pytest -svx

cov:
	@SAVVY_DATABASE_NAME=savvy_test pytest --cov && coverage html
