import asyncio
import aiohttp

# Constants
URL = "http://example.com"  # Replace with your URL
DATA = {}  # Replace with your data
NUM_REQUESTS = 20000
SECONDS_IN_MINUTE = 60

# Rate limit
RATE = NUM_REQUESTS / SECONDS_IN_MINUTE

async def send_request(session):
    async with session.post(URL, json=DATA) as response:
        return await response.text()

async def main():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for _ in range(NUM_REQUESTS):
            tasks.append(send_request(session))
            await asyncio.sleep(1/RATE)  # Rate limit
        responses = await asyncio.gather(*tasks)
        print(responses)  # Do something with the responses

# Python 3.7+
asyncio.run(main())
