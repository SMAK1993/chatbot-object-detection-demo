export JELLYFISH_CONFIG_SYNC_FILENAME=/tmp/jellyfish-sync.conf

# export CHATBOT_ENDPOINT=http://10.152.183.185:8000/api/v0.1/predictions
export CHATBOT_ENDPOINT_HOST=$(kubectl get service/chatbot-default -o jsonpath='{.spec.clusterIP}')
export CHATBOT_ENDPOINT=http://$CHATBOT_ENDPOINT_HOST:8000/api/v0.1/predictions

export AZURE_SPEECH_KEY=442180fa77ac4e4da0e1f3ef3082c3ff
export AZURE_SPEECH_REGION=eastus

export CHATBOT_USE_DEFAULT_MICROPHONE=True
#export CHATBOT_MICROPHONE_DEVICE_NAME=xxx

export CHATBOT_USE_DEFAULT_SPEAKER=True
#export CHATBOT_SPEAKER_DEVICE_NAME=xxx

# export OBJECT_DETECTION_ENDPOINT=http://10.152.183.119:8000/api/v0.1/predictions
export OBJECT_DETECTION_HOST=$(kubectl get service/object-detection-default -o jsonpath='{.spec.clusterIP}')
export OBJECT_DETECTION_ENDPOINT=http://$OBJECT_DETECTION_HOST:8000/api/v0.1/predictions


export VISION_USE_CAMERA_ID=0
