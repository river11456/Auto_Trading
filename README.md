🚀 Automated Crypto Trading Backend

이 프로젝트는 TradingView 웹훅 기반 자동 암호화폐 거래 시스템의 백엔드입니다.FastAPI, Bithumb API, Rich 로그 시스템을 활용하여 실시간 거래를 수행할 수 있도록 설계되었습니다.

📌 Features

자동 매매: TradingView 웹훅을 수신하여 자동으로 매수/매도 주문 실행

Bithumb API 연동: 실시간 시세 조회 및 주문 처리

전략 기반 거래: 현재 TradingView 알러트 기반 전략만 구현   

FastAPI 기반 서버: 비동기 API 서버로 높은 성능 제공

커스텀 로깅 시스템: Rich를 활용한 가독성 높은 로그 출력 및 파일 기록






🛠 Installation

1. Clone Repository

TBD

2. Create Virtual Environment & Install Dependencies

TBD


3. Set Up Environment Variables

.env 파일을 생성하고 다음과 같은 환경 변수를 설정합니다.

# 빗썸 API 키 설정
BITHUMB_API_KEY=your_api_key_here
BITHUMB_SECRET=your_api_secret_here


# 서버 환경 설정
ENV=development   (이건 아직 의미 없음)



🚀 How to Run

1. Start the Server

python main.py


* DDNS 설정, 포트 포워딩 설정, Nginx (리버스 프록시) 설정 필요함

DDNS : 
동적 DNS 서비스
일반 가정에서 쓰는 공인 아이피는 주기적으로 변함
DDNS 서비스 사용하면 주기적으로 변하는 내 아이피를 특정 도메인에 고정해줌
트레이딩뷰 알러트를 그 도메인으로 보내야함 

아이피 타임 사용하면 아이피 타임 DDNS 설정 검색 ㄱㄱ


포트 포워딩 :
TBD  

이것도 아이피 타임 설정에서 가능  
웹훅과 내 서버의 문을 연결 해주는 역할  


Nginx :
리버스 프록시 프로그램
이걸 써야 내 로컬 서버를 안전하게 외부에 오픈 가능



* 서버로 윈도우 PC 사용하려면 자동 절전 기능도 꺼야 함!
절전이어도 네트워크 연결 되긴 하는데,
절전모드 진입하는 타이밍이랑 알러트 수신되는 타이밍이 같으면 일시적으로 놓침






2. API Documentation

빗썸 Api 1.2.0 사용
빗썸 Api 2.0은 특정 ip를 등록해야 하기 때문에 주기적으로 바뀐다
1.0은 ip 제한이 없다

https://apidocs.bithumb.com/v1.2.0/




📁 Project Structure

backend/
│── app/
│   ├── config/              # 설정 관련 파일
│   │   ├── config.py
│   ├── exceptions/          # 예외 처리 모듈
│   │   ├── custom_exceptions.py
│   │   ├── exception_handler.py
│   ├── models/              # Pydantic 데이터 모델
│   │   ├── trading_model.py
│   ├── routes/              # API 라우트
│   │   ├── webhook_route.py
│   ├── services/            # 핵심 서비스 로직
│   │   ├── bithumb_api_client.py
│   │   ├── strategy_service.py
│   │   ├── trading_service.py
│   ├── utils/               # 유틸리티 함수 (로깅, 프로세스 관리 등)
│   │   ├── display.py
│   │   ├── logger.py
│   │   ├── nginx_checker.py
│   │   ├── process_checker.py
│── logs/                    # 로그 파일 저장
│── main.py                   # FastAPI 서버 실행 파일
│── test_bithumb_api.py       # Bithumb API 테스트 코드
│── test_display.py           # 로그 디스플레이 테스트
│── test_exceptions.py        # 예외 처리 테스트
│── test_trading_model.py     # 데이터 모델 테스트
│── test_trading_service.py   # 트레이딩 서비스 테스트
│── .env                      # 환경 변수 파일
│── requirements.txt          # Python 패키지 목록
│── README.md                 # 프로젝트 문서


* 테스트 코드들은 위치 이동 필요



🔍 주요 기능

1. 웹훅 기반 자동 거래

TradingView에서 보낸 웹훅을 수신하여 자동으로 매매를 수행합니다.

{
  "signal": "buy",
  "symbol": "USDT",
  "amount": 100.0     
}

이를 FastAPI 라우트(/webhook)에서 처리하며, 전략 실행 후 매매를 결정합니다.


* 여기서 말하는 전략이란?

사실 진짜 전략은 트레이딩뷰에서 관리된다
난 트레이딩뷰 알러트를 Only 매수/매도 신호로 활용한다
그래서 매수 신호가 왔을 때 실제 매수를 실행할지, 얼마를 살지 등을 정해줘야 한다
결국 최종 주문 실행을 결정하는 부분이 필요한데 이를 strategy_service 로 구분했다

웹훅 신호 -> Strategy 에서 최종 결정 -> Trading 에서 실제 거래 진행 

Strategy : strategy_service.py
Trading : trading_service.py

그리고 이 두 모듈은 bithumb_api_client.py 에서 Api를 이용한다


* 만약 파이썬 코드로 트레이딩뷰를 대체할 수 있다면 strategy_service를 진짜 전략으로 확장해서 사용 가능하다 (이건 나중에)  



2. 로그 시스템

Rich 콘솔 로그: 컬러 출력 및 JSON 데이터 가독성 향상

파일 로그 기록: logs/app.log에 저장

커스텀 로그 핸들러: ConsoleHandlerWithDisplay를 통해 터미널과 파일 로그를 분리





3. 예외 처리

모든 API 요청과 내부 프로세스에서 발생하는 예외를 핸들링합니다.

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"요청 데이터 검증 실패: {exc.errors()}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

