import pytest
from ec2_auto_tagging.app import parse_tags


def test_parse_tags_ok():
    tags = parse_tags(["Environment=dev", "Owner=david"])
    assert tags[0].key == "Environment"
    assert tags[0].value == "dev"


def test_parse_tags_bad():
    with pytest.raises(ValueError):
        parse_tags(["NoEquals"])
