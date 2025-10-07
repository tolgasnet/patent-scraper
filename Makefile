run-cli:
	poetry run python ingest/cli.py scrape

run-ui:
	poetry run streamlit run visualise/app.py