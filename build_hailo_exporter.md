# Building Hailo Exporter
- 폴더 구조 참고
```
hailo_exporter/                   # 최상위 폴더
├── Dockerfile                    # Docker 빌드 설정 파일
├── requirements.txt              # Python 의존성 목록
├── hailo_exporter.py             # exporter 코드
└──scheduler_mon_pb2.py           # protobuf 컴파일 결과 (scheduler_mon.proto → pb2)
```

## hailo_exporter module

- ### `requirements.txt`
  - 프로젝트에서 사용하는 Python 패키지 목록
  - [requirements.txt](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/requirements.txt)

- ### `scheduler_mon_pb2.py`
  - scheduler_mon.proto를 protoc로 컴파일해서 생성된 Python 코드
  - [scheduler_mon_pb2.py](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/hailo_exporter/scheduler_mon_pb2.py)

- ### `__init__.py`
  - 이 디렉토리를 Python 패키지로 인식시키기 위한 파일
  - [__init__.py](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/hailo_exporter/__init__.py)

- ### `__main__.py`
  - 모듈로 실행시 진입점. HTTP 서버를 시작하고, Prometheus exporter 등록 후 루프 실행
  - [__main__.py](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/hailo_exporter/__main__.py)

- ### `exporter.py`
  - Prometheus exporter 클래스를 정의하고 Hailo 장치의 메트릭을 수집해 노출
  - [exporter.py](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/hailo_exporter/exporter.py)

- ### `hailo_stats.py`
  - /tmp/hmon_files에 저장된 .pb 파일을 열고 scheduler_mon_pb2를 통해 Hailo 사용률 정보를 추출하는 기능
  - [hailo_stats.py](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/hailo_exporter/hailo_stats.py)

- ### `logger.py `
  - 로그 출력 담당
  - [logger.py](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/hailo_exporter/logger.py)

## exporter 실행
- 가상환경 세팅
```
# (필요시) 원래 가상환경 삭제
deactivate
rm -rf venv

sudo apt update
sudo apt install python3-venv python3-pip

#가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

#pip 업그레이드!
python -m pip install --upgrade pip

#필요 패키지 설치
pip install -r requirements.txt
```

- exporter 모듈 실행해보기    
    - 모듈이 들어있는 폴더명이 hailo_exporter 이고 다음 명령어를 폴더 밖에서 실행 
```
python -m hailo_exporter --port 9101
```
