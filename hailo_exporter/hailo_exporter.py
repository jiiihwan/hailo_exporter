import os
import argparse
from time import sleep
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, GaugeMetricFamily

from scheduler_mon_pb2 import ProtoMon


class HailoExporter:
    def __init__(self, update_period=1, directory="/tmp/hmon_files"):
        if update_period < 0.5:
            print("[Warning] update_period too low. Falling back to 1.0s.")
            update_period = 1.0
        self.interval = update_period
        self.directory = directory
        self.data = {}

    def get_single_file(self):
        #디렉토리 내 단일 바이너리 파일 선택 (여러 파일 있을 경우 첫 번째 사용)
        try:
            files = os.listdir(self.directory)
            if not files:
                return None
            if len(files) > 1:
                print("Warning: Multiple files found, using the first one.")
            return os.path.join(self.directory, files[0])
        except Exception as e:
            print(f"[Error] Failed to list directory: {e}")
            return None

    def read_stats(self):
        #protobuf 파싱을 통해 Hailo NPU utilization 값을 읽어옴
        try:
            path = self.get_single_file()
            if path:
                proto = ProtoMon()
                with open(path, "rb") as f:
                    proto.ParseFromString(f.read())

                # 첫 번째 디바이스의 utilization 값 반환
                if proto.device_infos:
                    self.data["utilization"] = proto.device_infos[0].utilization
                else:
                    self.data["utilization"] = 0.0
            else:
                self.data["utilization"] = 0.0
        except Exception as e:
            print(f"Error reading utilization: {e}")
            self.data["utilization"] = 0.0

        return self.data
    
    def npu_usage(self):
        # utilization 메트릭 생성
        utilization_gauge = GaugeMetricFamily(
            name="hailo_NPU_utilization",
            documentation="Hailo NPU utilization from scheduler monitoring",
            labels=["NPU"],
            unit="percent"
        )

        # utilization 값 추가
        utilization_gauge.add_metric(["NPU"], self.data["utilization"])

        return utilization_gauge


    def collect(self):
        # utilization 값 수집
        self.read_stats()
        yield self.npu_usage()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9102)
    parser.add_argument("--update_period", type=float, default=1)
    args = parser.parse_args()

    start_http_server(args.port)
    REGISTRY.register(HailoExporter(args.update_period))

    while True:
        sleep(1)
