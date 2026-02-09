import pandas as pd

from release_notes_generator.app import normalize, to_markdown


def test_normalize_requires_description():
    df = pd.DataFrame({"type": ["Added"]})
    try:
        normalize(df)
        assert False, "Expected SystemExit"
    except SystemExit:
        assert True


def test_markdown_sections_created():
    df = pd.DataFrame(
        {
            "type": ["Added", "Fixed"],
            "description": ["Add x", "Fix y"],
            "ticket": ["A-1", ""],
            "owner": ["", "Sam"],
        }
    )
    clean = normalize(df)
    md = to_markdown(clean, "1.0.0")
    assert "## Added" in md
    assert "## Fixed" in md
    assert "Release Notes — 1.0.0" in md
