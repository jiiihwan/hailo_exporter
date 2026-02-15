# 📊 Monitoring Example Guide

[**English**](monitoring_example.en.md) | [**한국어**](monitoring_example.md)

This guide explains how to run an example pipeline to generate NPU load, allowing you to verify that the Hailo Exporter is collecting metrics correctly.

References:
- [hailo-rpi5-examples](https://github.com/hailo-ai/hailo-rpi5-examples)
- [DataRoot Labs Blog](https://datarootlabs.com/blog/hailo-ai-kit-raspberry-pi-5-setup-and-computer-vision-pipelines)

---

## ⚙️ 1. Download & Examples Setup

Clone the example repository provided by Hailo and set up the environment.

```bash
# Clone repository
git clone https://github.com/hailo-ai/hailo-rpi5-examples.git
cd hailo-rpi5-examples

# Run install script
./install.sh

# Download resources (models, etc.)
./download_resources.sh
```

---

## 🖥️ 2. Environment Setup

Configure environment variables before running the example.

```bash
cd hailo-rpi5-examples

# Load virtual environment and libraries
source setup_env.sh 

# Display settings (Required for SSH)
# Set to :0 if a physical monitor is connected
export DISPLAY=:0 

# Enable Monitoring (Important!)
# This variable must be set for NPU usage to be recorded and collected by the Exporter.
export HAILO_MONITOR=1
```

---

## ✔️ 3. Generate Load
Run the Object Detection pipeline. NPU load will be generated while this code is running.

```bash
python basic_pipelines/detection.py
```

---

## 📈 4. Check Metrics

### 4.1 Check via CLI
Open a new terminal and enter the following command to view real-time usage.

```bash
hailortcli monitor 
```

### 4.2 Check via Prometheus/Grafana
If the Hailo Exporter is installed, you should see the `hailo_NPU_utilization` metric rising in your Grafana dashboard.
