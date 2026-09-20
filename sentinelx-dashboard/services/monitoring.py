import requests


def query_prometheus(prometheus_url, query):
    """
    Run a PromQL query against Prometheus.
    Returns a list of metric results.
    """

    try:
        response = requests.get(
            f"{prometheus_url}/api/v1/query",
            params={"query": query},
            timeout=5,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") != "success":
            return []

        return data.get("data", {}).get("result", [])

    except requests.RequestException:
        return []


def get_service_health(prometheus_url):
    """
    Get the current Blackbox health status
    for SentinelX services.
    """

    query = 'probe_success{job="sentinelx-health"}'

    results = query_prometheus(prometheus_url, query)

    services = []

    for result in results:
        metric = result.get("metric", {})
        value = result.get("value", [])

        if len(value) < 2:
            continue

        services.append(
            {
                "service": metric.get("service", "unknown"),
                "status": "UP" if float(value[1]) == 1 else "DOWN",
                "instance": metric.get("instance", ""),
            }
        )

    return services


def get_service_response_time(prometheus_url):
    """
    Get HTTP response time for SentinelX services.
    """

    query = 'probe_duration_seconds{job="sentinelx-health"}'

    results = query_prometheus(prometheus_url, query)

    services = []

    for result in results:
        metric = result.get("metric", {})
        value = result.get("value", [])

        if len(value) < 2:
            continue

        services.append(
            {
                "service": metric.get("service", "unknown"),
                "response_time_ms": round(
                    float(value[1]) * 1000,
                    2,
                ),
            }
        )

    return services


def get_qdrant_vector_count(prometheus_url):
    """
    Get the number of vectors in the SentinelX
    threat-intel Qdrant collection.
    """

    query = 'collection_points{id="threat-intel"}'

    results = query_prometheus(prometheus_url, query)

    if not results:
        return None

    value = results[0].get("value", [])

    if len(value) < 2:
        return None

    return int(float(value[1]))


def get_monitoring_components(prometheus_url):
    """
    Check whether Prometheus and Blackbox Exporter
    are being scraped successfully.
    """

    query = 'up{job=~"prometheus|blackbox-exporter"}'

    results = query_prometheus(prometheus_url, query)

    components = []

    for result in results:
        metric = result.get("metric", {})
        value = result.get("value", [])

        if len(value) < 2:
            continue

        components.append(
            {
                "component": metric.get("job", "unknown"),
                "status": "UP" if float(value[1]) == 1 else "DOWN",
            }
        )

    return components