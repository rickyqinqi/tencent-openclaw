#!/bin/bash
# OpenClaw 一键部署脚本 - 腾讯云 Ubuntu 24.04
set -e

echo "=== OpenClaw Deployment Script ==="

# 1. Install Node.js
echo "[1/5] Installing Node.js 22.x..."
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# 2. Install OpenClaw
echo "[2/5] Installing OpenClaw..."
sudo npm install -g openclaw@latest

# 3. Initialize
echo "[3/5] Running openclaw doctor --fix..."
openclaw doctor --fix

# 4. Configure SiliconFlow
echo "[4/5] Configuring SiliconFlow provider..."
if [ -z "$SILICONFLOW_API_KEY" ]; then
    echo "Warning: SILICONFLOW_API_KEY not set. Edit ~/.openclaw/openclaw.json manually."
fi

if [ ! -f ~/.openclaw/openclaw.json ]; then
    echo "No config found, copying template..."
    mkdir -p ~/.openclaw
    cp config/openclaw.json ~/.openclaw/openclaw.json
    if [ -n "$SILICONFLOW_API_KEY" ]; then
        sed -i "s/YOUR_SILICONFLOW_API_KEY/$SILICONFLOW_API_KEY/" ~/.openclaw/openclaw.json
    fi
fi

# 5. Setup systemd service
echo "[5/5] Setting up systemd user service..."
mkdir -p ~/.config/systemd/user
cp systemd/openclaw-gateway.service ~/.config/systemd/user/
XDG_RUNTIME_DIR=/run/user/$(id -u) systemctl --user daemon-reload
XDG_RUNTIME_DIR=/run/user/$(id -u) systemctl --user enable --now openclaw-gateway.service

echo ""
echo "=== Deployment Complete! ==="
echo "Gateway: http://127.0.0.1:18789"
echo "Models: run 'openclaw models list' to see available models"
echo ""
echo "To test: curl https://api.siliconflow.cn/v1/chat/completions -H 'Authorization: Bearer YOUR_KEY' ..."
