import httpx
import pytest
import respx

from post_fetcher.service import combined_service, single_service


@pytest.mark.asyncio
async def test_single_service_success():
    async with httpx.AsyncClient(base_url="https://api.test") as client:
        with respx.mock(base_url="https://api.test") as respx_mock:
            respx_mock.get("/posts/1").respond(
                200, json={"id": 1, "title": "Test Post"}
            )

            data = await single_service(client, post_id=1, backoff_factor=0.0)
            assert data["id"] == 1
            assert data["title"] == "Test Post"


@pytest.mark.asyncio
async def test_single_service_retry_and_recover():
    async with httpx.AsyncClient(base_url="https://api.test") as client:
        with respx.mock(base_url="https://api.test") as respx_mock:
            respx_mock.get("/posts/1").mock(
                side_effect=[
                    httpx.Response(500),
                    httpx.Response(200, json={"id": 1, "title": "Recovered"}),
                ]
            )

            data = await single_service(
                client, post_id=1, max_retries=3, backoff_factor=0.0
            )
            assert data["id"] == 1
            assert data["title"] == "Recovered"
            assert respx_mock.calls.call_count == 2


@pytest.mark.asyncio
async def test_single_service_exhausted_retries():
    async with httpx.AsyncClient(base_url="https://api.test") as client:
        with respx.mock(base_url="https://api.test") as respx_mock:
            respx_mock.get("/posts/99").respond(503)

            result = await single_service(
                client, post_id=99, max_retries=2, backoff_factor=0.0
            )
            assert result["status"] == "failed"
            assert result["id"] == 99
            assert "503" in result["error"]
            assert respx_mock.calls.call_count == 2


@pytest.mark.asyncio
async def test_combined_service_batch():
    async with httpx.AsyncClient(base_url="https://api.test") as client:
        with respx.mock(base_url="https://api.test") as respx_mock:
            respx_mock.get().respond(200, json={"status": "ok"})

            results = await combined_service(
                client=client,
                total_requests=10,
                concurrency_limit=3,
            )

            assert len(results) == 10
            assert all(r["status"] == "ok" for r in results)
