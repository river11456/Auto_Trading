from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional, List
from enum import Enum


# 거래 시그널 Enum
class TradeSignal(str, Enum):
    BUY = "buy"
    SELL = "sell"
    TEST = "test"


# 웹훅 요청 데이터 모델
class TradeRequest(BaseModel):
    signal: TradeSignal = Field(..., description="거래 신호 (buy, sell, test)")
    symbol: str = Field(..., description="거래 심볼 (예: USDT, BTC, ETH 등)")
    amount: Optional[float] = Field(None, gt=0, description="거래 수량 (선택 사항)")

    @field_validator("signal")
    @classmethod
    def validate_signal(cls, v):
        if v not in {"buy", "sell", "test"}:
            raise ValueError("signal 필드는 'buy', 'sell', 'test'만 허용됩니다.")
        return v


# 거래 응답 데이터 모델
class TradeResponse(BaseModel):
    status: str = Field(..., description="응답 상태 (success 또는 error)")
    message: str = Field(..., description="결과 메시지")
    order_id: str = Field(..., description="거래 주문 ID")
    filled_quantity: float = Field(..., ge=0, description="체결된 수량")
    avg_price: float = Field(..., ge=0, description="평균 체결 가격")
    fee: float = Field(..., ge=0, description="거래 수수료")
    net_settlement: float = Field(..., description="최종 정산 금액")




"""
빗썸 api 응답을 사용하기 편하도록 데이터 구조 재구성    

"""
class TickerResponse(BaseModel):
    status: str = Field(..., description="결과 상태 코드 (0000: 정상, 그 외 에러 코드)")
    opening_price: float = Field(..., ge=0, description="시가 00시 기준")
    closing_price: float = Field(..., ge=0, description="종가 00시 기준")
    min_price: float = Field(..., ge=0, description="저가 00시 기준")
    max_price: float = Field(..., ge=0, description="고가 00시 기준")
    units_traded: float = Field(..., ge=0, description="거래량 00시 기준")
    acc_trade_value: float = Field(..., ge=0, description="거래금액 00시 기준")
    prev_closing_price: float = Field(..., ge=0, description="전일종가")
    units_traded_24H: float = Field(..., ge=0, description="최근 24시간 거래량")
    acc_trade_value_24H: float = Field(..., ge=0, description="최근 24시간 거래금액")
    fluctate_24H: float = Field(..., description="최근 24시간 변동가")
    fluctate_rate_24H: float = Field(..., description="최근 24시간 변동률")
    date: int = Field(..., description="타임 스탬프")


class OrderbookEntry(BaseModel):
    price: float = Field(..., description="해당 가격에서의 매도 또는 매수 요청 가격")
    quantity: float = Field(..., description="해당 가격에서 거래 가능한 Currency 수량")

class OrderbookResponse(BaseModel):
    status: str = Field(..., description="결과 상태 코드 (0000: 정상, 그 외 에러 코드)")
    timestamp: int = Field(..., description="타임 스탬프")
    order_currency: str = Field(..., description="주문 통화 (코인)")
    payment_currency: str = Field(..., description="결제 통화 (마켓)")
    bids: list[OrderbookEntry] = Field(..., description="매수 요청 내역")
    asks: list[OrderbookEntry] = Field(..., description="매도 요청 내역")



class BalanceResponse(BaseModel):
    status: str = Field(..., description="결과 상태 코드 (0000: 정상, 그 외 에러 코드)")
    total_currency: Optional[float] = Field(None, description="전체 가상자산 수량")
    total_krw: Optional[float] = Field(None, description="전체 원화(KRW) 잔액")
    in_use_currency: Optional[float] = Field(None, description="주문 중 묶여있는 가상자산 수량")
    in_use_krw: Optional[float] = Field(None, description="주문 중 묶여있는 원화(KRW) 잔액")
    available_currency: Optional[float] = Field(None, description="주문 가능 가상자산 수량")
    available_krw: Optional[float] = Field(None, description="주문 가능 원화(KRW) 잔액")
    xcoin_last: Optional[float] = Field(None, description="마지막 체결된 거래 금액")

    @classmethod
    def from_api_response(cls, response: dict, currency: str):
        """
        빗썸 API 응답을 기반으로 BalanceResponse 모델 생성
        """
        currency = currency.lower()

        return cls(
            status=response.get("status", "error"),
            total_currency=float(response["data"].get(f"total_{currency}", 0)),
            total_krw=float(response["data"].get("total_krw", 0)),
            in_use_currency=float(response["data"].get(f"in_use_{currency}", 0)),
            in_use_krw=float(response["data"].get("in_use_krw", 0)),
            available_currency=float(response["data"].get(f"available_{currency}", 0)),
            available_krw=float(response["data"].get("available_krw", 0)),
            xcoin_last=float(response["data"].get(f"xcoin_last_{currency}", 0)),
        )
        




# 거래 유형 Enum
class TransactionType(int, Enum):
    ALL = 0            # 전체
    BUY = 1            # 매수 완료
    SELL = 2           # 매도 완료
    WITHDRAW_PENDING = 3  # 출금 중
    DEPOSIT = 4        # 입금
    WITHDRAW = 5       # 출금
    KRW_DEPOSIT_PENDING = 9  # KRW 입금 중


class TransactionRecord(BaseModel):
    search: TransactionType = Field(..., description="검색 구분 (거래 유형)")
    transfer_date: int = Field(..., description="거래 일시")
    order_currency: str = Field(..., description="주문 통화")
    payment_currency: str = Field(..., description="결제 통화")
    units: float = Field(..., description="거래 요청 수량", ge=0)
    price: float = Field(..., description="1 단위당 가격", ge=0)
    amount: float = Field(..., description="거래 총액", ge=0)
    fee_currency: str = Field(..., description="수수료 통화")
    fee: float = Field(..., description="거래 수수료", ge=0)
    order_balance: float = Field(..., description="주문 통화 잔액", ge=0)
    payment_balance: float = Field(..., description="결제 통화 잔액", ge=0)


class TransactionResponse(BaseModel):
    status: str = Field(..., description="결과 상태 코드")
    transactions: List[TransactionRecord] = Field(..., description="거래 내역 리스트")

    @classmethod
    def from_api_response(cls, response: dict) -> "TransactionResponse":
        """
        빗썸 API 응답을 기반으로 TransactionResponse 객체 생성
        """
        transactions = response.get("data", [])
        return cls(
            status=response["status"],
            transactions=[
                TransactionRecord(
                    search=TransactionType(int(tx["search"])),
                    transfer_date=int(tx["transfer_date"]),
                    order_currency=tx["order_currency"],
                    payment_currency=tx["payment_currency"],
                    units=float(tx["units"]),
                    price=float(tx["price"]),
                    amount=float(tx["amount"]),
                    fee_currency=tx["fee_currency"],
                    fee=float(tx["fee"]),
                    order_balance=float(tx["order_balance"]),
                    payment_balance=float(tx["payment_balance"]),
                )
                for tx in transactions
            ]
        )