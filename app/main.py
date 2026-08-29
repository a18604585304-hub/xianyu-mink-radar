from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse

from app.config import settings
from app.monitor.scanner import STATUS as SCANNER_STATUS
from app.storage.db import init_db

app = FastAPI(title="Xianyu Mink Radar", version="0.0.1")


@app.on_event("startup")
def _startup():
    init_db()


@app.get("/health")
def health():
    has_key = bool(settings.taobao_app_key)
    has_session = bool(settings.taobao_session_key)
    return {
        "status": "ok",
        "scanner_status": SCANNER_STATUS,
        "api_status": "credentials_missing" if not (has_key and has_session) else "configured_untested",
        "auth_status": "no_session" if not has_session else "session_present",
        "last_scan": None,
        "last_successful_api_request": None,
        "last_new_item": None,
        "today_api_calls": 0,
        "today_new_items": 0,
        "today_pushes": 0,
        "average_discovery_delay": None,
        "p50_discovery_delay": None,
        "p90_discovery_delay": None,
        "phase": 0,
        "note": "闲鱼联盟类目当前账号企业资质未通过，官方物料查询 API 尚不能调用。",
    }


@app.get("/auth/taobao")
def auth_taobao():
    if not settings.taobao_app_key or not settings.public_base_url:
        return JSONResponse(
            {"error": "缺少 TAOBAO_APP_KEY 或 PUBLIC_BASE_URL"},
            status_code=400,
        )
    redirect = settings.public_base_url.rstrip("/") + "/auth/callback"
    url = (
        "https://oauth.taobao.com/authorize"
        f"?response_type=code&client_id={settings.taobao_app_key}"
        f"&redirect_uri={redirect}"
        "&state=mink-radar"
    )
    return RedirectResponse(url)


@app.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    err = request.query_params.get("error")
    if err:
        return JSONResponse({"error": err, "detail": dict(request.query_params)})
    if not code:
        return JSONResponse({"error": "no_code", "query": dict(request.query_params)})
    return JSONResponse(
        {
            "ok": True,
            "code_received": True,
            "note": "凭据齐全后在此用 code 换 session。当前未配置 AppSecret，未向淘宝换 token。",
        }
    )
