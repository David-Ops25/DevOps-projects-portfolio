from datetime import datetime, timedelta, timezone

from countdown_cli.app import CountdownArgs, run


def test_future_deadline_not_reached():
    args = CountdownArgs(
        goal="Test",
        deadline=datetime.now(timezone.utc) + timedelta(seconds=5),
        tz="UTC",
        as_json=False,
        verbose=False,
    )
    res = run(args)
    assert res["reached"] is False
    assert "remaining" in res


def test_past_deadline_reached():
    args = CountdownArgs(
        goal="Test",
        deadline=datetime.now(timezone.utc) - timedelta(seconds=5),
        tz="UTC",
        as_json=False,
        verbose=False,
    )
    res = run(args)
    assert res["reached"] is True
