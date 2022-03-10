#!/bin/sh

# Configuration and service definition
kubectl create -f flink_config/flink-configuration-configmap.yaml
kubectl create -f flink_config/jobmanager-service.yaml
# Create the deployments for the cluster
kubectl create -f flink_config/jobmanager-session-deployment.yaml
kubectl create -f flink_config/taskmanager-session-deployment.yaml
