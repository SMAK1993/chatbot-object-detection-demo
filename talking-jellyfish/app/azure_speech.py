import azure.cognitiveservices.speech as speechsdk


class AzureSpeechRecognition:

    def __init__(self, speech_key, speech_region, language='en-US'):
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region,
            speech_recognition_language=language)

        audio_config = speechsdk.audio.AudioConfig(
            use_default_microphone=True)

        self.speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config)

    def __call__(self, *args, **kwargs):
        print("Listening to the message in mic")
        result_message = self.speech_recognizer.recognize_once_async().get()

        if result_message.reason == speechsdk.ResultReason.RecognizedSpeech:
            result = result_message.text
            print(f"Recognized: {result}")
            return result
        elif result_message.reason == speechsdk.ResultReason.NoMatch:
            print(f"No speech could be recognized:",
                  result_message.no_match_details)
        elif result_message.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result_message.cancellation_details
            print(f"Speech Recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(
                    cancellation_details.error_details))
            raise Exception(cancellation_details.reason)


class AzureSpeechSynthesizer:
    def __init__(self, speech_key, speech_region,
                 voice_name='en-US-JennyNeural'):
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region)
        speech_config.speech_synthesis_voice_name = voice_name

        audio_config = speechsdk.audio.AudioOutputConfig(
            use_default_speaker=True)

        self.speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config)

    def __call__(self, *args, **kwargs):
        text = args[0]
        result = self.speech_synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Speech synthesized for text [{text}]")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print(
                        f"Error details: {cancellation_details.error_details}")
            raise Exception(cancellation_details.reason)
