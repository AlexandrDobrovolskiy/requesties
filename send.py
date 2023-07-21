import asyncio
import aiohttp
import time

# Constants
URL = "https://webhook.site/a3abd1e4-0c0c-41fd-8253-1f609b0427a1"  # Replace with your URL
DATA = {}  # Replace with your data
TOTAL_REQUESTS = 10
REQUESTS_PER_MINUTE = 5
SECONDS_IN_MINUTE = 60

# Rate limit
RATE = REQUESTS_PER_MINUTE / SECONDS_IN_MINUTE

async def send_request(session):
    try:
        print("Sending a request...", time.time())
        async with session.post(URL, json=DATA) as response:
            res = await response.text()
            print(res)
            return res
    except Exception as e:
        print("Error sending request:", e)

async def main():
    tasks = []
    async with aiohttp.ClientSession() as session:
        requests_sent = 0
        start_time = time.time()  # Initialize start_time variable
        while requests_sent < TOTAL_REQUESTS:
            for _ in range(REQUESTS_PER_MINUTE):
                if requests_sent >= TOTAL_REQUESTS:
                    break
                task = asyncio.create_task(send_request(session))  # Use asyncio.create_task
                tasks.append(task)
                requests_sent += 1
                if requests_sent % REQUESTS_PER_MINUTE == 0:
                    elapsed_time = time.time() - start_time
                    if elapsed_time < SECONDS_IN_MINUTE:
                        sleep_time = SECONDS_IN_MINUTE - elapsed_time
                        print("Sleeping for", sleep_time, "seconds")
                        await asyncio.sleep(sleep_time)
            if requests_sent < TOTAL_REQUESTS:
                start_time = time.time()  # Update start_time for the next set
        responses = await asyncio.gather(*tasks)
        print("Total responses:", len(responses))  # Do something with the responses
        return len(responses)  # Return the total number of responses

# Python 3.7+
total_responses = asyncio.run(main())
print("Total requests sent:", total_responses)
