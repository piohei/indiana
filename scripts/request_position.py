import requests
import time

while True:
    print(requests.get("http://localhost:8886/position/dc-ee-06-61-b0-3d").json())
    time.sleep(1)