import subprocess
import platform
from app.utils.logger import logger


def check_and_start_nginx():
    """Nginx 서버 실행 상태를 확인하고 필요 시 실행"""
    try:
        # 1️⃣ OS 확인
        os_name = platform.system()

        # 2️⃣ Nginx 상태 확인
        if os_name == "Windows":
            result = subprocess.run(["tasklist"], capture_output=True, text=True)
            nginx_running = "nginx.exe" in result.stdout
            nginx_start_command = ["nginx.exe"]

        else:
            result = subprocess.run(["pgrep", "nginx"], capture_output=True, text=True)
            nginx_running = bool(result.stdout.strip())
            nginx_start_command = ["sudo", "systemctl", "start", "nginx"]

        # 3️⃣ Nginx 상태에 따른 로직
        if nginx_running:
            logger.info("✅ Nginx 실행 중")
            return True
        else:
            logger.warning("⚠️ Nginx가 실행되지 않았습니다. 실행을 시도합니다...")

            # 4️⃣ Nginx 실행 시도
            try:
                start_result = subprocess.run(nginx_start_command, capture_output=True, text=True)
                
                if start_result.returncode == 0:
                    logger.info("✅ Nginx를 성공적으로 실행했습니다.")
                    return True
                else:
                    logger.error(f"❌ Nginx 실행 실패: {start_result.stderr}")
                    return False

            except Exception as start_err:
                logger.error(f"⚠️ Nginx 실행 중 오류 발생: {str(start_err)}")
                return False

    except Exception as e:
        logger.error(f"🚨 Nginx 상태 확인 중 오류 발생: {str(e)}")
        return False
