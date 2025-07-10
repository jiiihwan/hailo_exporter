# Understanding monitoring with hailo example
- referred to the following link:
  - https://github.com/hailo-ai/hailo-rpi5-examples
  - https://datarootlabs.com/blog/hailo-ai-kit-raspberry-pi-5-setup-and-computer-vision-pipelines

### ⚙️ git clone & initial setting
```
git clone https://github.com/hailo-ai/hailo-rpi5-examples.git
cd hailo-rpi5-examples
./install.sh
./download_resources.sh
```

### 🖥️ Monitoring environmental settings


```
cd hailo-rpi5-examples
```

```
source setup_env.sh 
```
환경 세팅

```
export DISPLAY=:0 
```
ssh로 연결했을때 gui출력이 없으므로 연결된 실제 모니터에 대신 출력

```
export HAILO_MONITOR=1
```
코드를 실행하는 터미널에서 입력해서 환경변수 설정

### ✔️ Example execution
```
python basic_pipelines/detection.py --input resources/detection0.mp4
```

### 📈 Monitoring NPU usage
- Open a new terminal and enter the following command 

```
hailortcli monitor 
```

