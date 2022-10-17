# Chatbot

# TODO

- add GPU support for inference (change base image to cuda)
- Remove run as root

## Instruction

1. Run `clean-and-build.sh` to download model, weights etc.
2. Build docker image and replace it in deploy.sh

```shell
docker build . -t bponieckiklotz/jellyfish.chatbot:dev
docker push bponieckiklotz/jellyfish.chatbot:dev
```

3. Deploy model using Seldon Core

```shell
kubectl apply -f - << END
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: chatbot
spec:
  name: chatbot
  predictors:
  - componentSpecs:
    - spec:
        containers:
        - name: classifier
          image: bponieckiklotz/jellyfish.chatbot:dev
          imagePullPolicy: Always
          securityContext:
            allowPrivilegeEscalation: false
            runAsUser: 0
    graph:
      name: classifier
    name: default
    replicas: 1
END
```

## Invoke model

Adjust the model endpoint and image url in the `sample-request.py`. Run
python script.

## Swagger

Go to the URL of deployed model with suffix `/api/v0.1/doc/`.
If you port-forward to pods directly, then select service/pod with 8000 port
open. 