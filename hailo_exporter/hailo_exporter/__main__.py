from time import sleep
import argparse

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from .exporter import HailoExporter
from .logger import factory


def start_exporter(port=9100, update_period=1):
    # 로거 초기화
    logger = factory(__name__)
    logger.info(f"Hailo exporter running on port {port}. Querying speed: {update_period}s")
    
    # Prometheus HTTP 서버 시작
    start_http_server(port)
    
    # Hailo 익스포터 인스턴스 생성
    data_collector = HailoExporter(update_period)

    # 초기 데이터 수집을 위한 대기
    sleep(update_period * 2)
    
    # 익스포터를 Prometheus 레지스트리에 등록
    REGISTRY.register(data_collector)
    
    # 메인 루프
    while True:
        sleep(1)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, nargs='?', default=9100, help='Exporter port')
    parser.add_argument('--update_period', type=int, nargs='?', default=1, help='Querying speed')
    return vars(parser.parse_args())


if __name__ == '__main__':
    start_exporter(**cli())
