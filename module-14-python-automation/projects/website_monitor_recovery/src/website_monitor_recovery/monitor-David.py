import argparse
import time
from typing import Set

import requests


def parse_expected(s: str) -> Set[int]:
    out: set[int] = set()
    for p in s.split(","):
        p = p.strip()
        if not p:
            continue
        out.add(int(p))
    return out or {200}


def check_once(url: str, timeout: int, expected_codes: set[int]) -> tuple[bool, str]:
    try:
        r = requests.get(url, timeout=timeout)
        ok = r.status_code in expected_codes
        msg = f"status={r.status_code} bytes={len(r.content)}"
        return ok, msg
    except requests.RequestException as e:
        return False, f"error={type(e).__name__}: {e}"


def main():
    ap = argparse.ArgumentParser(description="Website monitoring (HTTP check with retries).")
    ap.add_argument("--url", required=True)
    ap.add_argument("--timeout", type=int, default=3)
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--sleep", type=int, default=5)
    ap.add_argument("--expected", default="200,301,302")
    args = ap.parse_args()

    expected_codes = parse_expected(args.expected)
    print(
        f"Monitoring URL={args.url} expected={sorted(expected_codes)} timeout={args.timeout}s retries={args.retries}"
    )

    for attempt in range(1, args.retries + 1):
        ok, msg = check_once(args.url, args.timeout, expected_codes)
        state = "UP" if ok else "DOWN"
        print(f"{state} attempt={attempt}/{args.retries} {msg}")
        if ok:
            raise SystemExit(0)
        if attempt < args.retries:
            time.sleep(args.sleep)
    raise SystemExit(2)


if __name__ == "__main__":
    main()
