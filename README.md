# Python Healthcheck

A lightweight Python application exposing Prometheus metrics for monitoring external URLs and Python process statistics.

## Features

- Monitors availability of external URLs (`up` / `down`)
- Measures response time for each URL in milliseconds
- Exposes Python runtime metrics (GC stats, memory usage, CPU time)
- Docker-ready with a multi-stage build
- Prometheus-compatible `/metrics` endpoint

## Getting Started

### Prerequisites

- Python 3.13+
- `pip`
- Docker (optional)
- Helm (optional)

### Local Setup

# Clone the repository
git clone https://github.com/ivanov-vision/vaerolab-v1
cd vaerolab-v1/app

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # On Windows PowerShell
# OR
source venv/bin/activate       # On Linux / macOS

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open your browser or use curl to see metrics
curl http://localhost:8000/metrics

### Docker Setup
From root dir
docker build -f docker/Dockerfile -t vaerolab-app .
docker run -p 8000:8000 vaerolab-app

### Kubernetes / Helm Deployment

Navigate to Helm chart folder:  
`cd helm-charts`

Install the Helm chart:  
`helm install vaerolab-app .`  

Check pods and service:  
`kubectl get pods`  
`kubectl get svc`

Customizing Deployment:  
Override default values using a file:  
`helm install vaerolab-app . -f my-values.yaml`  

I recommend k8s deployment is done via pipelines.

### Prometheus Integration in k8s

Add this job to your Prometheus configuration:

scrape_configs:
  - job_name: 'python-healthcheck'
    static_configs:
      - targets: ['python-healthcheck.default.svc.cluster.local:8400']  # adjust host/port/url as needed

### Metrics Exposed

- `sample_external_url_up{url="..."}`: 1 if URL is reachable, 0 otherwise
- `sample_external_url_response_ms{url="..."}`: Response time in ms
- `python_gc_objects_collected_total{generation="0|1|2"}`: GC collected objects
- `python_gc_objects_uncollectable_total{generation="0|1|2"}`: Uncollectable objects
- `python_gc_collections_total{generation="0|1|2"}`: GC collection counts
- `python_info`: Python version info
- `process_virtual_memory_bytes`, `process_resident_memory_bytes`, `process_cpu_seconds_total`, etc.