import requests


def get_graph(base_url):
    """
    Get the Digital Twin graph summary.
    """

    response = requests.get(
        f"{base_url}/twin/graph",
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def get_blast_radius(
    base_url,
    asset,
    entrypoint=None
):
    """
    Calculate the Digital Twin blast radius
    for an asset.
    """

    params = {}

    if entrypoint:
        params["entrypoint"] = entrypoint

    response = requests.get(
        f"{base_url}/twin/blast-radius/{asset}",
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def get_health(base_url):

    response = requests.get(
        f"{base_url}/health",
        timeout=5
    )

    response.raise_for_status()

    return response.json()