import argparse
import datetime as dt
import time
from typing import Iterable

import boto3


def session():
    # Uses default credential chain
    return boto3.session.Session()


def whoami() -> dict:
    return session().client("sts").get_caller_identity()


def iter_running_instance_ids(ec2) -> list[str]:
    resp = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )
    ids: list[str] = []
    for r in resp.get("Reservations", []):
        for i in r.get("Instances", []):
            ids.append(i["InstanceId"])
    return ids


def fetch_status(ec2, instance_ids: Iterable[str]) -> list[dict]:
    if not instance_ids:
        return []
    resp = ec2.describe_instance_status(
        InstanceIds=list(instance_ids),
        IncludeAllInstances=True,
    )
    return resp.get("InstanceStatuses", [])


def print_status_rows(ec2, ids: list[str]) -> bool:
    statuses = fetch_status(ec2, ids)
    unhealthy = False
    by_id = {s["InstanceId"]: s for s in statuses}
    for iid in ids:
        s = by_id.get(iid, {})
        state = s.get("InstanceState", {}).get("Name", "unknown")
        inst = s.get("InstanceStatus", {}).get("Status", "unknown")
        sys = s.get("SystemStatus", {}).get("Status", "unknown")
        print(f"{iid} | state={state} | instance={inst} | system={sys}")
        if state == "running" and (inst != "ok" or sys != "ok"):
            unhealthy = True
    return unhealthy


def main():
    parser = argparse.ArgumentParser(prog="ec2_health_checks")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("whoami", help="Print sts:GetCallerIdentity output")

    sub.add_parser("status", help="Print status checks for running instances")

    p_loop = sub.add_parser("loop", help="Continuously monitor EC2 status checks")
    p_loop.add_argument("--interval", type=int, default=30)

    args = parser.parse_args()

    if args.cmd == "whoami":
        print(whoami())
        return

    ec2 = session().client("ec2")

    if args.cmd == "status":
        ids = iter_running_instance_ids(ec2)
        if not ids:
            print("No running instances found.")
            return
        unhealthy = print_status_rows(ec2, ids)
        if unhealthy:
            raise SystemExit(2)
        return

    if args.cmd == "loop":
        interval = max(5, int(args.interval))
        print(f"{dt.datetime.utcnow().isoformat()}Z | starting monitor interval={interval}s")
        try:
            while True:
                ids = iter_running_instance_ids(ec2)
                if not ids:
                    print("No running instances found.")
                else:
                    unhealthy = print_status_rows(ec2, ids)
                    if not unhealthy:
                        print("All running instances OK.")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("Stopped by user.")
        return


if __name__ == "__main__":
    main()
