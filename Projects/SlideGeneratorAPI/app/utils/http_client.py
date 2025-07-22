import httpx

async_client = None

def get_async_client():
    global async_client
    if async_client is None:
        async_client = httpx.AsyncClient(timeout=60.0)
    return async_client