from website_monitor_recovery.monitor import parse_expected

def test_parse_expected():
    assert parse_expected("200,301") == {200, 301}
