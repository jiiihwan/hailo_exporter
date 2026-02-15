# 🍓 Hailo Exporter

[**English**](README.en.md) | [**한국어**](README.md)

> A Prometheus exporter for monitoring Hailo NPU usage on Raspberry Pi 5 in Kubernetes environment.

**Hailo Exporter** is an extension of the [k8s dashboard](https://github.com/jiiihwan/k8s-dashboard) and is based on the architecture of [jetson-exporter](https://github.com/jiiihwan/jetson_exporter).

---

## 📖 Introduction

This exporter collects real-time **Hailo-8 / Hailo-8L NPU** utilization metrics from a Raspberry Pi 5 and exports them to Prometheus.

### How it Works
1.  **Protobuf Parsing**: Reads binary log files generated in the `/tmp/hmon_files` directory.
2.  **Data Extraction**: Parses the binary using Google Protocol Buffers (`scheduler_mon.proto`) to extract NPU utilization.
3.  **Prometheus Export**: Converts the extracted data into the `hailo_NPU_utilization` metric and exposes it via an HTTP server (default port 9102).

> For more technical details, please refer to the [**Internal Details**](docs/internal_details.en.md) document.

### Collected Metrics
- `hailo_NPU_utilization`: Current utilization of the Hailo NPU (%)

---

## 📦 Installation & Deployment

### 1. Prerequisites
This project assumes a **Raspberry Pi 5** running in a **Kubernetes** environment.
If you haven't set up your environment yet, please follow the [**Raspberry Pi 5 Setup Guide**](docs/rpi_setup.en.md) first.

- Enable PCIe Gen 3.0
- Install Hailo libraries and drivers (`hailo-all`)

### 2. Clone Repository
Run the following command on the master node:

```bash
git clone https://github.com/jiiihwan/hailo_exporter
cd hailo_exporter
```

### 3. Node Labeling
You must add the `device=rpi` label to the Raspberry Pi nodes equipped with Hailo NPU for the DaemonSet to be deployed correctly.

```bash
# Check node list
kubectl get nodes --show-labels

# Add label (replace [rpi-node-name] with your worker node name)
kubectl label nodes [rpi-node-name] device=rpi
```

### 4. Apply Resources
Deploy the DaemonSet, Service, and ServiceMonitor.

```bash
cd k8s_resources

# Deploy DaemonSet
kubectl apply -f hailo-exporter-daemonset.yaml

# Deploy Service & ServiceMonitor (monitoring namespace)
kubectl apply -f hailo-exporter-service.yaml -n monitoring
kubectl apply -f hailo-exporter-servicemonitor.yaml -n monitoring
```

> **Want to build the image yourself?** See the [**Build Guide (BUILD.en.md)**](BUILD.en.md).

---

## 📊 Verification

Once installed, you can generate load on the NPU to verify that metrics are being collected.
Refer to the [**Monitoring Example Guide**](docs/monitoring_example.en.md) for instructions on generating NPU load and checking metrics.
