from prometheus_client import start_http_server, Gauge
import requests
import time

# URLs to check
URLS = [
    "https://tools-httpstatus.pickup-services.com/503",
    "https://tools-httpstatus.pickup-services.com/200",
]

# Define Prometheus metrics
url_up = Gauge(
    "sample_external_url_up",
    "Whether the URL is up (1 = yes, 0 = no)",
    ["url"],
)
url_response_ms = Gauge(
    "sample_external_url_response_ms",
    "Response time for the URL in milliseconds",
    ["url"],
)

def check_url(url):
    try:
        start = time.time()
        resp = requests.get(url, timeout=5)
        elapsed_ms = (time.time() - start) * 1000
        url_response_ms.labels(url=url).set(elapsed_ms)
        if resp.status_code == 200:
            url_up.labels(url=url).set(1)
        else:
            url_up.labels(url=url).set(0)
    except requests.RequestException:
        url_up.labels(url=url).set(0)
        url_response_ms.labels(url=url).set(-1)

if __name__ == "__main__":
    # Start Prometheus metrics server on port 8000
    start_http_server(8000)
    print("Serving metrics on :8000/metrics")

    while True:
        for url in URLS:
            check_url(url)
        time.sleep(10)  # scrape interval
