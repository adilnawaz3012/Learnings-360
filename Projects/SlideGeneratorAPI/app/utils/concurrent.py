import asyncio
from concurrent.futures import ThreadPoolExecutor

# Thread pool for CPU-bound tasks
ppt_executor = ThreadPoolExecutor(max_workers=8)

async def run_in_thread(fn, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(ppt_executor, fn, *args, **kwargs)