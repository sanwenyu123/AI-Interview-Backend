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
    # 火山引擎短语音 ASR （HTTP）
    VOLC_ASR_APP_ID: str | None = None
    VOLC_ASR_TOKEN: str | None = None
    VOLC_ASR_LANGUAGE: str = "zh-CN"
    VOLC_ASR_FORMAT: str = "wav"  # wav/mp3/opus 等
    # 录音文件识别 HTTP 端点（若不为空则优先使用），例如：
    # https://openspeech.bytedance.com/api/v2/short_asr （以你的文档为准）
    VOLC_ASR_ENDPOINT: str | None = None
    # 表单里承载音频文件的字段名，文档一般为 file 或 audio
    VOLC_ASR_FILE_FIELD: str = "file"
    # 是否用 multipart/form-data 方式提交（新版接口通常需要）
    VOLC_ASR_USE_MULTIPART: bool = True

    # TOS 对象存储（用于生成公网可访问音频 URL）
    TOS_ACCESS_KEY_ID: str | None = None
    TOS_SECRET_ACCESS_KEY: str | None = None
    TOS_REGION: str | None = None
    TOS_BUCKET: str | None = None
    TOS_ENDPOINT: str | None = None  # 例如 tos-cn-beijing.volces.com
    TOS_SSL_VERIFY: bool = True  # 如遇本机证书链问题可暂时设为 False
    
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





