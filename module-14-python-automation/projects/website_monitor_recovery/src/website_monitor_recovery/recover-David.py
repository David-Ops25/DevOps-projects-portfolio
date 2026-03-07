import argparse
import time

import paramiko
import requests


def http_check(url: str, timeout: int) -> tuple[bool, str]:
    try:
        r = requests.get(url, timeout=timeout)
        return True, f"status={r.status_code} bytes={len(r.content)}"
    except requests.RequestException as e:
        return False, f"error={type(e).__name__}: {e}"


def run_ssh_cmd(host: str, user: str, key_path: str, cmd: str, timeout: int = 10) -> None:
    key = paramiko.RSAKey.from_private_key_file(key_path)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, pkey=key, timeout=timeout)
    _, stdout, stderr = client.exec_command(cmd)
    stdout.channel.recv_exit_status()
    out = stdout.read().decode(errors="ignore").strip()
    err = stderr.read().decode(errors="ignore").strip()
    client.close()
    if out:
        print(out)
    if err:
        print(err)


def main():
    ap = argparse.ArgumentParser(description="Monitor a URL and auto-recover via SSH if DOWN.")
    ap.add_argument("--url", required=True)
    ap.add_argument("--timeout", type=int, default=3)
    ap.add_argument("--ssh-host", required=True)
    ap.add_argument("--ssh-user", required=True)
    ap.add_argument("--ssh-key", required=True)
    ap.add_argument("--restart-cmd", default="sudo systemctl restart nginx")
    ap.add_argument("--recheck-wait", type=int, default=3)
    args = ap.parse_args()

    ok, msg = http_check(args.url, args.timeout)
    if ok:
        print(f"UP {msg}")
        return

    print(f"DOWN {msg}")
    print(f"Running recovery over SSH: {args.restart_cmd}")
    run_ssh_cmd(args.ssh_host, args.ssh_user, args.ssh_key, args.restart_cmd)
    print(f"Recovery command executed. Waiting {args.recheck_wait}s then rechecking...")
    time.sleep(args.recheck_wait)

    ok2, msg2 = http_check(args.url, args.timeout)
    if ok2:
        print(f"RECOVERED {msg2}")
        return
    print(f"STILL_DOWN {msg2}")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
