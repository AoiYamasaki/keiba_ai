import requests
import time

def make_request_with_retry(url, max_retries=3, session=None):
    retries = 0
    while retries < max_retries:
        try:
            if session:
                response = session.get(url)
            else:
                response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            retries += 1
            if retries >= max_retries:
                print("Max retries exceeded.")
                return None
            print(f"Retrying in 10 seconds... (Attempt {retries}/{max_retries})")
            time.sleep(10)
