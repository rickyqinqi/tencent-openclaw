# Tencent OpenClaw 🦞

OpenClaw（小龙虾）AI Agent 网关 - 腾讯云服务器部署工程

## 项目简介

在腾讯云服务器 (Ubuntu 24.04) 上部署 [OpenClaw](https://github.com/openclaw/openclaw) AI Agent 网关，
并配置 [硅基流动 (SiliconFlow)](https://siliconflow.cn) 免费大模型 API。

## 架构

```
用户 → OpenClaw Gateway (端口 18789) → SiliconFlow API → 大模型推理
                                        ├── DeepSeek V3 (主模型)
                                        ├── Qwen 2.5 7B (回退模型)
                                        └── DeepSeek R1 (推理模型)
```

## 服务器信息

- **IP**: 118.89.89.113
- **OS**: Ubuntu 24.04 LTS
- **OpenClaw**: v2026.4.26
- **Gateway 端口**: 18789
- **Node.js**: v22.x

## 部署步骤

### 1. SSH 连接

```bash
ssh ubuntu@118.89.89.113
```

### 2. 安装 Node.js

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 3. 安装 OpenClaw

```bash
sudo npm install -g openclaw@latest
```

### 4. 初始化 OpenClaw

```bash
openclaw doctor --fix
```

### 5. 配置 SiliconFlow 模型

编辑 `~/.openclaw/openclaw.json`，添加 SiliconFlow 作为模型提供商（参考 `config/openclaw.json` 模板）。

> ⚠️ 请将 `YOUR_SILICONFLOW_API_KEY` 替换为你的 SiliconFlow API Key。  
> 新用户注册可获得 2000 万免费 tokens：https://cloud.siliconflow.cn

### 6. 重启 Gateway

```bash
XDG_RUNTIME_DIR=/run/user/$(id -u) systemctl --user restart openclaw-gateway.service
```

### 7. 验证

```bash
# 查看模型列表
openclaw models list

# 测试 API
curl https://api.siliconflow.cn/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"model":"deepseek-ai/DeepSeek-V3","messages":[{"role":"user","content":"你好"}]}'
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `ssh_connect.py` | SSH 连接测试脚本 |
| `ssh_cmd.py` | 远程配置 OpenClaw + SiliconFlow 的脚本 |
| `ssh_restart.py` | 重启 Gateway 并验证 API 的脚本 |
| `config/openclaw.json` | OpenClaw 配置模板 |
| `systemd/openclaw-gateway.service` | systemd 用户服务文件 |
| `deploy.sh` | 一键部署脚本 |

## 注意事项

- SiliconFlow 免费模型有速率限制，适合测试和轻量使用
- Gateway 默认监听 `127.0.0.1:18789`，如需外网访问请配置反向代理
- API Key 请妥善保管，不要提交到公开仓库

## License

MIT
