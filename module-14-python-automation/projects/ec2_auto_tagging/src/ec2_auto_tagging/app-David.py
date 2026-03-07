import argparse
from dataclasses import dataclass

import boto3


@dataclass(frozen=True)
class TagKV:
    key: str
    value: str


def parse_tags(pairs: list[str]) -> list[TagKV]:
    out: list[TagKV] = []
    for p in pairs:
        if "=" not in p:
            raise ValueError(f"Bad tag '{p}'. Use Key=Value.")
        k, v = p.split("=", 1)
        k = k.strip()
        v = v.strip()
        if not k:
            raise ValueError(f"Bad tag '{p}'. Empty key.")
        out.append(TagKV(k, v))
    return out


def session():
    return boto3.session.Session()


def list_instances(ec2, only_running: bool) -> list[str]:
    filters = []
    if only_running:
        filters.append({"Name": "instance-state-name", "Values": ["running"]})
    resp = ec2.describe_instances(Filters=filters) if filters else ec2.describe_instances()
    ids: list[str] = []
    for r in resp.get("Reservations", []):
        for i in r.get("Instances", []):
            ids.append(i["InstanceId"])
    return ids


def main():
    ap = argparse.ArgumentParser(description="Auto-tag EC2 instances")
    ap.add_argument("--only-running", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--tags", nargs="+", required=True, help="Key=Value pairs")
    args = ap.parse_args()

    tags = parse_tags(args.tags)
    tag_spec = [{"Key": t.key, "Value": t.value} for t in tags]

    ec2 = session().client("ec2")
    ids = list_instances(ec2, args.only_running)

    if not ids:
        print("No instances matched selection.")
        return

    print("Instances that match selection:")
    for iid in ids:
        print(f" - {iid}")

    if args.dry_run:
        print("DRY RUN: No tags were applied.")
        return

    ec2.create_tags(Resources=ids, Tags=tag_spec)
    print("✅ Tags applied.")


if __name__ == "__main__":
    main()
