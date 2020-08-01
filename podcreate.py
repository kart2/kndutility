"""
Karthick Udayakumar
Creates, updates a deployment using AppsV1Api.
"""

import sys
from kubernetes import client, config
from urllib3.exceptions import MaxRetryError
import time
from progress.bar import Bar
import logging


logger = logging.getLogger('PodDeploy')
hdlr = logging.FileHandler('./poddeploy.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)


class PodDeploy:
    """
    This class helps to create the pod deploy arguments wrapper       
    """
    def __init__(self,replicas,version,name):
                self.replicas=replicas
                self.version=version
                self.name=name

             
def create_deployment_object(pd):
    # Configureate Pod template container
    container = client.V1Container(
        name="nginx",
        image="nginx:"+pd.version,
        ports=[client.V1ContainerPort(container_port=80)],
        resources=client.V1ResourceRequirements(
            requests={"cpu": "50m", "memory": "100Mi"},
            limits={"cpu": "50m", "memory": "200Mi"}
        )
    )
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=pd.replicas,
        template=template,
        selector={'matchLabels': {'app': 'nginx'}})
    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=pd.name),
        spec=spec)

    return deployment


def create_deployment(api_instance, deployment):
    # Create deployement
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace="default")
    logger.info("Deployment created. status='%s'" % str(api_response.status))


def update_deployment(api_instance, deployment,pd):
    # update the kube deployment
    # Update container image
    deployment.spec.template.spec.containers[0].image = "nginx:"+pd.version
    deployment.spec.template.spec.replicas = pd.replicas
    # Update the deployment
    api_response = api_instance.patch_namespaced_deployment(
        name=pd.name,
        namespace="default",
        body=deployment)
    logger.info("Deployment updated. status='%s'" % str(api_response.status))
    
 
def get_deployment_status(api_instance,pd):
     # check the deployment status   
    api_response = api_instance.read_namespaced_deployment(pd.name, "default")
    logger.info("Pod Deployment Staus. status='%s'" % str(api_response.status))

 
def print_progress_bar(task):
    # prints the progress bar  
    bar = Bar(task, max=60)
    for i in range(60):
    # Do some work
        bar.next()
    bar.finish()
  

def nginx_deploy(replicas,version,name):
    # main deploy method
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    print_progress_bar(" Loading Kube Config")
    try:
        apps_v1 = ""
        try:
            config.load_kube_config()
            apps_v1 = client.AppsV1Api()
        except MaxRetryError as e:
            logger.error("MaxRetryError ",e.message)
            raise   
        pd=PodDeploy(int(replicas),version,name)
        # Create a deployment object with client-python API.
        deployment = create_deployment_object(pd)     
        try:
            get_deployment_status(apps_v1,pd)
            print_progress_bar(" Retrieving Pod Deployment Status")
        except client.exceptions.ApiException as e1:
            # Create a new deployment 
            create_deployment(apps_v1, deployment)
            print_progress_bar(" Creating Pod Deployment")
        else:
            try:
                update_deployment(apps_v1, deployment,pd)
                print_progress_bar(" Updating Pod Deployment")
            except client.exceptions.ApiException as e1:
                logger.exception("Exception when calling AppsV1Api->update_deployment: %s\n" % e1)
    except Exception as ex:
        logger.exception("Exception Occurred.")
        raise
    except:
        logger.error("Unexpected error:", sys.exc_info()[0])