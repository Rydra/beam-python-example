## Apache BEAM + Flink + Python POC

Most of the configuration setup for kubernetes was inspired by the following post:
https://python.plainenglish.io/apache-beam-flink-cluster-kubernetes-python-a1965f37b7cb

### How to run in local

You require to have [minikube](https://minikube.sigs.k8s.io/docs/start/) and [kubectl](https://kubernetes.io/docs/tasks/tools/) installed. I really tried having Flink and apache
BEAM play together with docker compose, but I just was unable to get it working since the
BEAM docker image hardcodes the usage of localhost.

Steps:

1. Start minikube
```
$ minikube
```

2. Run the `start-kube.sh` script to mount the docker images in the kubernetes cluster:

```
$ sh start-kube.sh
```

3. Run the `forward-flink.sh` script to forward the port 8081 to your localhost:

```
$ sh forward-flink.sh
```

4. Install the python dependencies in a virtual environment with poetry:

```
$ poetry install
```

6. Run the `beam_python_poc/beam_example.py to execute the word split example`. There are other
examples in the folder:

```
$ poetry run python beam_python_poc/beam_example.py
```

Once you are done, unmount the docker images in the kubernetes cluster by running:

```
$ sh stop-kube.sh 
```

### Running (hopefully) the Kafka examples

Start the docker compose to spin up a local kafka and zookeeper, as well as creating a couple
of test topics in the local kafka cluster:

```
$ docker-compose up
```

### TODO

* Try to run this on the Cloud (like AWS)
* Figure out of to make Kafka work offline, since I get this error:

```
Unknown Coder URN beam:coder:pickled_python:v1
```

* Try more of the examples from https://github.com/apache/beam/tree/master/sdks/python/apache_beam/examples
