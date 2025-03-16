from openai import OpenAI
import os

from dotenv import load_dotenv

class OpenAIChatClient:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def get_chat_completion(self, messages):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return completion.choices[0].message.content


# Usage example
# if __name__ == "__main__":
#     chat_client = OpenAIChatClient()
#     messages = [
#         {"role": "developer", "content": "Talk like a pirate."},
#         {
#             "role": "user",
#             "content": "How do I check if a Python object is an instance of a class?",
#         },
#     ]
#     response = chat_client.get_chat_completion(messages)
#     print(response)
