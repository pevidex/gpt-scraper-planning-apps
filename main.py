import os
import openai
from dotenv import load_dotenv
import json
import requests


PLANNING_APPS_FOLDER = "planning-apps"
DEFAULT_COUNCIL = "cornwall"
FIELDS_TO_EXTRACT = ["address", "description", "date_received", "ref", "decision"]


def build_prompt_messages(html):
    list_of_fields = ",".join(FIELDS_TO_EXTRACT)
    base_message = f"I'm going to provide you an html file. Extract me this set of fields {list_of_fields} in a dictionary format. Your answer should only be the dictionary."
    extra_request = "Also, based on the description, could you tell me if it's commercial or residential? Add that to the dictionary as well. Remember to only print the dictionary and nothing else."
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
        model="gpt-4", messages=messages, temperature=0, max_tokens=256
    )
    return json.loads(response.choices[0].message.content)


def get_html_from_url(url):
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Print the content of the HTML page
        return response.text
    raise Exception("HTML failed to be downloaded")


def extract_fields(html):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    return extract_data(html)


def do_something_with_fields(fields):
    print(fields)


if __name__ == "__main__":
    load_dotenv()
    html = get_html_from_url("https://planning.cornwall.gov.uk/online-applications/applicationDetails.do?keyVal=S3RAUDFG0JW00&activeTab=summary")
    fields = extract_fields(html)
    do_something_with_fields(fields)
