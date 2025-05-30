from prometheus_client.core import GaugeMetricFamily
from .hailo_stats import HailoObservable
from .logger import factory

class HailoExporter(object):
    def __init__(self, update_period=1):
        self.hailo = HailoObservable(update_period)
        self.logger = factory(__name__)
        self.name = "Hailo"

    def collect(self):
        # utilization 값 수집
        stats = self.hailo.read_stats()
        
        # utilization 메트릭 생성
        utilization_gauge = GaugeMetricFamily(
            name="device_utilization",
            documentation="Device utilization from scheduler monitoring",
            labels=["device"],
            unit="percent"
        )

        # utilization 값 추가
        utilization_gauge.add_metric(
            ["device0"],
            value=stats["utilization"]
        )

        yield utilization_gauge 
