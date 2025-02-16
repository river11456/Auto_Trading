from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
from app.models.trading_model import (
    TradeRequest, TradeResponse, TransactionResponse, BalanceResponse
)
console = Console()


def display_trade_request(trade_request: TradeRequest):
    """
    Rich 라이브러리를 사용하여 TradeRequest 데이터를 보기 좋게 출력하는 함수.

    Args:
        trade_request (TradeRequest): 거래 요청 데이터 (Pydantic 모델)
    """

    # 테이블 생성
    table = Table(title="📜 거래 요청 정보", show_header=True, header_style="bold cyan")
    table.add_column("항목", style="dim", justify="left")
    table.add_column("값", justify="right")

    # 데이터 추가
    table.add_row("신호 (Signal)", trade_request.signal.value)
    table.add_row("심볼 (Symbol)", trade_request.symbol)
    table.add_row("거래 수량 (Amount)", str(trade_request.amount) if trade_request.amount else "-")

    # 출력
    console.print(table)


def display_trade_response(trade_response: TradeResponse):
    """
    Rich 라이브러리를 사용하여 TradeResponse 데이터를 보기 좋게 출력하는 함수.

    Args:
        trade_response (TradeResponse): 거래 응답 데이터 (Pydantic 모델)
    """
    console = Console()

    # 테이블 생성
    table = Table(title="📊 거래 응답 정보", show_header=True, header_style="bold green")
    table.add_column("항목", style="dim", justify="left")
    table.add_column("값", justify="right")

    # 데이터 추가
    table.add_row("상태 (Status)", trade_response.status)
    table.add_row("메시지 (Message)", trade_response.message)
    table.add_row("주문 ID (Order ID)", trade_response.order_id if trade_response.order_id else "-")
    table.add_row("체결 수량 (Filled Quantity)", f"{trade_response.filled_quantity:.8f}")
    table.add_row("평균 체결 가격 (Avg Price)", f"{trade_response.avg_price:.2f} KRW")
    table.add_row("거래 수수료 (Fee)", f"{trade_response.fee:.2f} KRW")
    table.add_row("최종 정산 금액 (Net Settlement)", f"{trade_response.net_settlement:.0f} KRW")

    # 출력
    console.print(table)








def print_transaction_history(response: TransactionResponse):
    """
    거래 내역을 보기 좋게 출력하는 함수 (rich 라이브러리 활용)
    """
    table = Table(title="📊 거래 내역", show_lines=True)

    # 테이블 헤더 추가
    table.add_column("거래 일시", justify="center", style="cyan", no_wrap=True)
    table.add_column("주문 통화", style="magenta")
    table.add_column("결제 통화", style="magenta")
    table.add_column("거래 유형", style="yellow")
    table.add_column("수량", justify="right", style="green")
    table.add_column("가격", justify="right", style="green")
    table.add_column("총액", justify="right", style="red")
    table.add_column("수수료", justify="right", style="blue")
    table.add_column("주문 잔액", justify="right", style="white")
    table.add_column("결제 잔액", justify="right", style="white")

    # 데이터 삽입 (최신순 정렬)
    for tx in sorted(response.transactions, key=lambda x: x.transfer_date, reverse=True):
        formatted_date = datetime.fromtimestamp(tx.transfer_date / 1_000_000).strftime("%Y-%m-%d %H:%M:%S")
        
        table.add_row(
            formatted_date,  
            tx.order_currency,  
            tx.payment_currency,  
            tx.search.name,  # 거래 유형 (Enum 사용)
            f"{tx.units:.4f}",  
            f"{tx.price:,.2f}",  
            f"{tx.amount:,.2f}",  
            f"{tx.fee:,.2f}",  
            f"{tx.order_balance:,.2f}",  
            f"{tx.payment_balance:,.2f}"
        )

    # 테이블 출력
    console.print(table)




def print_balance_info(symbol: str, balance: BalanceResponse):
    """
    Rich 라이브러리를 이용하여 BalanceResponse 데이터를 보기 좋게 출력하는 함수
    """

    # 코인 단위 설정
    unit = f"{symbol.upper()}"  # 코인 단위 (예: usdt, btc, eth)
    krw_unit = "KRW"  # 원화(KRW) 단위

    # 원화 값은 소수점 1자리에서 반올림
    def format_krw(value):
        return f"{round(value):,.1f}" if value is not None else "-"

    # 코인 값은 소수점 8자리 표시
    def format_crypto(value):
        return f"{value:,.8f}" if value is not None else "-"

    # 테이블 생성
    table = Table(title=f"💰 {symbol.upper()} 계좌 잔액 정보", show_header=True, header_style="bold cyan")
    table.add_column("항목", style="dim", justify="right")
    table.add_column("값", justify="right")  # 값 오른쪽 정렬
    table.add_column("단위", justify="left")  # 단위 왼쪽 정렬

    # 데이터 추가
    table.add_row("총 코인 수량", format_crypto(balance.total_currency), unit)
    table.add_row("총 원화 잔액", format_krw(balance.total_krw), krw_unit)
    table.add_row("주문 중 코인 수량", format_crypto(balance.in_use_currency), unit)
    table.add_row("주문 중 원화 잔액", format_krw(balance.in_use_krw), krw_unit)
    table.add_row("사용 가능 코인 수량", format_crypto(balance.available_currency), unit)
    table.add_row("사용 가능 원화 잔액", format_krw(balance.available_krw), krw_unit)
    table.add_row("최근 체결 가격", format_krw(balance.xcoin_last), krw_unit)

    # 패널로 출력
    panel = Panel(table, title="[bold magenta]📊 Balance Overview", expand=False)
    console.print(panel)