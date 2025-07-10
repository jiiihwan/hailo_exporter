# Building Hailo Exporter
- 폴더 구조 참고
```
hailo_exporter/                   # 최상위 폴더
├── Dockerfile                    # Docker 빌드 설정 파일
├── requirements.txt              # Python 의존성 목록
├── hailo_exporter.py             # exporter 코드
└── scheduler_mon_pb2.py          # protobuf 컴파일 결과 (scheduler_mon.proto → pb2)
```

## hailo_exporter

### `requirements.txt`
  - 프로젝트에서 사용하는 Python 패키지 목록
  - [requirements.txt](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/requirements.txt)

### `scheduler_mon_pb2.py`
  - scheduler_mon.proto를 protoc로 컴파일해서 생성된 Python 코드
  - [scheduler_mon_pb2.py](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/scheduler_mon_pb2.py)

### `exporter.py`
  - Prometheus exporter 클래스를 정의하고 Hailo 장치의 메트릭을 수집해 노출
  - [hailo_exporter.py](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/hailo_exporter.py)


## exporter 실행
- 가상환경 세팅
```
# (필요시) 원래 가상환경 삭제 및 설치
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

- exporter 실행해보기    
```
python hailo_exporter --port 9102
```
