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

### Local Setup

# Clone the repository
git clone https://github.com/your-username/vaerolab-v1.git
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

cd docker
docker build -t vaerolab-app .
docker run -p 8000:8000 vaerolab-app

### Prometheus Integration

Add this job to your Prometheus configuration:

scrape_configs:
  - job_name: 'vaerolab-app'
    static_configs:
      - targets: ['host.docker.internal:8000']  # adjust host/port as needed

### Metrics Exposed

- `sample_external_url_up{url="..."}`: 1 if URL is reachable, 0 otherwise
- `sample_external_url_response_ms{url="..."}`: Response time in ms
- `python_gc_objects_collected_total{generation="0|1|2"}`: GC collected objects
- `python_gc_objects_uncollectable_total{generation="0|1|2"}`: Uncollectable objects
- `python_gc_collections_total{generation="0|1|2"}`: GC collection counts
- `python_info`: Python version info
- `process_virtual_memory_bytes`, `process_resident_memory_bytes`, `process_cpu_seconds_total`, etc.



