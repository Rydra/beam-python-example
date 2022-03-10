#!/bin/sh

# Configuration and service definition
kubectl delete -f flink_config/flink-configuration-configmap.yaml
kubectl delete -f flink_config/jobmanager-service.yaml
# Create the deployments for the cluster
kubectl delete -f flink_config/jobmanager-session-deployment.yaml
kubectl delete -f flink_config/taskmanager-session-deployment.yaml
