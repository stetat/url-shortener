import sys
import os
from fastapi.testclient import TestClient
from main import create_app
import time
import random
from config import ALPHABET

n = 500
test_links = []
for i in range(n):
    test_links.append("https://" + ''.join(random.choices(ALPHABET, k=16)) + ".com")


client = TestClient(create_app())

def read_main():

    try:
        response = client.post("/links/test")
        assert response.status_code == 200
        assert response.json() == {"response" : "works well"}
    except Exception as e:
        print(f"Request failed: {e}")
        raise

def shorten_link():
    try:
        for i in range(n):
            response = client.post("/links/shorten/", params={"original_url": test_links[i]})
            assert response.status_code == 200
    except Exception as e:
        print(f"Request has failed: {e}")
        raise

# def test_read_main_multiple():
#     print("Test has started...")

#     start_time = time.perf_counter()
#     for i in range(n):
#         read_main()

#     total_time = time.perf_counter() - start_time
#     print(f"{n} tests ran in {total_time}", flush=True)
#     print(f"Average time per request is {total_time / n}", flush=True)
    
#     print("✅ Test passed!")

def test_shorten_link_multiple():
    print("Test has started")

    start_time = time.perf_counter()
    shorten_link()

    total_time = time.perf_counter() - start_time
    print(f"{n} tests ran in {total_time}")
    print(f"Average time per request: {total_time / n}")
    print(f"Average number of requests per second: {n / total_time}")
    


if __name__ == "__main__":
    test_shorten_link_multiple()