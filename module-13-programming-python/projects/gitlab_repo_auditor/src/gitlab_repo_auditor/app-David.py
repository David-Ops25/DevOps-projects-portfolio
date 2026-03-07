from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

GITLAB_API = "https://gitlab.com/api/v4"


@dataclass(frozen=True)
class Args:
    username: str
    output_dir: Path
    per_page: int


def parse_args(argv: list[str] | None = None) -> Args:
    p = argparse.ArgumentParser(prog="gitlab-audit", description="Audit a GitLab user's public repositories.")
    p.add_argument("--username", required=True, help="GitLab username (public profile).")
    p.add_argument("--output-dir", default="out", help="Directory to write outputs into.")
    p.add_argument("--per-page", type=int, default=50, help="Results per page (max 100).")
    ns = p.parse_args(argv)
    return Args(username=str(ns.username), output_dir=Path(ns.output_dir), per_page=int(ns.per_page))


def _get_json(url: str, params: dict[str, Any] | None = None) -> Any:
    r = requests.get(url, params=params, timeout=30)
    if r.status_code != 200:
        raise SystemExit(f"GitLab API error {r.status_code}: {r.text[:200]}")
    return r.json()


def resolve_user_id(username: str) -> int:
    data = _get_json(f"{GITLAB_API}/users", params={"username": username})
    if not data:
        raise SystemExit(f"User not found: {username}")
    return int(data[0]["id"])


def list_projects(user_id: int, per_page: int = 50) -> list[dict[str, Any]]:
    projects: list[dict[str, Any]] = []
    page = 1
    while True:
        batch = _get_json(
            f"{GITLAB_API}/users/{user_id}/projects",
            params={
                "per_page": min(max(per_page, 1), 100),
                "page": page,
                "simple": True,
                "order_by": "last_activity_at",
            },
        )
        if not batch:
            break
        projects.extend(batch)
        page += 1
    return projects


def _repo_tree_names(project_path_with_namespace: str, ref: str) -> set[str]:
    encoded = project_path_with_namespace.replace("/", "%2F")
    tree = _get_json(
        f"{GITLAB_API}/projects/{encoded}/repository/tree",
        params={"per_page": 100, "ref": ref},
    )
    return {item.get("name", "").lower() for item in tree}


def has_readme(project_path_with_namespace: str, default_branch: str | None = None) -> bool:
    candidates: list[str] = []
    if default_branch:
        candidates.append(default_branch)
    for b in ("main", "master"):
        if b not in candidates:
            candidates.append(b)

    for ref in candidates:
        try:
            names = _repo_tree_names(project_path_with_namespace, ref=ref)
        except Exception:
            continue
        if any(n in names for n in {"readme.md", "readme", "readme.txt"}):
            return True

    return False


def parse_dt(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


def audit(projects: list[dict[str, Any]]) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    results = []
    readme_ok = 0

    for p in projects:
        path_ns = p.get("path_with_namespace", "")
        last_activity = parse_dt(p["last_activity_at"]) if p.get("last_activity_at") else None
        age_days = (now - last_activity).days if last_activity else None

        default_branch = p.get("default_branch") or None

        readme = False
        try:
            readme = has_readme(path_ns, default_branch=default_branch) if path_ns else False
        except Exception:
            readme = False

        if readme:
            readme_ok += 1

        results.append(
            {
                "name": p.get("name"),
                "path_with_namespace": path_ns,
                "web_url": p.get("web_url"),
                "description": p.get("description") or "",
                "visibility": p.get("visibility"),
                "star_count": p.get("star_count", 0),
                "forks_count": p.get("forks_count", 0),
                "default_branch": default_branch,
                "last_activity_at": p.get("last_activity_at"),
                "inactive_days": age_days,
                "has_readme": readme,
            }
        )

    summary = {
        "total_projects": len(results),
        "readme_present": readme_ok,
        "readme_missing": len(results) - readme_ok,
    }
    return {"summary": summary, "projects": results}


def to_markdown(data: dict[str, Any], username: str) -> str:
    s = data["summary"]
    lines = [
        f"# GitLab Repo Audit — {username}",
        "",
        f"- Total projects: **{s['total_projects']}**",
        f"- README present: **{s['readme_present']}**",
        f"- README missing: **{s['readme_missing']}**",
        "",
        "## Projects",
        "",
        "| Repo | Stars | Forks | Default branch | README | Last activity | Inactive days |",
        "|---|---:|---:|---|:---:|---|---:|",
    ]
    for p in data["projects"]:
        repo = f"[{p['path_with_namespace']}]({p['web_url']})" if p.get("web_url") else p.get("path_with_namespace", "")
        readme = "✅" if p.get("has_readme") else "❌"
        last = p.get("last_activity_at") or ""
        inactive = "" if p.get("inactive_days") is None else str(p["inactive_days"])
        branch = p.get("default_branch") or ""
        lines.append(
            f"| {repo} | {p.get('star_count',0)} | {p.get('forks_count',0)} | {branch} | {readme} | {last} | {inactive} |"
        )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    user_id = resolve_user_id(args.username)
    projects = list_projects(user_id, per_page=args.per_page)
    data = audit(projects)

    (args.output_dir / "audit.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    (args.output_dir / "audit.md").write_text(to_markdown(data, args.username), encoding="utf-8")

    print(f"Wrote: {args.output_dir / 'audit.md'}")
    print(f"Wrote: {args.output_dir / 'audit.json'}")


if __name__ == "__main__":
    main()
