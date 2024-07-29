import asyncio
import aiohttp
import pyfiglet
from termcolor import colored

async def join_group(session, group_id, token):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ja",
        "Agent": "YayWeb 3.32.1",
        "X-Device-Info": "Yay 3.32.1 Web (Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0)",
        "Authorization": f"Bearer {token}",
    }
    join_url = f"https://api.yay.space/v1/groups/{group_id}/join"
    async with session.post(join_url, headers=headers) as response:
        response_text = await response.text()  
        if response.status == 201:
            message = f"Successfully joined the group."
            return True, token, message
        else:
            message = f"Failed to join the group. Error code: {response.status}. Response: {response_text}"
            return False, token, message

async def main():
    print(colored(pyfiglet.figlet_format("Yay! Joiner"), 'blue'))
    group_id = input("Enter the group ID to join: ")
    with open('token.txt') as file:
        tokens = [line.strip() for line in file]

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*(join_group(session, group_id, token) for token in tokens))
        for success, token, message in results:
            if not success:
                print(colored(f"[✖︎] {token}: {message}", 'red'))
            else:
                print(colored(f"[✔︎] {token}: {message}", 'green'))

if __name__ == "__main__":
    asyncio.run(main())
