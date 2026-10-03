"""Tests for interview question templates and helper functions"""

from app.voice_agent.prompts import get_template, list_templates, InterviewTemplate, TEMPLATES


def test_get_template():
    general = get_template("general")
    assert isinstance(general, InterviewTemplate)
    assert general.name == "General Service"

    trades = get_template("trades")
    assert trades.name == "Skilled Trades"

    # Default fallback
    unknown = get_template("unknown_template")
    assert unknown.name == "General Service"


def test_list_templates():
    templates = list_templates()
    assert isinstance(templates, list)
    assert len(templates) > 0

    # Ensure all expected fields are present
    for t in templates:
        assert "name" in t
        assert "description" in t
        assert "industry" in t
        assert "duration_minutes" in t
        assert "question_count" in t

    # Ensure unique template names in listing
    names = [t["name"] for t in templates]
    assert len(names) == len(set(names))
