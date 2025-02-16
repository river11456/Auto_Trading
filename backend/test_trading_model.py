from app.models.trading_model import TradeRequest, TradeResponse, TradeSignal
from pydantic import ValidationError

# ✅ 1️⃣ 유효한 데이터 테스트
def test_valid_data():
    valid_data = {
        "signal": "buy",
        "symbol": "USDT",
        "amount": 100.0
    }
    try:
        request = TradeRequest(**valid_data)
        print("✅ 유효한 데이터 검증 성공:", request)
    except ValidationError as e:
        print("❌ 유효한 데이터 검증 실패:", e)

# ❌ 2️⃣ 잘못된 signal 테스트
def test_invalid_signal():
    invalid_data = {
        "signal": "invalid",
        "symbol": "USDT",
        "amount": 100.0
    }
    try:
        TradeRequest(**invalid_data)
    except ValidationError as e:
        print("🔴 signal 오류 감지:", e)

# ❌ 3️⃣ 음수 amount 테스트
def test_negative_amount():
    invalid_data = {
        "signal": "buy",
        "symbol": "USDT",
        "amount": -10
    }
    try:
        TradeRequest(**invalid_data)
    except ValidationError as e:
        print("🔴 amount 음수 오류 감지:", e)

# ❌ 4️⃣ symbol 오타 테스트
def test_invalid_symbol():
    invalid_data = {
        "signal": "buy",
        "symbol": "BTC",  # 지원하지 않는 심볼
        "amount": 100.0
    }
    try:
        TradeRequest(**invalid_data)
    except ValidationError as e:
        print("🔴 symbol 오류 감지:", e)

# 🧪 5️⃣ TEST 신호 테스트 (새로 추가된 신호)
def test_test_signal():
    test_data = {
        "signal": "test",
        "symbol": "USDT",
        "amount": 50.0
    }
    try:
        request = TradeRequest(**test_data)
        print("✅ TEST 신호 검증 성공:", request)
    except ValidationError as e:
        print("❌ TEST 신호 검증 실패:", e)


# 🚀 모든 테스트 실행
if __name__ == "__main__":
    print("\n🎯 [TEST: 유효 데이터]")
    test_valid_data()

    print("\n🚨 [TEST: 잘못된 signal]")
    test_invalid_signal()

    print("\n🚨 [TEST: 음수 amount]")
    test_negative_amount()

    print("\n🚨 [TEST: 잘못된 symbol]")
    test_invalid_symbol()

    print("\n🛠️ [TEST: TEST 신호]")
    test_test_signal()
