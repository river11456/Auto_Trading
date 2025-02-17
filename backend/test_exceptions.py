from fastapi.testclient import TestClient
from fastapi.exceptions import RequestValidationError
from app.exceptions.exception_handler import (
    validation_exception_handler,
    general_exception_handler,
    api_error_handler,
    business_logic_error_handler,
)
from app.exceptions.custom_exceptions import APIError, BusinessLogicError
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from app.utils.logger import logger



# FastAPI 앱 생성
app = FastAPI()

# 예외 핸들러 등록
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(APIError, api_error_handler)
app.add_exception_handler(BusinessLogicError, business_logic_error_handler)

# 테스트용 데이터 모델
class TestRequest(BaseModel):
    value: int = Field(..., gt=0, description="양수만 허용됨")

# 테스트 엔드포인트 정의
@app.post("/test/validation-error")
async def test_validation_error(req: TestRequest):
    return {"message": "정상 요청", "value": req.value}

@app.get("/test/general-error")
async def test_general_error():
    raise Exception("일반적인 서버 오류 발생!")

@app.get("/test/api-error")
async def test_api_error():
    raise APIError("외부 API 호출 실패")

@app.get("/test/business-error")
async def test_business_error():
    raise BusinessLogicError("비즈니스 로직 오류 발생")

# 테스트 클라이언트 생성
client = TestClient(app)

# 테스트 실행 함수
def run_tests():
    test_cases = [
        ("POST", "/test/validation-error", {"value": -1}),
        #("GET", "/test/general-error", None),
        ("GET", "/test/api-error", None),
        ("GET", "/test/business-error", None),
    ]

    for method, url, json_data in test_cases:
        print(f"\n🔍 Testing {url} ({method})")
        if method == "POST":
            response = client.post(url, json=json_data)
        else:
            response = client.get(url)

        
        logger.info(f"✅ Status Code: {response.status_code}")
        logger.info(f"📝 Response: {response.json()}")


if __name__ == "__main__":
    run_tests()
