# KND Utility

## Prerequisite

Install the following in your CentOS 8 VM
1. Docker - https://docs.docker.com/engine/install/centos/
2. kind - https://kind.sigs.k8s.io/docs/user/quick-start/
3. Install Python

### Installation & Usage

#### Create a Cluster using kind

```sh
sudo kind create cluster
```

#### Install progress bar python module
```sh
sudo pip install progress
```
#### Install KND as cli using below command
```sh
sudo python -m pip install --editable .
```

## How to run KND

```sh
KND --help
```
Usage: KND [OPTIONS] REPLICAS NGINXVERSION DEPLOYMENTNAME

Options:
  --help.

