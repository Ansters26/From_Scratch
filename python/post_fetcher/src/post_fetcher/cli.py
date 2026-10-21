import asyncio
import time

from post_fetcher.service import combined_service


async def async_main():
    start = time.time()
    try:
        results = await combined_service()
        print(f"Sample response: {results[0]}")
        print(f"Total processed: {len(results)}")
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\nShutdown signal received. All tasks cleaned up gracefully.")
    finally:
        print(f"Total elapsed time: {time.time() - start:.2f}s")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
