# 🍓 Hailo Exporter

[**English**](README.en.md) | [**한국어**](README.md)

> Kubernetes 환경의 Raspberry Pi 5에서 Hailo NPU 사용량을 모니터링하기 위한 Prometheus Exporter

**Hailo Exporter**는 [k8s dashboard](https://github.com/jiiihwan/k8s-dashboard)프로젝트의 확장 기능으로, [jetson-exporter](https://github.com/jiiihwan/jetson_exporter)의 아키텍처를 기반으로 제작되었습니다.

기존의 `hailortcli monitor` 명령어를 외부 프로세스로 실행하여 데이터를 수집하는 방식 대신, HailoRT의 내부 동작 방식을 분석하여 NPU 사용률 정보가 담긴 바이너리 파일을 실시간으로 파싱하는 독자적인 수집 구조를 개발했습니다. 이를 통해 오버헤드를 낮추고 Prometheus 환경에 최적화된 안정적인 성능을 보장합니다.



---

## 📖 소개 (Introduction)

이 Exporter는 Raspberry Pi 5에 연결된 **Hailo-8 / Hailo-8L NPU**의 실시간 사용률(Utilization)을 수집하여 Prometheus로 내보냅니다.

### 동작 원리 (How it Works)
1.  **Protobuf 파싱**: `/tmp/hmon_files` 디렉토리에 생성되는 바이너리 로그 파일을 읽습니다.
2.  **데이터 추출**: Google Protocol Buffers(`scheduler_mon.proto`)를 사용하여 바이너리를 파싱하고 NPU 사용률 정보를 추출합니다.
3.  **Prometheus 노출**: 추출된 데이터를 `hailo_NPU_utilization` 메트릭으로 변환하여 HTTP 서버(기본 포트 9102)를 통해 노출합니다.

> 더 자세한 기술적 내용은 [**내부 동작 원리 (Internal Details)**](docs/internal_details.md) 문서를 참고하세요.

### 수집 데이터 (Collected Metrics)
- `hailo_NPU_utilization`: Hailo NPU의 현재 사용률 (%)

---

## 📦 설치 및 배포 (Installation & Deployment)

### 1. 사전 준비 (Prerequisites)
이 프로젝트는 **Raspberry Pi 5**와 **Kubernetes** 환경을 전제로 합니다.
아직 환경 설정이 되지 않았다면 [**Raspberry Pi 5 설정 가이드 (Setup Guide)**](docs/rpi_setup.md)를 먼저 진행해 주세요.

- PCIe Gen 3.0 활성화
- Hailo 라이브러리 및 드라이버 설치 (`hailo-all`)

### 2. 레포지토리 클론
마스터 노드에서 다음 명령어를 실행합니다.

```bash
git clone https://github.com/jiiihwan/hailo_exporter
cd hailo_exporter
```

### 3. 노드 라벨링 (Node Labeling)
Hailo NPU가 장착된 라즈베리파이 노드에 `device=rpi` 라벨을 추가해야 DaemonSet이 올바르게 배포됩니다.

```bash
# 노드 목록 확인
kubectl get nodes --show-labels

# 라벨 추가 (워커 노드 이름이 rpi-node인 경우)
kubectl label nodes [rpi-node-name] device=rpi
```

### 4. 리소스 적용 (Apply Resources)
DaemonSet, Service, ServiceMonitor를 배포합니다.

```bash
cd k8s_resources

# DaemonSet 배포
kubectl apply -f hailo-exporter-daemonset.yaml

# Service & ServiceMonitor 배포 (모니터링 네임스페이스)
kubectl apply -f hailo-exporter-service.yaml -n monitoring
kubectl apply -f hailo-exporter-servicemonitor.yaml -n monitoring
```

> **직접 이미지를 빌드하려면?** [**빌드 가이드 (BUILD.md)**](BUILD.md)를 참고하세요.

---

## 📊 모니터링 검증 (Verification)

설치가 완료되면 실제로 NPU에 부하를 주어 메트릭이 수집되는지 확인할 수 있습니다.
NPU 부하 생성 및 모니터링 확인 방법은 [**모니터링 예제 가이드 (Monitoring Example)**](docs/monitoring_example.md)를 참고하세요.
