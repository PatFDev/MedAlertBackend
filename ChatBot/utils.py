import openai
from dotenv import load_dotenv
import os
# Load environment variables from a .env file
load_dotenv()

# OpenAI API key configuration
openai.api_key = os.getenv("OPENAI_API_KEY")

def format_openai_messages(developer_message, medications, conversation, user_message):
    """
    Formats the messages for the OpenAI ChatCompletion request.
    
    Args:
        developer_message (str): Instruction for the assistant's behavior.
        medications (list): List of the user's current medications.
        conversation (list): List of previous messages in the conversation.
        user_message (str): The latest user message.

    Returns:
        list: A formatted list of messages for OpenAI ChatCompletion.
    """
    # Base developer message
    messages = [
        {"role": "developer", "content": developer_message},
        {"role": "developer", "content": f"The patient is currently taking the following medications: {medications}."}
    ]

    # Add conversation history
    for entry in conversation:
        messages.append({"role": entry["role"], "content": entry["content"]})

    # Add the latest user message
    messages.append({"role": "user", "content": user_message})

    return messages


def get_openai_response(messages, model="gpt-4o"):
    """
    Makes a call to OpenAI ChatCompletion API and returns the assistant's response.

    Args:
        messages (list): Formatted list of messages for the OpenAI API.
        model (str): The model to use for the OpenAI API request.

    Returns:
        str: The assistant's response message.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        return response["choices"][0]["message"]["content"]
    except openai.error.OpenAIError as e:
        raise Exception(f"OpenAI API error: {str(e)}")
