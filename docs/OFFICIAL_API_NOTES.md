# 官方 API 笔记（2026-08-29 现场核对）

来源：https://developer.alibaba.com/docs/api.htm?apiId=71090  
控制台：https://work.open.taobao.com/open-console-home/new （账号 a842105620）

## 接口是否存在

**存在。** 文档类目：闲客联盟。

- 名称：`alibaba.idle.affiliate.material.query`
- 中文：闲鱼联盟-物料查询
- 标记：**免费**、**需要授权**（必须带 session / AccessToken）
- 示例：`client.execute(req, sessionKey)`

同组相关接口：

- `alibaba.idle.affiliate.material.guide.get` 物料指南
- `alibaba.idle.affiliate.general.link.convert` 推广转链
- `alibaba.idle.affiliate.material.exact.get` 物料精确获取

## 调用入口

文档示例使用官方 SDK 的 `url`（即 TOP 网关）。Phase 0 代码默认：

```text
https://eco.taobao.com/router/rest
```

以控制台/SDK 当前网关为准，不猜测沙箱地址。

## 请求结构

入参对象：`materials_query_vo`（MaterialsQueryVO，必须）

文档示例字段：

- `materialType`：示例 `1`
- `pageRequest.pageSize` / `pageRequest.pageNum`
- `itemGuideVO.keyword`：示例「手机」
- `itemGuideVO.itemPublisherTime`：示例 `in1day`（近 1 天）
- `itemGuideVO.sellerCreditLevel`：示例 `excellent`
- `itemGuideVO.tabName`、`filterLevel5Yxp`、`filterYhb`、`sellerName`

**未在文档中看到 page_size 硬上限数字。** 示例用 10。POC 从 10 起步，再试官方允许的更大值。

**不得假设返回顺序 = 最新发布。** 本地必须按 `create_time` 再排。

## 返回字段（文档响应示例）

`result.result.material_d_t_o[]` → `item_info.item_base_info`：

| 字段 | 文档含义 |
|---|---|
| item_id | 商品 ID |
| reserve_price | 售价 |
| original_price | 原价 |
| item_title | 标题 |
| stuff_status | 成色 |
| item_desc | 描述 |
| category_name | 类目 |
| status | promoting / cannotPromote / sold / offline / unknown |
| create_time | 发布时间 |
| update_time | 修改时间 |
| seller_level_code | 卖家信用 |
| is_fish_shop | 是否鱼小铺 |
| image_urls | 文档另有图片字段（以实际 JSON 为准） |
| item_promote_info.commission_rate | 佣金比例（联盟属性） |

## 认证 / Token

- 需要用户授权。`access_token` 在 TOP 体系即 `sessionkey`。
- 测试态应用通常 **5000 次/天**，上线后一般类型默认更高（文档写一般 100 万/天，以控制台为准）。
- Session 常见 2–3 个月，**不能自动 refresh**，到期需重新授权。
- 回调 URL 必须公网 http(s)，不能是阿里系域名，不能是 127.0.0.1。

OAuth：

```text
https://oauth.taobao.com/authorize
https://oauth.taobao.com/token
```

code 换 token 也可用 TOP：`taobao.top.auth.token.create`。

## 控制台实测：本账号能否创建「闲鱼联盟」应用

**不能。**

选择「阿里生态API开放 → 闲鱼 → 闲鱼联盟」后：

- 确认类目按钮 **禁用**
- 弹窗：「抱歉，您不符合该类目的入驻要求」
- **企业资质认证：认证未通过**
- 描述：**你的支付宝账号不是企业资质认证**
- 类目说明写的是「闲鱼联盟代理商」

「闲鱼电商」类目本账号可以点「确认类目」，但开放权限包只有：

- 系统工具 381
- 消息服务 12159
- 闲鱼开放平台服务（商品管理）17805

**没有** 闲客联盟物料查询。该类目是卖家/商品管理，不是全站搜新货。

因此：在当前个人支付宝主体下，**无法合法申请 `alibaba.idle.affiliate.material.query`。**

## 2026-08-29 二次现场核对

账号 `a842105620`：

- 我的应用：**您还没有创建过应用**
- 应用资质：暂无数据
- 闲鱼联盟：底部 **身份不通过**，确认类目按钮禁用
- 弹窗原文：**企业资质认证 / 认证未通过 / 你的支付宝账号不是企业资质认证**
- 闲鱼联盟权限包：`31298` 闲鱼联盟服务商权限包（物料查询应在此包内）
- 未创建「闲鱼电商」应用：该类目权限包只有 381 / 12159 / 17805，没有物料查询，创建了也无法跑 POC
- 闲鱼垂直行业-C端（确认类目可点，未创建）：12159 / 381 / 29134 闲鱼AutoTrade / 29691 安康容器。无物料查询，且 AutoTrade 属于自动交易方向，本项目不做
- 闲鱼垂直行业-B端（确认类目可点，未创建）：17805 / 12159 / 381 / 29691。仍是卖家商品管理，无全站搜新货

应用类型页面可选：淘宝购物小程序、商家经营工具、小程序插件、阿里生态API开放、内容创作工具。物料查询只在 **阿里生态API开放 → 闲鱼联盟**。

## 对 POC 的影响

Phase 0 代码可以先写好（签名、解析、保存 raw JSON、按 create_time 排序）。

在拿到：

1. 企业支付宝资质
2. 闲鱼联盟类目应用
3. AppKey / AppSecret
4. 授权 SessionKey

之前，**无法完成真实 API 调用，也不能判断覆盖率和发现延迟。**
