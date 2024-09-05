# rocm-smi-exporter
A Prometheus exporter for rocm-smi

This exporter currently piggybacks on `rocm-smi` and exports the following metrics as Prometheus `Gauges` for AMD GPUs as well as iGPUs:

1. `rocm_smi_edge_temperature` - GPU edge temperature in degrees Celsius (`°C`).
2. `rocm_smi_socket_power` - GPU socket power consumption in watts (`W`).
3. `rocm_smi_gpu_usage` - GPU usage in percent (`%`).
4. `rocm_smi_gpu_vram_allocation` - GPU VRAM allocation in percent (`%`).

In addition, all gauges get the following labels:
1. `device_id`
2. `device_name`
3. `subsystem_id`

Support for more metrics(like fan speed) are coming soon.

## Prerequisites

1. A Linux server with an AMD iGPU/GPU present(support for Windows is in the works).
2. ROCm installed. You can refer to the official docs maintained by AMD [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html#rocm-install-quick). 

## Running

While we set up official builds, please use the following instructions to build the exporter:

1. Clone this repo
2. If you're using `pipenv`, run `pipenv install` inside this directory. If not, run `pip install -r requirements.txt`.
3. To run the app: `pipenv run python main.py` or `python main.py`. 
4. To compile the app into a binary: `pipenv run pyinstaller main.spec` or `pyinstaller main.spec`. 

The compiled binary can be found inside a newly-generated folder called `dist/` - you can move it to `/usr/local/bin`. To run the exporter as a `systemd` job, feel free to use the following template:

```
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
ExecStart=/usr/local/bin/rocm-smi-exporter
Restart=always

[Install]
WantedBy=multi-user.target
```

Also, don't forget to add a rule for scraping the exporter from Prometheus:

```yaml
scrape_configs:
# Existing configuration
  - job_name: "rocm-smi-exporter"
    static_configs:
      - targets: ["localhost:9393"]
```

