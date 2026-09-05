import requests


def get(
    url: str,
    params: dict | None = None,
    headers: dict | None = None,
    timeout: int = 10,
) -> requests.Response:
    response = requests.get(url, params=params, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response