.PHONY: run

run:
	@fastapi dev --reload

test:
	@SAVVY_DATABASE_NAME=savvy_test pytest -s -x