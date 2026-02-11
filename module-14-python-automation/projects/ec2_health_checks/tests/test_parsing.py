from ec2_health_checks.app import print_status_rows


def test_smoke_function_exists():
    assert callable(print_status_rows)
