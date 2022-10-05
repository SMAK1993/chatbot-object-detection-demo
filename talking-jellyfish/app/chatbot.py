import json
import logging
import os
import time

import requests

from azure_speech import AzureSpeechRecognition, AzureSpeechSynthesizer
from config import SyncConfig

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("ChatbotApp")


def chatbot(text):
    body = {
        "data": {
            "ndarray": text
        }
    }
    response = requests.post(CHATBOT_ENDPOINT, json=body)
    log.debug(response.status_code, response.content)
    return json.loads(response.content)["strData"]


if __name__ == '__main__':

    SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
    SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
    CHATBOT_ENDPOINT = os.getenv("CHATBOT_ENDPOINT")
    log.debug("Environment properties set")

    speech_recognition = AzureSpeechRecognition(SPEECH_KEY, SPEECH_REGION)
    log.debug("Speech recognition API set")
    speech_synthesizer = AzureSpeechSynthesizer(SPEECH_KEY, SPEECH_REGION)
    log.debug("Speech synthesizer API set")

    config = SyncConfig("/tmp/jellyfish-sync.conf")
    config.save_config(cv=False, chat=False)
    log.info(f"SyncConfig file created with values: {config}")

    result_text = None
    while result_text != "Execute order 66.":
        if config.cv:
            log.info("Initiate the conversation.")
            config.save_config(cv=False, chat=True)
            INITIATION_TEXT = "Hello, would you like to talk with me?"
            speech_synthesizer(INITIATION_TEXT)
            log.info(f"New person welcomed using text: {INITIATION_TEXT}")
        elif config.chat:
            log.info("Speak to the microphone")
            result_text = speech_recognition()

            if result_text:
                log.info(f"Send user text to chatbox: {result_text}")
                chatbot_replay = chatbot(result_text)
                log.info(f"Chatbot reply: {chatbot_replay}")
                speech_synthesizer(chatbot_replay)
                log.info(f"Chatbot reply synthesized into sound.")
            else:
                log.info("No human speech sound was detected.")
                config.save_config(cv=False, chat=False)

        else:
            log.debug("Waiting for new person to arrive.")
            time.sleep(1)
            config.load_config()

    log.info("Order 66 executed. Jedi were eliminated. Shutting off.")
