# 配置管理
import os
from dotenv import load_dotenv

load_dotenv()

# API配置
AI_SERVICE_HOST = os.getenv("AI_SERVICE_HOST", "0.0.0.0")
AI_SERVICE_PORT = int(os.getenv("AI_SERVICE_PORT", "8000"))

# Qwen API配置（使用通义千问）
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "sk-bb2f7a6f43454349ab1168136e9ec523")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/api/v1")

# 模型配置
CHAT_MODEL = os.getenv("CHAT_MODEL", "qwen3-max")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-v4")

# Redis配置
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "1"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# SpringBoot后端配置
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080/api")

# 向量配置
VECTOR_DIMENSION = int(os.getenv("VECTOR_DIMENSION", "1536"))
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
