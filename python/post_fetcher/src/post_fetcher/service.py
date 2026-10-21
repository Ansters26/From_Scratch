import asyncio
import random
from contextlib import nullcontext

import httpx


async def single_service(
    client: httpx.AsyncClient,
    post_id: int,
    sem: asyncio.Semaphore | None = None,
    max_retries: int = 3,
    backoff_factor: float = 1.0,
) -> dict:
    sem_context = sem if sem is not None else nullcontext()

    for attempt in range(max_retries):
        try:
            async with sem_context:
                response = await client.get(f"/posts/{post_id}", timeout=2.0)
                response.raise_for_status()
                return response.json()

        except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
            if attempt == max_retries - 1:
                return {"id": post_id, "status": "failed", "error": str(e)}

            delay = ((2**attempt) + random.uniform(0, 0.5)) * backoff_factor
            await asyncio.sleep(delay)


async def combined_service(
    base_url: str = "https://jsonplaceholder.typicode.com",
    total_requests: int = 200,
    concurrency_limit: int = 10,
    client: httpx.AsyncClient | None = None,
) -> list:
    """Orchestrate concurrent requests with clean cancellation handling."""
    sem = asyncio.Semaphore(concurrency_limit)

    async def _run(active_client: httpx.AsyncClient):
        tasks = [
            asyncio.create_task(single_service(active_client, (i % 100) + 1, sem=sem))
            for i in range(total_requests)
        ]
        try:
            return await asyncio.gather(*tasks, return_exceptions=True)
        except asyncio.CancelledError:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise

    if client is not None:
        return await _run(client)

    async with httpx.AsyncClient(base_url=base_url) as owned_client:
        return await _run(owned_client)
