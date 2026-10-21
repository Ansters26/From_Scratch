import asyncio
import random
import time
import httpx

sem = asyncio.Semaphore(10)

async def single_service(client: httpx.AsyncClient, id: int, maxretries: int = 3):
    for attempt in range(maxretries):
        try:
            async with sem:
                response = await client.get(f"/posts/{id}", timeout=2.0)
                response.raise_for_status()
                return response.json()

        except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
            if attempt == maxretries - 1:
                return {"id": id, "status": "failed", "error": str(e)}

            delay = (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(delay)


async def combined_service():
    async with httpx.AsyncClient(base_url="https://jsonplaceholder.typicode.com") as client:
        tasks = [
            asyncio.create_task(single_service(client, (i % 100) + 1))
            for i in range(200)
        ]
        
        try:
            return await asyncio.gather(*tasks, return_exceptions=True)
        except asyncio.CancelledError:
            for task in tasks:
                if not task.done():
                    task.cancel()
            
            await asyncio.gather(*tasks, return_exceptions=True)
            raise  


async def main():
    start = time.time()
    try:
        result = await combined_service()
        print(f"Sample response: {result[0]}")
        print(f"Total processed: {len(result)}")
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\nShutdown signal received. All tasks cleaned up gracefully.")
    finally:
        end = time.time()
        print(f"Total elapsed time: {end - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())