import asyncio
import aiohttp
import time
import uuid
import random
import string

# Constants
URL = "http://track.retainly.app/events"  # Replace with your URL
TOTAL_REQUESTS = 10000
REQUESTS_PER_MINUTE = 10000
SECONDS_IN_MINUTE = 60

# Rate limit
RATE = REQUESTS_PER_MINUTE / SECONDS_IN_MINUTE

async def generate_random_event():
    customer_id = random.randint(1, 200000)
    event = "event_test"
    data = {"test" : "blabla"}
    return {
        "customer_id": customer_id,
        "event": event,
        "data": data
    }

async def generate_random_data():
    event = await generate_random_event()
    return event


async def send_request(session):
    try:
        headers = {
            "key": "nO5lz1TIy29Wn6dyk5Qn6wrWvlWp5ydV4vxT9V98qQBsxQK78MML9EOYoFJJ",  # Replace with your key
            "secret": "ap9Mg8mWMkPRgVrUxWklr2koGMOt8ZCJzxGxbTxqPftoAXI696rvFW4a4z2K"  # Replace with your secret
        }
        data = await generate_random_data()
        print("Sending a request...", time.time())
        async with session.post(URL, json=data, headers=headers) as response:
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
