import json
import os
import time

import requests

from azure_speech import AzureSpeechRecognition, AzureSpeechSynthesizer
from config import SyncConfig


def chatbot(text):
    body = {
        "data": {
            "ndarray": text
        }
    }
    response = requests.post(CHATBOT_ENDPOINT, json=body)
    print(response.status_code, response.content)
    return json.loads(response.content)["strData"]


def save_config(filename, cv, chat):
    content = {
        "cv_enabled": cv,
        "chat_enabled": chat
    }

    with open(filename, 'w') as f:
        f.write(json.dumps(content))
    return content


def load_config(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())


if __name__ == '__main__':

    SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
    SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
    CHATBOT_ENDPOINT = os.getenv("CHATBOT_ENDPOINT")

    speech_recognition = AzureSpeechRecognition(SPEECH_KEY, SPEECH_REGION)
    speech_synthesizer = AzureSpeechSynthesizer(SPEECH_KEY, SPEECH_REGION)

    config = SyncConfig("/tmp/jellyfish-sync.conf")

    result_text = None
    while result_text != "Execute order 66.":
        if config.cv:
            config.save_config(cv=False, chat=True)
            INITIATION_TEXT = "Hello, would you like to talk with me?"
            speech_synthesizer(INITIATION_TEXT)
        elif config.chat:
            result_text = speech_recognition()

            if result_text:
                chat_bot_replay = chatbot(result_text)
                speech_synthesizer(chat_bot_replay)
            else:
                config.save_config(cv=False, chat=False)

        else:
            time.sleep(1)
            config.load_config()

    print("End")
