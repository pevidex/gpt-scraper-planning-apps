import os
import openai
from dotenv import load_dotenv
import json

PLANNING_APPS_FOLDER = "planning-apps"
DEFAULT_COUNCIL = "cornwall"
FIELDS_TO_EXTRACT = ["address", "description", "date_received", "ref", "decision"]


def build_prompt_messages(html):
    list_of_fields = ",".join(FIELDS_TO_EXTRACT)
    base_message = f"I'm going to provide you an html file. Extract me this set of fields {list_of_fields} in a dictionary format. Your answer should only be the dictionary."
    extra_request = "Also, based on the description, could you tell me if it's commercial or residential? Add that to the dictionary as well."
    return [
        {"role": "user", "content": base_message},
        {"role": "user", "content": html},
        {"role": "user", "content": extra_request},
    ]


def read_files():
    folder_path = f"{PLANNING_APPS_FOLDER}/{DEFAULT_COUNCIL}"
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                yield f.read()


def extract_data(html):
    messages = build_prompt_messages(html)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature=0, max_tokens=256
    )
    return json.loads(response.choices[0].message.content)


def execute():
    openai.api_key = os.getenv("OPENAI_API_KEY")

    res = [extract_data(file) for file in read_files()]
    print(res)


if __name__ == "__main__":
    load_dotenv()
    execute()
