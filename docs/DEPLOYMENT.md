# Zeabur 部署

日期：2026-08-29

## 当前项目

- Zeabur 项目名：`xianyu-mink-radar`
- Project ID：`6a92edbbcb6b9b31c9e72c95`
- 区域：Tencent Singapore 2C 4GB
- 控制台：https://zeabur.com/projects/6a92edbbcb6b9b31c9e72c95

## 计划结构

- 一个 Python/Docker 服务（FastAPI + Scanner）
- Persistent Volume：`/data`，SQLite 放 `/data/xianyu.db`
- Health Check：`GET /health`
- 公网 HTTPS：`https://<service>.zeabur.app`
- 淘宝 OAuth Callback：`https://<service>.zeabur.app/auth/callback`

## 环境变量（在 Zeabur 控制台填写，不要写进 Git）

```text
TAOBAO_APP_KEY=
TAOBAO_APP_SECRET=
TAOBAO_SESSION_KEY=
TAOBAO_REFRESH_TOKEN=
BARK_SERVER=https://api.day.app
BARK_KEY=
BARK_KEY_2=
DATABASE_URL=sqlite:////data/xianyu.db
POLL_INTERVAL_SECONDS=45
DAILY_API_LIMIT=5000
TZ=Asia/Shanghai
PUBLIC_BASE_URL=
```

`PUBLIC_BASE_URL` 等 HTTPS 域名出来后再填。

## 当前进度

1. 项目已创建并改名。
2. 代码已具备 Dockerfile / `/health` / OAuth 路由。
3. **还没有 HTTPS 服务地址**：等代码仓库或本地上传绑定成功后才会生成。
4. 官方 API 凭据尚未拿到（闲鱼联盟要求企业支付宝资质），Scanner 不会在 POC 通过前空转打满额度。
