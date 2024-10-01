import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

availableUsers = set()

def checkUsername(username: str, total: int, count: int):
    url = f"https://api.phantom.app/user/v1/profiles/{username}"
    start_time = time.time()

    try:
        r = requests.get(url)
        if r.status_code == 404 and r.json()['message'].lower() == "not found":
            availableUsers.add(username)

            elapsed_time = time.time() - start_time
            current_thread = threading.current_thread().name.split('_')[-1]

            print(f"\r[✅] Username Available: {username} ({count}/{total}) | Current Thread: {current_thread} | Time Taken: {elapsed_time:.2f} seconds", end="", flush=True)
            time.sleep(0.1)

    except Exception as e:
        print(f"[❓] {username} ({e})")

    return availableUsers

def main():
    with open('usernames.txt', 'r') as f:
        usernames = f.read().splitlines()

    total_usernames = len(usernames)

    try:
        threads = int(input("[🟠] Threads: "))
    except Exception:
        threads = 75

    print(f"[✅] Loaded {total_usernames:,} usernames...")
    time.sleep(1.5)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(checkUsername, username, total_usernames, idx + 1): username for idx, username in enumerate(usernames)}

        for future in as_completed(futures):
            username = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"[Error] {username} generated an exception: {e}")

    with open('available.txt', 'w') as f:
        for username in availableUsers:
            f.write(f"{username}\n")
        print(f"\n[✅] Wrote to available.txt")

if __name__ == "__main__":
    main()
