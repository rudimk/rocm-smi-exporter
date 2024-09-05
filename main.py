from subprocess import check_function
import json
import time
from prometheus_client import start_http_server, Gauge

'''
This function runs `rocm-smi` with the `--json` flag, and parses the output.
'''
def getGPUMetrics():
    metrics = json.loads(check_output(["rocm-smi", "-a", "--json"]))
    return metrics