#!/usr/bin/env python3
"""
Configure OpenClaw with SiliconFlow provider on remote server.
Reads current config, merges SiliconFlow settings, writes back via SFTP.
"""

import paramiko
import json
import os

HOSTNAME = "118.89.89.113"
PORT = 22
USERNAME = "ubuntu"
PASSWORD = os.environ.get("SSH_PASSWORD", "")
SILICONFLOW_API_KEY = os.environ.get("SILICONFLOW_API_KEY", "YOUR_API_KEY")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print("Connecting...", flush=True)
client.connect(hostname=HOSTNAME, port=PORT, username=USERNAME, password=PASSWORD, timeout=15)
print("Connected!", flush=True)

# Read current config
stdin, stdout, stderr = client.exec_command("cat ~/.openclaw/openclaw.json", timeout=10)
current_config_str = stdout.read().decode()

try:
    config = json.loads(current_config_str)
except:
    config = {}

if "models" not in config:
    config["models"] = {}
if "providers" not in config.get("models", {}):
    config["models"]["providers"] = {}

config["models"]["mode"] = "merge"
config["models"]["providers"]["siliconflow"] = {
    "baseUrl": "https://api.siliconflow.cn/v1",
    "apiKey": SILICONFLOW_API_KEY,
    "api": "openai-completions",
    "models": [
        {
            "id": "Qwen/Qwen2.5-7B-Instruct",
            "name": "Qwen 2.5 7B (Free)",
            "reasoning": False,
            "input": ["text"],
            "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
            "contextWindow": 32768,
            "maxTokens": 8192
        },
        {
            "id": "deepseek-ai/DeepSeek-V3",
            "name": "DeepSeek V3",
            "reasoning": False,
            "input": ["text"],
            "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
            "contextWindow": 65536,
            "maxTokens": 8192
        },
        {
            "id": "deepseek-ai/DeepSeek-R1",
            "name": "DeepSeek R1 (Reasoning)",
            "reasoning": True,
            "input": ["text"],
            "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
            "contextWindow": 65536,
            "maxTokens": 8192
        }
    ]
}

if "agents" not in config:
    config["agents"] = {}
if "defaults" not in config["agents"]:
    config["agents"]["defaults"] = {}
config["agents"]["defaults"]["model"] = {
    "primary": "siliconflow/deepseek-ai/DeepSeek-V3",
    "fallbacks": ["siliconflow/Qwen/Q2.5-7B-Instruct"]
}

new_config_json = json.dumps(config, indent=2, ensure_ascii=False)

# Write back via SFTP
sftp = client.open_sftp()
with sftp.open("/home/ubuntu/.openclaw/openclaw.json", "w") as f:
    f.write(new_config_json)
sftp.close()
print("Config written!", flush=True)

# Set permissions
stdin, stdout, stderr = client.exec_command("chmod 600 ~/.openclaw/openclaw.json", timeout=10)
stdout.read()

# Restart gateway
stdin, stdout, stderr = client.exec_command(
    "XDG_RUNTIME_DIR=/run/user/$(id -u) systemctl --user restart openclaw-gateway.service 2>&1",
    timeout=30
)
print(f"Restart: {stdout.read().decode()}", flush=True)
print("Done!", flush=True)
client.close()
