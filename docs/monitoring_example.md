# 📊 모니터링 예제 가이드 (Monitoring Example)

[**English**](monitoring_example.en.md) | [**한국어**](monitoring_example.md)

이 문서는 Hailo Exporter가 정상적으로 메트릭을 수집하는지 확인하기 위해, NPU에 부하를 주는 예제 파이프라인을 실행하는 방법을 설명합니다.

참고 링크:
- [hailo-rpi5-examples](https://github.com/hailo-ai/hailo-rpi5-examples)
- [DataRoot Labs Blog](https://datarootlabs.com/blog/hailo-ai-kit-raspberry-pi-5-setup-and-computer-vision-pipelines)

---

## ⚙️ 1. 예제 다운로드 및 설정 (Initial Setting)

Hailo 공식에서 제공하는 예제 레포지토리를 클론하고 환경을 설정합니다.

```bash
# 레포지토리 클론
git clone https://github.com/hailo-ai/hailo-rpi5-examples.git
cd hailo-rpi5-examples

# 설치 스크립트 실행
./install.sh

# 리소스 다운로드 (모델 파일 등)
./download_resources.sh
```

---

## 🖥️ 2. 실행 환경 설정 (Environment Setup)

예제를 실행하기 전, 환경 변수를 설정해야 합니다.

```bash
cd hailo-rpi5-examples

# 가상환경 및 라이브러리 로드
source setup_env.sh 

# 디스플레이 설정 (SSH 접속 시 필수)
# 실제 연결된 모니터가 있다면 :0, 없다면 X11 Forwarding 등을 고려해야 함
export DISPLAY=:0 

# 모니터링 활성화 (중요!)
# 이 환경변수가 설정되어야 NPU 사용량이 기록되어 Exporter가 수집할 수 있습니다.
export HAILO_MONITOR=1
```

---

## ✔️ 3. 예제 실행 (Generate Load)
NPU를 사용하는 객체 탐지(Detection) 파이프라인을 실행합니다. 이 코드가 실행되는 동안 NPU 부하가 발생합니다.

```bash
python basic_pipelines/detection.py
```

---

## 📈 4. 모니터링 확인 (Check Metrics)

### 4.1 CLI로 확인
새로운 터미널을 열고 다음 명령어를 입력하면 실시간 사용량을 확인할 수 있습니다.

```bash
hailortcli monitor 
```

### 4.2 Prometheus/Grafana 확인
Hailo Exporter가 설치되어 있다면, Grafana 대시보드에서 `hailo_NPU_utilization` 메트릭이 상승하는 그래프를 볼 수 있어야 합니다.
