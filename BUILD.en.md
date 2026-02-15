# 🏗️ Build Guide

[**English**](BUILD.en.md) | [**한국어**](BUILD.md)

This guide explains how to manually build and deploy the Docker image for **Hailo Exporter**.
It is written based on the Raspberry Pi 5 environment (Linux/arm64).

---

## 🛠️ Prerequisites

If your Kubernetes cluster uses `containerd` instead of Docker, you will need `nerdctl` to build images.

### Install nerdctl and buildkit
1.  **Create installation directory**
    ```bash
    mkdir nerdctl && cd nerdctl
    ```

2.  **Download and install nerdctl**
    ```bash
    # Check latest version URL (arm64) and download
    curl -s https://api.github.com/repos/containerd/nerdctl/releases/latest \
    | grep "browser_download_url.*linux-arm64.tar.gz" \
    | cut -d '"' -f 4 \
    | wget -i -

    # Extract (filename may vary by version)
    tar xzvf nerdctl-full-*-linux-arm64.tar.gz

    # Move binaries (nerdctl, buildctl, buildkitd)
    sudo cp bin/nerdctl /usr/local/bin/
    sudo cp bin/buildctl /usr/local/bin/
    sudo cp bin/buildkitd /usr/local/bin/
    ```

3.  **Verify installation and start daemon**
    ```bash
    nerdctl --version
    
    # Run buildkitd in background
    sudo nohup buildkitd > /dev/null 2>&1 &
    ```

---

## 🐳 Build & Push Image

### 1. Check Dockerfile
Use the `Dockerfile` included in the project root.
(It is configured to install `protobuf`, `prometheus_client`, etc., in a Python environment.)

### 2. Login to Docker Hub
```bash
sudo nerdctl login
```

### 3. Build Image
```bash
cd ~/hailo_exporter/
# Replace <your-dockerhub-id> with your actual Docker Hub ID.
sudo nerdctl build -t <your-dockerhub-id>/hailo_exporter:latest .
```

### 4. Push Image
```bash
sudo nerdctl push <your-dockerhub-id>/hailo_exporter:latest
```

---

## 📦 Manual Protobuf Compilation (Optional)
**Note**: The repository already includes the compiled `scheduler_mon_pb2.py` file, so this step is usually not necessary.
For underlying principles or details, refer to the [**Internal Details**](docs/internal_details.md) document.

If `scheduler_mon.proto` is updated and needs recompilation:

```bash
# 1. Install compiler
sudo apt install protobuf-compiler
pip install protobuf

# 2. Download source and compile
git clone https://github.com/hailo-ai/hailort
cd hailort/hailort/libhailort
protoc --python_out=. scheduler_mon.proto

# 3. Move result
mv scheduler_mon_pb2.py ~/hailo_exporter/
```
