import datetime as dt

def test_cutoff_math():
    now = dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=7)
    assert cutoff < now
