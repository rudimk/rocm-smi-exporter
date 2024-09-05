from subprocess import check_function
import json
import time
from prometheus_client import start_http_server, Gauge

'''
Define gauges
'''
gpuEdgeTemperature = Gauge('rocm_smi_edge_temperature', 'GPU edge temperature in degrees Celsius (°C)')
gpuSocketPower = Gauge('rocm_smi_socket_power', 'GPU socket power consumption in watts (W)')
gpuUsage = Gauge('rocm_smi_gpu_usage', 'GPU usage in percent (%)')
gpuVRAMUsage = Gauge('rocm_smi_gpu_vram_allocation', 'GPU VRAM allocation in percent (%)')

'''
This function runs `rocm-smi` with the `--json` flag, and parses the output.
'''
def getGPUMetrics():
    metrics = json.loads(check_output(["rocm-smi", "-a", "--json"]))
    return metrics

