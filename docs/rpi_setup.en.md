# 🍓 Raspberry Pi 5 Setup Guide

[**English**](rpi_setup.en.md) | [**한국어**](rpi_setup.md)

This guide explains how to set up a Raspberry Pi 5 to run the Hailo Exporter in a Kubernetes environment.

---

## 🛠️ 1. SSH Settings
Enable SSH to access the Raspberry Pi remotely.

```bash
# Check network interface
ifconfig
# Install net-tools if needed: sudo apt install net-tools

# Install OpenSSH Server
sudo apt-get install openssh-server

# Enable and start service
sudo systemctl enable ssh
sudo systemctl start ssh
```

---

## ☸️ 2. Kubernetes Node Settings

### 2.1 Edit cmdline.txt (Enable cgroup)
You need to add cgroup settings to `cmdline.txt` for the node to join the K8s cluster properly.

```bash
sudo vim /boot/firmware/cmdline.txt
```

Append the following content to the end of the file, **separated by a space** (do not add a new line):
```text
rootwait quiet splash cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1
```

Reboot after editing.
```bash
sudo reboot
```

### 2.2 Kubelet DNS Configuration (Fixing NotReady Issue)
Fixes an issue where `kubelet` points to an incorrect `resolv.conf` path on Raspberry Pi (Debian Bookworm), causing the node to be stuck in `NotReady` state or failing TLS bootstrap.

1.  **Create Kubelet service config directory**
    ```bash
    sudo mkdir -p /etc/systemd/system/kubelet.service.d
    ```

2.  **Create config file**
    ```bash
    sudo vim /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
    ```
    Paste the following content:
    ```ini
    [Service]
    Environment="KUBELET_CONFIG_ARGS=--config=/var/lib/kubelet/config.yaml --resolv-conf=/etc/resolv.conf"
    Environment="KUBELET_KUBEADM_ARGS=--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf"
    ExecStart=
    ExecStart=/usr/bin/kubelet $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS
    ```

3.  **Restart Service**
    ```bash
    sudo systemctl daemon-reexec
    sudo systemctl daemon-reload
    sudo systemctl restart kubelet
    ```

---

## ⚡ 3. PCIe Gen 3.0 Activation
Enable PCIe Gen 3.0 mode to maximize Hailo NPU performance.
Reference: [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#pcie-gen-3-0)

```bash
sudo raspi-config
```
1.  Select **Advanced Options**
2.  Select **PCIe Speed**
3.  Choose **Yes** to enable PCIe Gen 3 mode
4.  Select **Finish** and reboot (`sudo reboot`)

---

## 📦 4. Install Libraries
Install drivers and libraries required to use the Hailo NPU.

```bash
# Install all Hailo packages
sudo apt install hailo-all

# Install GStreamer plugins (for running examples)
sudo apt-get install gstreamer1.0-plugins-ugly

# Reboot to apply changes
sudo reboot
```

Verify the installation by checking firmware information.
```bash
hailortcli fw-control identify
```
