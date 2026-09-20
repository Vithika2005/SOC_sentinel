import requests


def get_rag_stats(base_url):
    """
    Get statistics from the RAG service.
    """

    response = requests.get(
        f"{base_url}/rag/stats",
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def search_rag(
    base_url,
    query,
    top_k=5,
    source_filter=None
):
    """
    Perform a real RAG search.
    """

    payload = {
        "query": query,
        "top_k": top_k
    }

    if source_filter:
        payload["source_filter"] = source_filter

    response = requests.post(
        f"{base_url}/rag/search",
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    return response.json()