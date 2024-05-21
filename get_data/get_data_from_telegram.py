import os
from telethon.sync import TelegramClient
from dotenv import find_dotenv, load_dotenv


# Load environment variables from .env file
ENV = find_dotenv()
if ENV:
    load_dotenv(ENV)

# Your Telegram API credentials
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
# Number of messages to retrieve
limit = int(os.getenv('LIMIT_MESSAGES'))
# Chat (group) name you want to retrieve messages from
group_name = os.getenv('GROUP_NAME')

# Path to session file
session_file = 'session/session_name.session'

# Initialize the Telegram client
client = TelegramClient(session_file, api_id, api_hash)

async def get_last_messages(entity, limit=10):
    messages = await client.get_messages(entity, limit=limit)
    return messages[::-1]  # Reversing the order to get the last messages

async def save_messages_to_file(messages, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for message in messages:
            file.write(f"{message.sender_id}: {message.text}\n{message.date}\n")

async def main():
    # Connect to Telegram
    await client.start(phone_number)
    # Get the entity corresponding to the group name
    group_entity = await client.get_entity(group_name)
    # Get the last messages from the group
    group_messages = await get_last_messages(group_entity, limit)
    # Save group messages to a text file
    group_filename = 'group_messages.txt'
    await save_messages_to_file(group_messages, group_filename)
    print(f"Last {limit} messages received from {group_name} saved to {group_filename}")

def loop_main():
    client.loop.run_until_complete(main())
