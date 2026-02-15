# 🧠 Hailo Exporter Internal Details

[**English**](internal_details.en.md) | [**한국어**](internal_details.md)

This document explains the working principles of `hailortcli monitor` and the Protobuf data structure, which were analyzed for the development of **Hailo Exporter**.

## 🎯 Goal
To understand how the `hailortcli monitor` command retrieves NPU usage information and to implement an Exporter that extracts this as a Prometheus metric (`hailo_NPU_utilization`).

### References
- [hailortcli/mon_command.cpp](https://github.com/hailo-ai/hailort/blob/master/hailort/hailortcli/mon_command.cpp)
- [libhailort/scheduler_mon.proto](https://github.com/hailo-ai/hailort/blob/master/hailort/libhailort/scheduler_mon.proto)

---

## 🏗️ How it Works

### 1. What is Protobuf?
> **Protobuf (Protocol Buffers)**: Google's mechanism for serializing structured data.

`hailortcli` handles usage information in the form of **Protobuf** messages.

- **Serialization**: Converting in-memory object data into a binary stream for storage or transmission.
- **protoc**: A compiler that parses `.proto` files (schemas) and converts them into code (C++, Python, etc.) usable in various languages.

### 2. Execution Flow of hailortcli monitor
1.  **Message Definition**: The `ProtoMon` message structure is defined in the `scheduler_mon.proto` file.
2.  **Data Logging**: The HailoRT internal scheduler logs `ProtoMon` messages containing NPU status to a `.pb` (binary) file. (This only happens when executed in a terminal with `HAILO_MONITOR=1` set).
3.  **Data Reading**: The `hailortcli monitor` command reads and parses this `.pb` file to display `device_infos`, `network_infos`, etc., on the terminal.

### 3. Exporter Implementation Strategy
`hailo_exporter` implements the above process in Python to collect data.

1.  Obtain the official `scheduler_mon.proto` file.
2.  Compile it into a Python module (`scheduler_mon_pb2.py`) using `protoc`.
3.  The Exporter periodically reads the `.pb` file and deserializes it into a `ProtoMon` object.
4.  Extracts the `utilization` field value from the object and exposes it as a Prometheus metric.

---

## 🔧 Protobuf Compilation Process (Reference)
The following is the Protobuf compilation process performed during Exporter development. (Since the converted file is already included, you generally do not need to do this).

### 1. Environment Setup
```bash
# Install Protobuf compiler
sudo apt install protobuf-compiler

# Install Python library
pip install protobuf
```

### 2. Convert .proto file
```bash
# Clone HailoRT source
git clone https://github.com/hailo-ai/hailort
cd hailort/hailort/libhailort

# Convert to Python code
protoc --python_out=. scheduler_mon.proto

# Move generated file to project
mv scheduler_mon_pb2.py ~/hailo_exporter/
```
