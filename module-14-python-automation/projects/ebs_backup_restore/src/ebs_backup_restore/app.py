import argparse
import datetime as dt

import boto3


CREATED_BY = "module14-python-automation"


def session():
    return boto3.session.Session()


def list_volumes(ec2) -> list[dict]:
    resp = ec2.describe_volumes()
    return resp.get("Volumes", [])


def create_snapshots(ec2, dry_run: bool) -> None:
    vols = list_volumes(ec2)
    print(f"Found {len(vols)} volume(s).")
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

    for v in vols:
        vid = v["VolumeId"]
        az = v.get("AvailabilityZone")
        size = v.get("Size")
        state = v.get("State")
        print(f"- {vid} | {az} | {size}GiB | state={state}")

    if dry_run:
        print("\nDRY RUN: No snapshots created.")
        return

    for v in vols:
        vid = v["VolumeId"]
        desc = f"Module14 backup {today} volume={vid}"
        snap = ec2.create_snapshot(VolumeId=vid, Description=desc)
        sid = snap["SnapshotId"]
        ec2.create_tags(
            Resources=[sid],
            Tags=[
                {"Key": "CreatedBy", "Value": CREATED_BY},
                {"Key": "CreatedOn", "Value": today},
            ],
        )
        print(f"✅ Created snapshot {sid} for volume {vid}")


def cleanup_snapshots(ec2, older_than_days: int, dry_run: bool) -> None:
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=older_than_days)
    resp = ec2.describe_snapshots(
        OwnerIds=["self"],
        Filters=[{"Name": "tag:CreatedBy", "Values": [CREATED_BY]}],
    )
    snaps = [s for s in resp.get("Snapshots", []) if s["State"] == "completed"]
    old = [s for s in snaps if s["StartTime"] < cutoff]

    if not old:
        print(f"No completed snapshots older than {older_than_days} day(s) to delete.")
        return

    for s in old:
        print(f"- {s['SnapshotId']} | {s['VolumeId']} | {s['StartTime']}")

    if dry_run:
        print("\nDRY RUN: No snapshots deleted.")
        return

    for s in old:
        ec2.delete_snapshot(SnapshotId=s["SnapshotId"])
        print(f"✅ Deleted {s['SnapshotId']}")


def restore_volume(ec2, az: str, volume_type: str = "gp3", tag: str | None = None) -> None:
    resp = ec2.describe_snapshots(
        OwnerIds=["self"],
        Filters=[{"Name": "tag:CreatedBy", "Values": [CREATED_BY]}],
    )
    snaps = [s for s in resp.get("Snapshots", []) if s["State"] == "completed"]
    if not snaps:
        raise SystemExit("No completed snapshots found.")
    snaps.sort(key=lambda s: s["StartTime"], reverse=True)
    s = snaps[0]

    sid = s["SnapshotId"]
    size = s["VolumeSize"]
    print(f"Using snapshot: {sid} | start={s['StartTime']} | size={size}GiB")
    print(f"Will create volume in {az} | type={volume_type} | size={size}GiB")

    tags = [{"Key": "CreatedBy", "Value": CREATED_BY}]
    if tag and "=" in tag:
        k, v = tag.split("=", 1)
        tags.append({"Key": k, "Value": v})

    vol = ec2.create_volume(
        AvailabilityZone=az,
        SnapshotId=sid,
        VolumeType=volume_type,
        Size=size,
        TagSpecifications=[{"ResourceType": "volume", "Tags": tags}],
    )
    print(f"✅ New volume created: {vol['VolumeId']}")


def main():
    ap = argparse.ArgumentParser(prog="ebs_backup_restore")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("snapshot")
    p1.add_argument("--dry-run", action="store_true")

    p2 = sub.add_parser("cleanup")
    p2.add_argument("--older-than-days", type=int, default=7)
    p2.add_argument("--dry-run", action="store_true")

    p3 = sub.add_parser("restore")
    p3.add_argument("--az", required=True)
    p3.add_argument("--tag", default=None)

    args = ap.parse_args()
    ec2 = session().client("ec2")

    if args.cmd == "snapshot":
        create_snapshots(ec2, args.dry_run)
    elif args.cmd == "cleanup":
        cleanup_snapshots(ec2, args.older_than_days, args.dry_run)
    elif args.cmd == "restore":
        restore_volume(ec2, args.az, tag=args.tag)


if __name__ == "__main__":
    main()
