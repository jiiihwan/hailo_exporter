# 📝 Prepare for Exporter

- `hailortlci monitor` 가 어떻게 동작하는지 파악하여 사용량 메트릭 정보만 추출하는 exporter를 만드는 것이 목표
- referred to the following link:
  - https://github.com/hailo-ai/hailort/blob/master/hailort/hailortcli/mon_command.cpp
  - https://github.com/hailo-ai/hailort/blob/master/hailort/libhailort/scheduler_mon.proto

### Protobuf?
> Protobuf(Protocol Buffers) : Google에서 개발한 구조화된 데이터의 직렬화(Serialization) 포맷

`hailortcli` 의 사용량 정보는 protobuf를 사용한다.

#### 직렬화?
> 프로그램 내에서 사용하는 데이터를 네트워크 전송이나 파일 저장을 위해 바이너리 또는 텍스트 형식으로 변환하는 과정
### protoc?
> Protobuf에서 제공하는 "Protocol Buffer Compiler"

`.proto` 파일로 정의한 데이터 구조(스키마)를 각 언어별로 사용할 수 있는 코드(클래스, 모듈 등)로 자동 변환해주는 컴파일러

## hailortcli monitor의 진행 과정
1. `scheduler_mon.proto` 에서 `ProtoMon` 메시지 구조 정의
2. HailoRT 내부 스케줄러가 `.pb` 파일에 `ProtoMon` 메시지를 기록. 이때 기록되는 것은 HAILO_MONITOR=1 인 터미널의 경우만 기록됨.
3. `hailortcli monitor`에 출력되는 정보를 표시하기 위해 사용되는 `mon_command.cpp`는 그 `.pb` 파일을 열고, `ProtoMon`으로 파싱한 뒤, 그 안에 있는 정보 (`device_infos`, `network_infos`, `net_frames_infos`)를 터미널에 출력함
- 사용률은 이진파일(.pb)에 담겨있고, 이진파일을 해석하기 위한 것이 `scheduler_mon.proto`
- 그래서 `scheduler_mon.proto` 를 파이썬에서 사용하기 위해 proto 파일을 다른언어로 변환해주는 컴파일러인 `protoc` 를 설치한다

## 🔨 protoc 설치
### 공식 protobuf 컴파일러 설치
```bash
sudo apt install protobuf-compiler
```

### 확인
```bash
protoc --version
```

## 🌿 파이썬 가상환경 생성 
### 가상환경 생성
```bash
python3 -m venv venv
```

### 가상환경 활성화
```bash
source venv/bin/activate
```

### protobuf 설치
```bash
pip install protobuf
```

### (원하면) 비활성화
```
deactivate
```

## 🔄️ proto 파일 파이썬으로 변환

### hailort 파일 clone
```bash
git clone https://github.com/hailo-ai/hailort
cd hailort/hailort/libhailort
```
### .proto파일 파이썬에서 불러와서 이진파일에 담긴 정보를 읽을 수 있게 파일을 만들기
```bash
protoc --python_out=. scheduler_mon.proto
```

### 프로젝트 경로로 이동
```bash
mv scheduler_mon_pb2.py ~/hailo_exporter/
```
