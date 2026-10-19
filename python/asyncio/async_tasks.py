import asyncio

async def fun(time,id):
    await asyncio.sleep(time)
    print(f"Done with the task {id}")

async def main():
    async with asyncio.TaskGroup() as tg:
        for id, time in enumerate([2, 1, 3], start=1):
            tg.create_task(fun(time, id))

asyncio.run(main())
