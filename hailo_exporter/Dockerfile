FROM python:3.11-slim

WORKDIR /app/hailo_exporter

# 필수 패키지 설치
RUN apt-get update

# requirements.txt  복사 + 설치
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# hailo_exporter 모듈 전체 복사
COPY hailo_exporter/ ./hailo_exporter/

# Prometheus가 수집할 포트 열기
EXPOSE 9101

# 모듈로 실행
ENTRYPOINT ["python", "-m", "hailo_exporter", "--port=9101"]
