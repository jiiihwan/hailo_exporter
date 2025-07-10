# 🍓 Raspberry pi installation in k8s

### ⚙️ SSH settings

```bash
ifconfig
sudo apt install net-tools
ifconfig
sudo apt-get install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
```

### ⚙️ k8s settings
join 안되는 문제 수정
```bash
sudo vim /boot/firmware/cmdline.txt
```

#### 열어서 이 내용 추가(공백으로 구분)
```
rootwait quiet splash cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1
```

```
sudo reboot
```

### ✔️ rpi Not ready 문제 수정
기본적으로 kubelet은 --resolv-conf 경로를 사용해 각 Pod에 DNS 설정을 넘겨주는데,
라즈베리파이 (Debian Bookworm) 등에서는 /run/systemd/resolve/resolv.conf가 존재하지 않을 수 있음

#### kubelet 설정에 올바른 DNS 경로 지정
```bash
sudo mkdir -p /etc/systemd/system/kubelet.service.d
sudo vim /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
```

```
Environment="KUBELET_CONFIG_ARGS=--config=/var/lib/kubelet/config.yaml --resolv-conf=/etc/resolv.conf"
Environment="KUBELET_KUBEADM_ARGS=--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf"
ExecStart=
ExecStart=/usr/bin/kubelet $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS
```

위 내용 넣고 저장

#### systemd 재로드 및 kubelet 재시작

```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

### ✅ PCIe Gen 3.0 활성화
referred to the following link: https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#pcie-gen-3-0

```
sudo raspi-config
```
1. Select Advanced Options.
2. Select PCIe Speed.
3. Choose Yes to enable PCIe Gen 3 mode.
4. Select Finish to exit.
5. Reboot your Raspberry Pi with sudo reboot for your changes to take effect.

### 🛠️ install libraries
```
sudo apt install hailo-all
```
```
sudo apt-get install gstreamer1.0-plugins-ugly
```
```
sudo reboot
```
#### 설치 확인
```
hailortcli fw-control identify
```
