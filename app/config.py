from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    taobao_app_key: str = ""
    taobao_app_secret: str = ""
    taobao_session_key: str = ""
    taobao_refresh_token: str = ""
    taobao_gateway: str = "https://eco.taobao.com/router/rest"
    bark_server: str = "https://api.day.app"
    bark_key: str = ""
    bark_key_2: str = ""
    database_url: str = "sqlite:///data/xianyu.db"
    poll_interval_seconds: int = 45
    daily_api_limit: int = 5000
    public_base_url: str = ""
    tz: str = "Asia/Shanghai"


settings = Settings()
