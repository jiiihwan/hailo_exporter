# 🧠 Hailo Exporter Internal Details

이 문서는 **Hailo Exporter** 개발을 위해 분석된 `hailortcli monitor`의 동작 원리와 Protobuf 데이터 구조에 대해 설명합니다.

## 🎯 목표
`hailortcli monitor` 명령어가 NPU 사용량 정보를 어떻게 가져오는지 파악하고, 이를 에뮬레이션하여 Prometheus 메트릭(`hailo_NPU_utilization`)으로 추출하는 Exporter를 구현합니다.

### 참고 자료
- [hailortcli/mon_command.cpp](https://github.com/hailo-ai/hailort/blob/master/hailort/hailortcli/mon_command.cpp)
- [libhailort/scheduler_mon.proto](https://github.com/hailo-ai/hailort/blob/master/hailort/libhailort/scheduler_mon.proto)

---

## 🏗️ 동작 원리 (How it Works)

### 1. Protobuf란?
> **Protobuf (Protocol Buffers)**: Google에서 개발한 구조화된 데이터의 직렬화(Serialization) 포맷

`hailortcli`는 사용량 정보를 **Protobuf** 메시지 형태로 처리합니다.

- **직렬화 (Serialization)**: 메모리 상의 객체 데이터를 파일 저장이나 네트워크 전송을 위해 바이너리 스트림으로 변환하는 과정.
- **protoc**: `.proto` 파일(스키마)을 파싱하여 각 언어(C++, Python 등)에서 사용할 수 있는 코드로 변환해주는 컴파일러.

### 2. hailortcli monitor 실행 흐름
1.  **메시지 정의**: `scheduler_mon.proto` 파일에 `ProtoMon` 메시지 구조가 정의되어 있습니다.
2.  **데이터 기록**: HailoRT 내부 스케줄러가 NPU 상태 정보를 담은 `ProtoMon` 메시지를 `.pb` (바이너리) 파일로 기록합니다. (단, `HAILO_MONITOR=1` 환경 변수가 설정된 터미널에서 실행될 때만 기록됨)
3.  **데이터 읽기**: `hailortcli monitor` 명령어는 이 `.pb` 파일을 읽고 파싱하여 터미널에 `device_infos`, `network_infos` 등을 출력합니다.

### 3. Exporter 구현 전략
`hailo_exporter`는 위 과정을 파이썬으로 구현하여 데이터를 수집합니다.

1.  공식 `scheduler_mon.proto` 파일을 가져옵니다.
2.  `protoc`를 사용하여 이를 파이썬 모듈(`scheduler_mon_pb2.py`)로 컴파일합니다.
3.  Exporter가 주기적으로 `.pb` 파일을 읽어 `ProtoMon` 객체로 역직렬화(Deserialization)합니다.
4.  객체에서 `utilization` 필드 값을 추출하여 Prometheus 메트릭으로 노출합니다.

---

## 🔧 Protobuf 컴파일 과정 (참고)
Exporter 개발 시 수행했던 Protobuf 컴파일 과정입니다. (현재는 이미 변환된 파일이 포함되어 있어 수행할 필요 없음)

### 1. 환경 설정
```bash
# Protobuf 컴파일러 설치
sudo apt install protobuf-compiler

# 파이썬 라이브러리 설치
pip install protobuf
```

### 2. .proto 파일 변환
```bash
# HailoRT 소스 다운로드
git clone https://github.com/hailo-ai/hailort
cd hailort/hailort/libhailort

# Python 코드로 변환
protoc --python_out=. scheduler_mon.proto

# 생성된 파일을 프로젝트로 이동
mv scheduler_mon_pb2.py ~/hailo_exporter/
```
