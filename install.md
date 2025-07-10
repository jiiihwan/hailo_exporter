# 🛠️ Install hailo_exporter
설치만 하고자 한다면 아래의 과정을 따라하기만 하면 됨

## 0. hailo_exporter 바로 설치
### git clone
마스터노드에서 입력
```bash
git clone https://github.com/jiiihwan/hailo_exporter
```

### 모두 적용
```bash
cd hailo_exporter/k8s_resources
```

```bash
kubectl apply -f hailo-exporter-daemonset.yaml
kubectl apply -f hailo-exporter-service.yaml -n monitoring
kubectl apply -f hailo-exporter-servicemonitor.yaml -n monitoring
```


## 설명
### `requirements.txt`
  - 프로젝트에서 사용하는 Python 패키지 목록
  - [requirements.txt](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/requirements.txt)

### `scheduler_mon_pb2.py`
  - scheduler_mon.proto를 protoc로 컴파일해서 생성된 Python 코드
  - [scheduler_mon_pb2.py](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/scheduler_mon_pb2.py)

### `exporter.py`
  - Prometheus exporter 클래스를 정의하고 Hailo 장치의 메트릭을 수집해 노출
  - [hailo_exporter.py](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/hailo_exporter.py)

