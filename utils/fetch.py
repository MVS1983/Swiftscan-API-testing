
import requests


def fetch_get(url, params):
    """Create the full query URL"""
    q = f"{url}?{'&'.join(params)}" if params else url

    print(q.rstrip('?'))
    # Make the HTTP request
    resp = requests.get(q)

    try:
        body = resp.json()
    except ValueError:
        body = {}

    return [resp, body]
