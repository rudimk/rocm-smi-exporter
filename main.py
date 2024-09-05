from subprocess import check_output
import json
import time
from prometheus_client import start_http_server, Gauge

'''
Define gauges
'''
gpuEdgeTemperature = Gauge('rocm_smi_edge_temperature', 'GPU edge temperature in degrees Celsius (°C)', ['device_name', 'device_id', 'subsystem_id'])
gpuSocketPower = Gauge('rocm_smi_socket_power', 'GPU socket power consumption in watts (W)', ['device_name', 'device_id', 'subsystem_id'])
gpuUsage = Gauge('rocm_smi_gpu_usage', 'GPU usage in percent (%)', ['device_name', 'device_id', 'subsystem_id'])
gpuVRAMUsage = Gauge('rocm_smi_gpu_vram_allocation', 'GPU VRAM allocation in percent (%)', ['device_name', 'device_id', 'subsystem_id'])

'''
This function runs `rocm-smi` with the `--json` flag, and parses the output.
'''
def getGPUMetrics():
    metrics = json.loads(check_output(["rocm-smi", "-a", "--json"]))
    return metrics

'''
Start a Prometheus exporter server, and emit GPU metrics every 10s
'''
if __name__ == '__main__':
    start_http_server(9393)

    # Start an infinite loop
    while True:
        # Retrieve current metrics
        metrics = getGPUMetrics()
        # Set values for all gauges, across all available GPUs
        for card in list(metrics.keys()):
            # Since the driver version is also exported as a key called `system`, disregard that
            if card != "system":
                gpuEdgeTemperature.labels(device_name=metrics[card]['Device Name'], device_id=metrics[card]['Device ID'], subsystem_id=metrics[card]['Subsystem ID']).set(metrics[card]['Temperature (Sensor edge) (C)'])
                gpuSocketPower.labels(device_name=metrics[card]['Device Name'], device_id=metrics[card]['Device ID'], subsystem_id=metrics[card]['Subsystem ID']).set(metrics[card]['Current Socket Graphics Package Power (W)'])
                gpuUsage.labels(device_name=metrics[card]['Device Name'], device_id=metrics[card]['Device ID'], subsystem_id=metrics[card]['Subsystem ID']).set(metrics[card]['GPU use (%)'])
                gpuVRAMUsage.labels(device_name=metrics[card]['Device Name'], device_id=metrics[card]['Device ID'], subsystem_id=metrics[card]['Subsystem ID']).set(metrics[card]['GPU Memory Allocated (VRAM%)'])
                
        time.sleep(10)

            

