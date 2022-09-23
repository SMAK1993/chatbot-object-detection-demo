#!/bin/bash

kubectl apply -f - << END
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: object-detection
spec:
  name: detect
  predictors:
  - componentSpecs:
    - spec:
        containers:
        - name: classifier
          image: bponieckiklotz/jellyfish.object-detection:0.1
          env:
          - name: TRANSFORMERS_CACHE
            value: /app/cache
    graph:
      name: classifier
    name: default
    replicas: 1
END

#test also the swagger API