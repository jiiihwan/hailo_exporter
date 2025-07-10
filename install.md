# 🛠️ Install hailo_exporter
설치만 하고자 한다면 아래의 과정을 따라하기만 하면 됨

## 🔨 0. hailo_exporter 바로 설치
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
