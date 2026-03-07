from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class CountdownArgs:
    goal: str
    deadline: datetime
    tz: str
    as_json: bool
    verbose: bool


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def parse_args(argv: list[str] | None = None) -> CountdownArgs:
    parser = argparse.ArgumentParser(prog="countdown", description="Countdown to a deadline.")
    parser.add_argument("--goal", required=True, help="What you're counting down to (e.g., 'AWS exam').")
    parser.add_argument(
        "--deadline",
        required=True,
        help="Deadline in ISO format, e.g. 2026-03-01T12:00:00Z or 2026-03-01T12:00:00+00:00",
    )
    parser.add_argument(
        "--timezone",
        default="UTC",
        help="Timezone for display (IANA name), e.g. 'UTC' or 'Europe/London'. Default: UTC",
    )
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON.")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging.")
    ns = parser.parse_args(argv)

    raw = ns.deadline.replace("Z", "+00:00")
    try:
        deadline = datetime.fromisoformat(raw)
    except ValueError as e:
        raise SystemExit(f"Invalid --deadline format: {ns.deadline}") from e

    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)

    # Validate timezone early
    try:
        ZoneInfo(ns.timezone)
    except Exception as e:
        raise SystemExit(f"Invalid --timezone: {ns.timezone}") from e

    return CountdownArgs(
        goal=ns.goal,
        deadline=deadline,
        tz=ns.timezone,
        as_json=bool(ns.json),
        verbose=bool(ns.verbose),
    )


def run(args: CountdownArgs) -> dict:
    tz = ZoneInfo(args.tz)
    now = datetime.now(timezone.utc)
    deadline_utc = args.deadline.astimezone(timezone.utc)
    delta = deadline_utc - now

    reached = delta.total_seconds() <= 0
    if reached:
        remaining = {"days": 0, "hours": 0, "minutes": 0, "seconds": 0}
    else:
        days = delta.days
        hours, rem = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        remaining = {"days": days, "hours": hours, "minutes": minutes, "seconds": seconds}

    result = {
        "goal": args.goal,
        "deadline_iso": args.deadline.isoformat(),
        "deadline_utc": deadline_utc.isoformat(),
        "deadline_display": args.deadline.astimezone(tz).isoformat(),
        "timezone": args.tz,
        "reached": reached,
        "remaining": remaining,
        "now_utc": now.isoformat(),
    }
    logging.debug("Computed result: %s", result)
    return result


def _format_text(res: dict) -> str:
    if res["reached"]:
        return f"✅ '{res['goal']}' reached! Deadline was {res['deadline_display']} ({res['timezone']})"

    r = res["remaining"]
    return (
        f"⏳ Goal: {res['goal']}\n"
        f"🗓️  Deadline ({res['timezone']}): {res['deadline_display']}\n"
        f"⏱️  Remaining: {r['days']}d {r['hours']}h {r['minutes']}m {r['seconds']}s"
    )


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    _configure_logging(args.verbose)

    res = run(args)

    if args.as_json:
        print(json.dumps(res, indent=2, sort_keys=True))
    else:
        print(_format_text(res))


if __name__ == "__main__":
    main()
