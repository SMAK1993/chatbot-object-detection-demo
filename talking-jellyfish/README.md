# Talking jellyfish demo

The Talking Jellyfish demo is used to showcase using multiple models to solve
the business case.

![](/home/barteus/Work/tutorials/ai-ml-demos/talking-jellyfish/app-diagram.drawio.png)

## Versions

### Version 1.0

Models:

- object detection (detr-resnet-50)
- chatbot (DialoGPT-medium)

Models are created using the hagging face pretrained models, wrapped in
Inference Endpoints and deployed as Seldon Core Deployments.

Models are build locally using the instruction in
the `./models/<model_name>/README.md`. The artifacts are stored in the Docker
repository (local or Dockerhub).

Services:

- Azure speech to text and text to speech

Applications:

- **vision app** - finds humans and notify the chatbot to start the conversation
- **chatbot app** - uses the Azure Speech API to convert sound-to-text and vice
  versa, user inputs are passed into the chatbot endpoint.

Applications are implementing the semaphore pattern using the file (
/tmp/jellyfish-sync.conf). This allows enabling and disabling the communication
for chatbot based on the humans detected in front of it.

## Instruction

1. Prepare instance with GPU and install GPUs (check using pytorch or
   tensorflow)
2. Install Microk8s and Kubeflow - https://charmed-kubeflow.io/docs/quickstart
   using the bundle.yaml file.

## Demo setup

### Models

Build, upload and deploy models based on the `README.md` files for:

- chatbot
- object-detection

Get the model endpoints:

```shell
$ kubectl get svc | grep 8000
chatbot-default                       ClusterIP   10.152.183.11    <none>        8000/TCP,5001/TCP   7d15h
object-detection-default              ClusterIP   10.152.183.182   <none>        8000/TCP,5001/TCP   5d23h
```

Create the environment properties for model urls:

```shell
export CHATBOT_ENDPOINT=http://10.152.183.11:8000/api/v0.1/predictions
export OBJECT_DETECTION_ENDPOINT=http://10.152.183.182:8000/api/v0.1/predictions
```

### Applications

#### Prerequisite

Create new Azure Speech object and get its key, region.
Setup the environment variables:

```shell
export AZURE_SPEECH_KEY=xxx
export AZURE_SPEECH_REGION=xxx
```

Run the applications using python in separated commandlines:

- `python chatbot.py`
- `python vision.py`

