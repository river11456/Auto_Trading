import os
import signal
import psutil
from app.utils.logger import logger

def find_and_kill_process(port: int):
    """
    지정된 포트를 사용 중인 프로세스를 찾아 종료하는 함수.
    종료한 경우 True 반환, 종료할 프로세스가 없으면 False 반환.
    """
    process_found = False  # 프로세스 종료 여부

    # 모든 프로세스의 네트워크 연결 조회
    for conn in psutil.net_connections(kind="inet"):
        if conn.laddr.port == port:
            try:
                proc = psutil.Process(conn.pid)
                logger.info(f"⚠️ {port} 포트를 점유 중인 프로세스를 종료합니다: PID {proc.pid} ({proc.name()})")
                os.kill(proc.pid, signal.SIGTERM)  # 안전 종료
                process_found = True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    if process_found:
        logger.info(f"✅ {port} 포트 점유 프로세스를 정상적으로 종료했습니다. 서버를 재시작합니다.")
    else:
        logger.info(f"✅ {port} 포트를 사용하는 프로세스가 없습니다.")

    return process_found  # 종료 여부 반환
