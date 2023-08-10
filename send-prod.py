import asyncio
import aiohttp
import time
import uuid
import random
import string

# Constants
URL = "http://track.retainly.app/customers"  # Replace with your URL
TOTAL_REQUESTS = 50000
REQUESTS_PER_MINUTE = 50000

SECONDS_IN_MINUTE = 60
MAX_CUSTOMERS_PER_REQUEST = 1000

# Rate limit
RATE = REQUESTS_PER_MINUTE / SECONDS_IN_MINUTE

async def generate_random_customer():
    customer_id = str(uuid.uuid4())  # Generate a random UUID
    email = ''.join(random.choices(string.ascii_lowercase, k=10)) + "@example.com"  # Random email
    phone = ''.join(random.choices(string.digits, k=10))  # Random phone number
    return {
        "id": customer_id,
        "email": email,
        "phone": phone
    }

async def generate_random_data():
    customers = []
    for _ in range(MAX_CUSTOMERS_PER_REQUEST):
        customers.append(await generate_random_customer())
    return {
        "customers": customers
    }

async def send_request(session):
    try:
        headers = {
            "key": "ljdQIfG99Wahspv7uwT8fECIroRIhy3fG6Y5eIRXVANs0C5jp3qL0l4B5kQV",  # Replace with your key
            "secret": "WRxfx5U17cRtcfFG71vnQggrF9KbJXys868uTRhZqe9T8hY8IYBbpVSBBpz7"  # Replace with your secret
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
