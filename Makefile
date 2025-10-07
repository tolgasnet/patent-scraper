run-cli:
	poetry run python ingest/cli.py scrape

run-ui:
	PYTHONPATH=. poetry run python -m streamlit run visualise/app.py
