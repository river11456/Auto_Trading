class APIError(Exception):
    """외부 API 호출 실패 시 발생하는 예외"""
    pass


class BusinessLogicError(Exception):
    """애플리케이션 비즈니스 로직 오류"""
    pass
