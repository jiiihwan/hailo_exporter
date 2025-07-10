# Automate Hailo_exporter in k8s cluster
jetson exporter와 마찬가지로 daemonset을 이용한 자동배포 구현

`9100`포트는 `node-exporter`, `9102`포트를 `hailo-exporter`로 사용

`jetson-exporter`와 다른기기니 `9101`포트를 사용해도 무방함

## 🏷️ 1. 노드에 라벨 붙히기
`device=rpi`라는 라벨을 붙히고, 이 라벨을 기준으로 `daemonset`이 exporter pod를 배포한다

```bash
kubectl get nodes
```
마스터노드에서

```
kubectl label node <node name> device=rpi
```
라벨 `device=rpi` 붙히기

```
kubectl get nodes --show-labels
```
라벨 확인

## 📄 2. Dockerfile 생성

```
vim Dockerfile
```

[Dockerfile](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/Dockerfile)

## 🛠️ 3. nerdctl 및 buildkit 설치
- k8s가 docker가 아닌 containerd를 사용하고 있기 때문에 docker말고 nerdctl을 사용한다

```bash
mkdir nerdctl
cd nerdctl
#nerdctl 설치
curl -s https://api.github.com/repos/containerd/nerdctl/releases/latest \
| grep "browser_download_url.*linux-arm64.tar.gz" \
| cut -d '"' -f 4 \
| wget -i -
#압축해제 (버전에 따라 명령어 수정) 
tar xzvf nerdctl-full-2.0.4-linux-arm64.tar.gz
#buildkit 포함 nerdctl 설치
sudo cp bin/nerdctl /usr/local/bin/
sudo cp bin/buildctl /usr/local/bin/
sudo cp bin/buildkitd /usr/local/bin/
#버전 확인
nerdctl --version

#buildkitd 실행
sudo nohup buildkitd > /dev/null 2>&1 &
```

## 🐋 4. 이미지 build & push
```
#Dockerhub login
sudo nerdctl login

#dockerfile 빌드
cd ~/hailo_exporter/
sudo nerdctl build -t <your dockerhub> .

#도커허브에 푸시
sudo nerdctl push <your dockerhub>
```

## 🔋 5. k8s resource 파일 작성
### 동작 방식
- 라벨을 이용해서 daemonset, service, service monitor가 target을 찾을 수 있게 한다

| 리소스              | 라벨                                     | 라벨 용도                             |
|---------------------|--------------------------------------------------|----------------------------------------|
| `Pod` (DaemonSet)   | `app: hailo-exporter`                            | Service가 Pod 선택하는 기준           |
| `Service`           | `app: hailo-exporter`, `release: prometheus`     | ServiceMonitor가 Service 찾는 기준    |
| `ServiceMonitor`    | `release: prometheus`                            | Prometheus가 ServiceMonitor 찾는 기준 |


### 5.1. Daemonset 
/tmp/hmon_files를 마운트하는데, hailo model을 한번도 실행한 적이 없거나 일정시간이 지나면 존재하지 않는 휘발성 경로이므로 미리 생성해서 마운트한다.

root권한으로 생성되므로 chmod 777로 권한부여했다. 혹여나 권한 관련문제 때문에 바꾸고 싶으면 적절히 조정하면 된다.

```
vim hailo-exporter-daemonset.yaml
```

See [hailo-exporter-daemonset.yaml](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/k8s_resources/hailo-exporter-daemonset.yaml) for full code

```bash
kubectl apply -f hailo-exporter-daemonset.yaml
kubectl get pods -n monitoring -o wide
```

### 5.2. Service
```
vim hailo-exporter-service.yaml
```

[hailo-exporter-service.yaml](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/k8s_resources/hailo-exporter-service.yaml) for full code

```
kubectl apply -f hailo-exporter-service.yaml
```

### 5.3. Service Monitor
`vim hailo-exporter-servicemonitor.yaml`

[hailo-exporter-servicemonitor.yaml](https://github.com/jiiihwan/hailo_exporter/blob/main/hailo_exporter/k8s_resources/hailo-exporter-servicemonitor.yaml) for full code

```
kubectl apply -f hailo-exporter-servicemonitor.yaml
```
