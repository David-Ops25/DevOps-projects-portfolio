# Project — Website Monitoring & Auto-Recovery

**Goal:** Monitor a web endpoint and automatically recover service via SSH if it goes down.

## Run (monitor only)
```bash
python3 src/website_monitor_recovery/monitor.py --url http://<PUBLIC_IP>/ --retries 3 --sleep 2
```

## Run (monitor + recover)
```bash
python3 src/website_monitor_recovery/recover.py \
  --url http://<PUBLIC_IP>/ \
  --ssh-host <PUBLIC_IP> \
  --ssh-user ec2-user \
  --ssh-key /path/to/key.pem \
  --restart-cmd "sudo systemctl restart nginx" \
  --recheck-wait 3
```

### Sample proof output
```
DOWN error=Connection refused
Running recovery over SSH: sudo systemctl restart nginx
RECOVERED status=200
```
