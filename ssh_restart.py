#!/usr/bin/env python3
"""Restart OpenClaw Gateway and verify SiliconFlow API connectivity."""

import paramiko
import os
import time

HOSTNAME = "118.89.89.113"
PORT = 22
USERNAME = "ubuntu"
PASSWORD = os.environ.get("SSH_PASSWORD", "")
SILICONFLOW_API_KEY = os.environ.get("SILICONFLOW_API_KEY", "")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=HOSTNAME, port=PORT, username=USERNAME, password=PASSWORD, timeout=15)

def run(cmd, timeout=30):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return stdout.read().decode() + stderr.read().decode()

print("Restarting gateway...", flush=True)
r = run("XDG_RUNTIME_DIR=/run/user/$(id -u) systemctl --user restart openclaw-gateway.service 2>&1")
time.sleep(5)

print(f"Port: {run('ss -tlnp | grep 18789')}", flush=True)
print(f"Models:\n{run('openclaw models list 2>&1 | head -10')}", flush=True)

if SILICONFLOW_API_KEY:
    r = run(f'''curl -s --max-time 30 https://api.siliconflow.cn/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer {SILICONFLOW_API_KEY}" -d '{{"model":"deepseek-ai/DeepSeek-V3","messages":[{{"role":"user","content":"Hi"}}],"max_tokens":20}}' 2>&1''', 45)
    print(f"API test: {r}", flush=True)

print("Done!", flush=True)
client.close()
