import pandas as pd

from visualise.cpc_filters import filter_by_title


def test_filter_by_title_returns_matching_rows():
    df = pd.DataFrame(
        {
            "title": ["Alpha Discovery", "Beta Insight", "Gamma"],
            "other": [1, 2, 3],
        }
    )

    filtered = filter_by_title(df, "beta")

    assert len(filtered) == 1
    assert filtered.iloc[0]["title"] == "Beta Insight"


def test_filter_by_title_handles_missing_column():
    df = pd.DataFrame({"name": ["Alpha", "Beta"]})

    filtered = filter_by_title(df, "alpha")

    assert filtered is df


def test_filter_by_title_empty_query_returns_original():
    df = pd.DataFrame({"title": ["One", "Two"]})

    filtered = filter_by_title(df, "")

    assert filtered is df
