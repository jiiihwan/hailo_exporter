# Prepare for Exporter

- referred to the following link:
  - https://github.com/hailo-ai/hailort/blob/master/hailort/hailortcli/mon_command.cpp
  - https://github.com/hailo-ai/hailort/blob/master/hailort/libhailort/scheduler_mon.proto
 
## 설명

1. `scheduler_mon.proto` → `ProtoMon` 메시지 구조 정의
2. HailoRT 내부 스케줄러가 `.pb` 파일에 `ProtoMon` 메시지를 기록
3. `mon_command.cpp`는 그 `.pb` 파일을 열고, `ProtoMon`으로 파싱한 뒤, 그 안에 있는 정보 (`device_infos`, `network_infos`, `net_frames_infos`)를 터미널에 출력함
- 사용률은 이진파일인 .pb 파일에 담겨있고, 이진파일을 해석하기 위한 것이 `scheduler_mon.proto`
- `scheduler_mon.proto` 를 파이썬에서 사용하기 위해 proto 파일을 다른언어로 변환해주는 컴파일러인 `protoc` 를 설치한다

## protoc 설치
```
# 공식 protobuf 컴파일러 설치
sudo apt install protobuf-compiler

# 확인
protoc --version
```

## 파이썬 가상환경 생성
```
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# protobuf 설치
pip install protobuf

# (원하면) 비활성화
deactivate
```

## proto 파일 파이썬으로 변환
```
#hailort 파일 clone
git clone https://github.com/hailo-ai/hailort

cd hailort/hailort/libhailort

# .proto파일 파이썬에서 불러와서 이진파일에 담긴 정보를 읽을 수 있게 파일을 만들기
protoc --python_out=. scheduler_mon.proto

#프로젝트 경로로 이동
mv scheduler_mon_pb2.py ~/hailo_exporter/
```
