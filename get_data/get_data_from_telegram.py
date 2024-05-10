import os
from telethon.sync import TelegramClient
from dotenv import find_dotenv, load_dotenv
#from datetime import datetime, timedelta


# Load environment variables from .env file
ENV = find_dotenv()
if ENV:
    load_dotenv(ENV)

# Your Telegram API credentials
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Your phone number
phone_number = os.getenv('PHONE_NUMBER')

# Path to your session file
session_file = 'session/session_name.session'

# Initialize the Telegram client
client = TelegramClient(session_file, api_id, api_hash)

async def get_last_messages(entity, limit=10):
    messages = await client.get_messages(entity, limit=limit)
    return messages[::-1]  # Reversing the order to get the last messages

async def save_messages_to_file(messages, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for message in messages:
            file.write(f"{message.sender_id}: {message.text}\n")

async def main():
    # Connect to Telegram
    await client.start(phone_number)

    # Phone number or username of the chat you want to retrieve messages from
    target_phone_number = os.getenv('TARGET_PHONE_NUMBER')
    
    # Get the entity corresponding to the phone number
    user_entity = await client.get_entity(target_phone_number)
    
    # Number of messages to retrieve
    limit = 10

    # Get the last messages from the phone number
    user_messages = await get_last_messages(user_entity, limit)

    # Save user messages to a text file
    user_filename = 'user_messages.txt'
    await save_messages_to_file(user_messages, user_filename)
    print(f"Last {limit} messages received from {target_phone_number} saved to {user_filename}")

    # Chat (group) name you want to retrieve messages from
    group_name = os.getenv('GROUP_NAME')

    # Get the entity corresponding to the group name
    group_entity = await client.get_entity(group_name)

    # Get the last messages from the group
    group_messages = await get_last_messages(group_entity, limit)

    # Save group messages to a text file
    group_filename = 'group_messages.txt'
    await save_messages_to_file(group_messages, group_filename)
    print(f"Last {limit} messages received from {group_name} saved to {group_filename}")

if __name__ == "__main__":
    client.loop.run_until_complete(main())