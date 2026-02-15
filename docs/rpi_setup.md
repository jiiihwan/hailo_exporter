# 🍓 Raspberry Pi 5 설정 가이드 (Setup Guide)

[**English**](rpi_setup.en.md) | [**한국어**](rpi_setup.md)

이 문서는 Kubernetes 환경에서 Hailo Exporter를 구동하기 위해 Raspberry Pi 5를 설정하는 방법을 설명합니다.

---

## 🛠️ 1. SSH 설정 (SSH Settings)
라즈베리파이에 원격 접속하기 위해 SSH를 활성화합니다.

```bash
# 네트워크 인터페이스 확인
ifconfig
# net-tools가 없다면 설치: sudo apt install net-tools

# OpenSSH Server 설치
sudo apt-get install openssh-server

# 서비스 활성화 및 시작
sudo systemctl enable ssh
sudo systemctl start ssh
```

---

## ☸️ 2. Kubernetes 노드 설정 (K8s Settings)

### 2.1 cmdline.txt 수정 (cgroup 활성화)
K8s 노드로 참여(join)하기 위해 cgroup 설정을 추가해야 합니다.

```bash
sudo vim /boot/firmware/cmdline.txt
```

파일의 맨 끝에 다음 내용을 **공백으로 구분하여** 추가합니다 (줄바꿈 금지):
```text
rootwait quiet splash cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1
```

수정 후 재부팅합니다.
```bash
sudo reboot
```

### 2.2 Kubelet DNS 설정 (NotReady 문제 해결)
라즈베리파이(Debian Bookworm)에서 `kubelet`이 잘못된 `resolv.conf` 경로를 참조하여 노드가 `NotReady` 상태에 빠지거나 TLS 부트스트랩이 실패하는 문제를 해결합니다.

1.  **Kubelet 서비스 설정 디렉토리 생성**
    ```bash
    sudo mkdir -p /etc/systemd/system/kubelet.service.d
    ```

2.  **설정 파일 작성**
    ```bash
    sudo vim /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
    ```
    아래 내용을 붙여넣습니다.
    ```ini
    [Service]
    Environment="KUBELET_CONFIG_ARGS=--config=/var/lib/kubelet/config.yaml --resolv-conf=/etc/resolv.conf"
    Environment="KUBELET_KUBEADM_ARGS=--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf"
    ExecStart=
    ExecStart=/usr/bin/kubelet $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS
    ```

3.  **서비스 재시작**
    ```bash
    sudo systemctl daemon-reexec
    sudo systemctl daemon-reload
    sudo systemctl restart kubelet
    ```

---

## ⚡ 3. PCIe Gen 3.0 활성화 (PCIe Activation)
Hailo NPU의 성능을 최대로 끌어내기 위해 PCIe Gen 3.0 모드를 활성화합니다.
참고: [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#pcie-gen-3-0)

```bash
sudo raspi-config
```
1.  **Advanced Options** 선택
2.  **PCIe Speed** 선택
3.  **Yes**를 선택하여 PCIe Gen 3 mode 활성화
4.  **Finish**를 눌러 종료 및 재부팅 (`sudo reboot`)

---

## 📦 4. 필수 라이브러리 설치 (Install Libraries)
Hailo NPU를 사용하기 위한 드라이버와 라이브러리를 설치합니다.

```bash
# Hailo 전체 패키지 설치
sudo apt install hailo-all

# GStreamer 플러그인 설치 (예제 실행용)
sudo apt-get install gstreamer1.0-plugins-ugly

# 적용을 위해 재부팅
sudo reboot
```

설치가 완료되면 펌웨어 정보를 확인하여 정상 작동을 검증합니다.
```bash
hailortcli fw-control identify
```
