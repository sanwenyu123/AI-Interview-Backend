"""
应用配置
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field
import json


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基础配置
    APP_NAME: str = "AI面试助手"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置 (MySQL)
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/interview_db"
    DATABASE_ECHO: bool = False
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AI/LLM 配置
    # 提供商：openai（默认）/ openai_compat（OpenAI兼容端点，如 DeepSeek/OpenRouter/Ollama 等）/ azure
    AI_PROVIDER: str = "openai"

    # OpenAI 或 OpenAI 兼容端点
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str | None = None  # 兼容端点需设置，例如 https://api.deepseek.com/v1 或 http://localhost:11434/v1
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_MAX_TOKENS: int = 2000
    OPENAI_TEMPERATURE: float = 0.7

    # Azure OpenAI（可选）
    AZURE_OPENAI_API_KEY: str | None = None
    AZURE_OPENAI_ENDPOINT: str | None = None
    AZURE_OPENAI_API_VERSION: str | None = None
    AZURE_OPENAI_DEPLOYMENT: str | None = None

    # 语音配置（默认前端 WebSpeech，可切换为火山引擎等）
    VOICE_PROVIDER: str = "webspeech"  # webspeech | volcengine | aliyun | xunfei
    VOLC_ACCESS_KEY_ID: str | None = None
    VOLC_SECRET_ACCESS_KEY: str | None = None
    VOLC_REGION: str | None = "cn-beijing"
    VOLC_TTS_VOICE: str | None = "zh-CN-XiaoxiaoNeural"
    VOLC_TTS_SPEED: float = 1.0
    
    # CORS配置
    ALLOWED_ORIGINS: str = '["http://localhost:3000","http://127.0.0.1:3000"]'
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False
    
    # 文件上传
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # API配置
    API_V1_PREFIX: str = "/api/v1"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    
    @property
    def origins(self) -> List[str]:
        """解析CORS允许的源"""
        try:
            return json.loads(self.ALLOWED_ORIGINS)
        except:
            return ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()





