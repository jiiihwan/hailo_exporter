import os
from . import scheduler_mon_pb2

class HailoObservable(object):
    def __init__(self, update_period=1):
        self.data = {}
        self.interval = update_period

    def get_single_file(self, directory="/tmp/hmon_files"):
        files = os.listdir(directory)
        if not files:
            return None
        if len(files) > 1:
            print("Warning: Multiple files found, using the first one.")
        return os.path.join(directory, files[0])

    def read_stats(self):
        try:
            path = self.get_single_file("/tmp/hmon_files")
            if path:
                proto = scheduler_mon_pb2.ProtoMon()
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
