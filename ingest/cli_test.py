from typer.testing import CliRunner
from cli import app

runner = CliRunner()

def test_scrape_command():
    result = runner.invoke(app, ["scrape"])
    assert result.exit_code == 0
    assert "Scraping patents..." in result.output

def test_math_works():
    assert 1 + 1 == 2
