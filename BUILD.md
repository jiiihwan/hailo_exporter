# 🏗️ 빌드 가이드 (Build Guide)

[**English**](BUILD.en.md) | [**한국어**](BUILD.md)

이 문서는 **Hailo Exporter**의 도커 이미지를 직접 빌드하고 배포하는 방법을 설명합니다.
Raspberry Pi 5 환경(Linux/arm64)을 기준으로 작성되었습니다.

---

## 🛠️ 사전 준비 (Prerequisites)

Kubernetes가 Docker 대신 `containerd`를 사용하는 경우, 이미지 빌드를 위해 `nerdctl`이 필요합니다.

### nerdctl 및 buildkit 설치
1.  **설치 디렉토리 생성 및 이동**
    ```bash
    mkdir nerdctl && cd nerdctl
    ```

2.  **nerdctl 다운로드 및 설치**
    ```bash
    # 최신 버전 URL 확인 및 다운로드 (arm64)
    curl -s https://api.github.com/repos/containerd/nerdctl/releases/latest \
    | grep "browser_download_url.*linux-arm64.tar.gz" \
    | cut -d '"' -f 4 \
    | wget -i -

    # 압축 해제 (파일명은 버전에 따라 다를 수 있음)
    tar xzvf nerdctl-full-*-linux-arm64.tar.gz

    # 실행 파일 이동 (nerdctl, buildctl, buildkitd)
    sudo cp bin/nerdctl /usr/local/bin/
    sudo cp bin/buildctl /usr/local/bin/
    sudo cp bin/buildkitd /usr/local/bin/
    ```

3.  **설치 확인 및 데몬 실행**
    ```bash
    nerdctl --version
    
    # buildkitd 백그라운드 실행
    sudo nohup buildkitd > /dev/null 2>&1 &
    ```

---

## 🐳 이미지 빌드 및 푸시 (Build & Push)

### 1. Dockerfile 확인
프로젝트 루트에 포함된 `Dockerfile`을 사용합니다.
(기본적으로 Python 환경에서 `protobuf`, `prometheus_client` 등을 설치하도록 구성되어 있습니다.)

### 2. Docker Hub 로그인
```bash
sudo nerdctl login
```

### 3. 이미지 빌드
```bash
cd ~/hailo_exporter/
# <your dockerhub> 부분을 본인의 ID로 변경하세요.
sudo nerdctl build -t <your-dockerhub-id>/hailo_exporter:latest .
```

### 4. 이미지 푸시
```bash
sudo nerdctl push <your-dockerhub-id>/hailo_exporter:latest
```

---

## 📦 Protobuf 수동 컴파일 (Optional)
**참고**: 레포지토리에는 이미 컴파일된 `scheduler_mon_pb2.py` 파일이 포함되어 있으므로, 일반적인 경우에는 이 과정이 필요하지 않습니다.
동작 원리나 상세 내용은 [**내부 동작 원리 (Internal Details)**](docs/internal_details.md) 문서를 참고하세요.

만약 `scheduler_mon.proto`가 업데이트되어 다시 컴파일해야 하는 경우:

```bash
# 1. 컴파일러 설치
sudo apt install protobuf-compiler
pip install protobuf

# 2. 소스 다운로드 및 컴파일
git clone https://github.com/hailo-ai/hailort
cd hailort/hailort/libhailort
protoc --python_out=. scheduler_mon.proto

# 3. 결과물 이동
mv scheduler_mon_pb2.py ~/hailo_exporter/
```
