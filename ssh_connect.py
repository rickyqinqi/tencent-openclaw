#!/usr/bin/env python3
"""SSH connection test to OpenClaw server."""

import paramiko
import os

HOSTNAME = "118.89.89.113"
PORT = 22
USERNAME = "ubuntu"
PASSWORD = os.environ.get("SSH_PASSWORD", "")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("Connecting...", flush=True)
client.connect(hostname=HOSTNAME, port=PORT, username=USERNAME, password=PASSWORD, timeout=15)
print("Connected!", flush=True)

stdin, stdout, stderr = client.exec_command("uname -a; echo '---'; free -h; echo '---'; df -h /", timeout=10)
print(stdout.read().decode())

client.close()
