# KND Utility

## Prerequisite with Vagrant

1. Install virtual box and Vagrant
2. vagrant up
3. vagrant ssh
4. cd /vagrant_data
5. run ./install.sh

The environment will be ready to execute the KND command.

#### Expected output
[root@localhost ~]# KND 1 1.18.0 pod1

 Loading Kube Config |################################| 60/60
 Retrieving Pod Deployment Status |################################| 60/60
 Updating Pod Deployment |################################| 60/60
 Pod Deployment Complete. |################################| 60/60


## How to run KND

```sh
KND --help
```
Usage: KND [OPTIONS] REPLICAS NGINXVERSION DEPLOYMENTNAME

Options:
  --help.

## Prerequisite without Vagrant

Install the following in your CentOS 8 VM
1. Docker - https://docs.docker.com/engine/install/centos/
2. kind - https://kind.sigs.k8s.io/docs/user/quick-start/
3. Install Python 2.7

### Installation & Usage

#### Create a Cluster using kind

```sh
 kind create cluster
```

#### Install progress bar python module
```sh
 pip install progress
```
#### Install KND as cli using below command
```sh
 python -m pip install --editable .
```


