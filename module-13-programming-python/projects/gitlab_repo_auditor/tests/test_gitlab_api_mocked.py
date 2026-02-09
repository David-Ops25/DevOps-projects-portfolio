from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from gitlab_repo_auditor import app


class FakeResp:
    def __init__(self, status_code: int, payload: Any):
        self.status_code = status_code
        self._payload = payload
        self.text = str(payload)

    def json(self) -> Any:
        return self._payload


def fake_get_factory(routes: dict[tuple[str, tuple[tuple[str, Any], ...] | None], Any]):
    """Small request router to keep tests deterministic and offline."""

    def _fake_get(url: str, params=None, timeout=30):
        key_params = None if params is None else tuple(sorted(params.items()))
        key = (url, key_params)
        if key not in routes:
            raise AssertionError(f"Unexpected request: url={url} params={params}")
        return FakeResp(200, routes[key])

    return _fake_get


def test_resolve_user_id_success():
    routes = {(f"{app.GITLAB_API}/users", (("username", "gitlab"),)): [{"id": 123}]}
    with patch("requests.get", new=fake_get_factory(routes)):
        assert app.resolve_user_id("gitlab") == 123


def test_resolve_user_id_not_found():
    routes = {(f"{app.GITLAB_API}/users", (("username", "nope"),)): []}
    with patch("requests.get", new=fake_get_factory(routes)):
        with pytest.raises(SystemExit):
            app.resolve_user_id("nope")


def test_list_projects_paginates_until_empty():
    routes = {
        (
            f"{app.GITLAB_API}/users/123/projects",
            (("order_by", "last_activity_at"), ("page", 1), ("per_page", 2), ("simple", True)),
        ): [{"name": "a"}, {"name": "b"}],
        (
            f"{app.GITLAB_API}/users/123/projects",
            (("order_by", "last_activity_at"), ("page", 2), ("per_page", 2), ("simple", True)),
        ): [{"name": "c"}],
        (
            f"{app.GITLAB_API}/users/123/projects",
            (("order_by", "last_activity_at"), ("page", 3), ("per_page", 2), ("simple", True)),
        ): [],
    }
    with patch("requests.get", new=fake_get_factory(routes)):
        projects = app.list_projects(123, per_page=2)
        assert [p["name"] for p in projects] == ["a", "b", "c"]


def test_has_readme_tries_default_branch_first_then_fallback():
    encoded = "my%2Fproj"
    routes = {
        (f"{app.GITLAB_API}/projects/{encoded}/repository/tree", (("per_page", 100), ("ref", "trunk"))): [{"name": "src"}],
        (f"{app.GITLAB_API}/projects/{encoded}/repository/tree", (("per_page", 100), ("ref", "main"))): [{"name": "README.md"}],
    }
    with patch("requests.get", new=fake_get_factory(routes)):
        assert app.has_readme("my/proj", default_branch="trunk") is True


def test_audit_summary_counts_readme():
    projects = [
        {
            "name": "p1",
            "path_with_namespace": "a/b",
            "web_url": "x",
            "last_activity_at": "2026-01-01T00:00:00Z",
            "default_branch": "main",
        },
        {
            "name": "p2",
            "path_with_namespace": "c/d",
            "web_url": "y",
            "last_activity_at": "2026-01-01T00:00:00Z",
            "default_branch": "main",
        },
    ]
    with patch.object(app, "has_readme", side_effect=[True, False]):
        data = app.audit(projects)
        assert data["summary"]["total_projects"] == 2
        assert data["summary"]["readme_present"] == 1
        assert data["summary"]["readme_missing"] == 1
