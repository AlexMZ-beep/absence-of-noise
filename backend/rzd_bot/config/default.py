from os import environ


class DefaultSettings:
    PATH_PREFIX: str = environ.get("PATH_PREFIX", "/api/v1")
    APP_HOST: str = environ.get("APP_HOST", "http://0.0.0.0")
    APP_PORT: int = int(environ.get("APP_PORT", 8080))
    REDIS_URL: str = environ.get("REDIS_URL", "redis://0.0.0.0:6379/0")
    LLM_URL: str = environ.get("LLM_URL", "http://176.109.110.144:8000/v1/")
    LLM_API_KEY: str = environ.get("LLM_API_KEY", "token-rzd-mz")
