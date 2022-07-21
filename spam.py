# Spam Script
import requests
import random
import time

token = 'ENTER ACCOUNT TOKEN HERE'
channel = 'ENTER CHANNEL ID HERE'


def spam_channel(channel_id: str):
    headers = {'authorization': token}
    data = {'content': ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(10))}
    requests.post(f'https://canary.discord.com/api/v9/channels/{channel_id}/messages', headers=headers, json=data)
    time.sleep(2)

def token_info(token: str):
    headers = {'authorization': token}
    return requests.get('https://canary.discord.com/api/v9/users/@me', headers=headers).json()
    
if __name__ == '__main__':
    info = token_info(token)
    print(f'[+] {info["username"]}#{info["discriminator"]} | {info["id"]}\n[!] Spam started, press Ctrl+C to stop.')
    while True:
        spam_channel(channel)

    

