import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()


class Config:
    """프로젝트 전역 설정 클래스"""
    
    # 빗썸 API 설정
    BITHUMB_API_URL = "https://api.bithumb.com"
    BITHUMB_API_KEY = os.getenv("BITHUMB_API_KEY")
    BITHUMB_SECRET = os.getenv("BITHUMB_SECRET")

    # 로깅 설정
    LOG_DIR = "logs"
    LOG_FILE = f"{LOG_DIR}/trading.log"
    LOG_LEVEL = "INFO"
    LOG_MAX_BYTES = 5 * 1024 * 1024  # 5MB
    LOG_BACKUP_COUNT = 5
    LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(module)s:%(funcName)s] %(message)s"
 

    # 트레이딩 설정
    BUY_PERCENT = 0.5  # 매수 비율 (98%)
    SELL_PERCENT = 1.0  # 매도 비율 (100%)

    # 서버 설정
    FASTAPI_HOST = "127.0.0.1"
    FASTAPI_PORT = 8000
    DEBUG_MODE = True


class DevelopmentConfig(Config):
    """개발 환경 설정"""
    LOG_LEVEL = "DEBUG"
    FASTAPI_HOST = "127.0.0.1"
    DEBUG_MODE = True


class ProductionConfig(Config):
    """운영 환경 설정"""
    LOG_LEVEL = "INFO"
    FASTAPI_HOST = "0.0.0.0"
    DEBUG_MODE = False


# 환경 설정 선택
ENV = os.getenv("ENV", "development").lower()

if ENV == "production":
    settings = ProductionConfig()
else:
    settings = DevelopmentConfig()
