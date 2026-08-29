# Xianyu Mink Radar / 闲鱼抽刀貂雷达

采购辅助：官方 API 搜闲鱼公开商品 → 去重 → Bark。不做自动拍、不做自动聊。

**当前阶段：Phase 0。** 官方接口 `alibaba.idle.affiliate.material.query` 文档已核对，但淘宝账号 `a842105620` 无法入驻闲鱼联盟（需企业支付宝），因此还没有真实物料查询结果。详见 `docs/OFFICIAL_API_NOTES.md` 和 `docs/API_POC_REPORT.md`。

## 架构

闲鱼官方物料查询 → 本地按 `create_time` 排序 → `item_id` 去重 → 关键词/排除规则过滤 → Bark。FastAPI 提供 `/health` 和淘宝 OAuth 回调。

## 本地

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # 填凭据，不要提交 .env
uvicorn app.main:app --reload --port 8080
python scripts/test_xianyu_api.py --keyword "抽刀貂"
```

## 环境变量

见 `.env.example`。AppSecret / SessionKey / Bark Key 禁止进 Git。

## 修改关键词 / 扫描间隔

- 关键词与排除词：`config/keywords.yaml`
- 扫描间隔：`POLL_INTERVAL_SECONDS`

测试额度常见 5000 次/天。POC 通过前 Scanner 不轮询，避免空转打满额度。

## Zeabur

见 `docs/DEPLOYMENT.md`。数据库必须挂 Persistent Volume 到 `/data`。

## 重新授权

浏览器打开 `https://<域名>/auth/taobao`。Session 通常不能自动 refresh，到期前会 Bark 提醒（POC 通过后实现）。

## 备份数据库

复制 `/data/xianyu.db`。
