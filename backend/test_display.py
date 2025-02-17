from app.utils.display import display_log



test_logs = [
    '[2025-02-17 19:08:11] [INFO] [main:startup] 서버가 시작되었습니다.',
    '[2025-02-17 19:10:23] [ERROR] [api:handle_request] API 요청 실패: {"error": "서버 오류", "code": 500, "details": "내부 서버 문제"}',
    '[2025-02-17 19:12:45] [DEBUG]  [db:query_database] 쿼리 실행 완료.',
    '[2025-02-17 19:14:30] [WARNING]  [auth:check_token] 토큰 만료 경고: {"expires_in": 300}',
    '[2025-02-17 19:16:50] [INFO] [trade:execute] 거래 실행 결과: {"status": "test", "message": "가상 거래 테스트 실행됨", "order_id": "TEST_ORDER_ID", "filled_quantity": 9999.0, "avg_price": 9999.0, "fee": 9999.0, "net_settlement": 9999.0} 추가 정보 있음.'
]


for log in test_logs:
    display_log(log)


