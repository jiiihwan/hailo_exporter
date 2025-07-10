FROM python:3.11-slim

WORKDIR /app/hailo_exporter

# 필수 패키지 설치
RUN apt-get update

# requirements.txt  복사 + 설치
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# 파이썬 소스 파일 복사
COPY hailo_exporter.py .
COPY scheduler_mon_pb2.py .

# Prometheus가 수집할 포트 열기
EXPOSE 9102

# 모듈로 실행
ENTRYPOINT ["python", "hailo_exporter.py", "--port=9102"]
