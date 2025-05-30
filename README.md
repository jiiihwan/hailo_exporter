# hailo_exporter
> A Prometheus exporter for monitoring Hailo NPU usage on Raspberry Pi 5

- This project is extension of [k8s dashboard](https://github.com/jiiihwan/k8s-dashboard)
- exporter module architecture is based on [jetson-exporter](https://github.com/laminair/jetson_stats_node_exporter)

## 1. Raspberry pi 5 k8s installation
- The installation was performed on Raspberry Pi OS

See [rpi_installation.md](https://github.com/jiiihwan/hailo_exporter/blob/main/rpi_installation.md) for more details

## 2. Understanding monitoring with hailo example 
- Using https://github.com/hailo-ai/hailo-rpi5-examples
- https://datarootlabs.com/blog/hailo-ai-kit-raspberry-pi-5-setup-and-computer-vision-pipelines

See [monitoring_example.md](https://github.com/jiiihwan/hailo_exporter/blob/main/monitoring_example.md) for more details

## 3. Prepare for Exporter

See [prepare_for_exporter.md](https://github.com/jiiihwan/hailo_exporter/blob/main/prepare_hailo_exporter.md) for more details

## 4. Build Hailo_exporter

See [build_hailo_exporter.md](https://github.com/jiiihwan/hailo_exporter/blob/main/build_hailo_exporter.md) for more details

## 5. Automate Hailo_exporter in k8s cluster

See [automate_hailo_exporter.md](https://github.com/jiiihwan/hailo_exporter/blob/main/automate_hailo_exporter.md) for more details
