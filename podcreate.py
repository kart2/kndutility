"""
Karthick Udayakumar
Creates, updates a deployment using AppsV1Api.
"""

import sys
from kubernetes import client, config
from urllib3.exceptions import MaxRetryError
import sys
import time
import logging
from progress.bar import Bar

logger = logging.getLogger('poddeploy')
hdlr = logging.FileHandler('/var/tmp/poddeploy.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)
# class of the deploy arg
class poddeploy:
    def __init__(self,replicas,version,name):
                self.replicas=replicas
                self.version=version
                self.name=name

# create deployment object using api              
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

# create actual kube deployment
def create_deployment(api_instance, deployment):
    # Create deployement
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace="default")
    logger.info("Deployment created. status='%s'" % str(api_response.status))

# update the kube deployment
def update_deployment(api_instance, deployment,pd):
    # Update container image
    deployment.spec.template.spec.containers[0].image = "nginx:"+pd.version
    deployment.spec.template.spec.replicas = pd.replicas
    # Update the deployment
    api_response = api_instance.patch_namespaced_deployment(
        name=pd.name,
        namespace="default",
        body=deployment)
    logger.info("Deployment updated. status='%s'" % str(api_response.status))
    
 # check the deployment status   
def getDeploymentStatus(api_instance,pd):
    api_response = api_instance.read_namespaced_deployment(pd.name, "default")
    logger.info("Pod Deployment Staus. status='%s'" % str(api_response.status))


    
def printProgressBar(task):
    bar = Bar(task, max=60)
    for i in range(60):
    # Do some work
        bar.next()
    bar.finish()
  
# main deploy method
def k8Deploy(replicas,version,name):
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    printProgressBar(" Loading Kube Config")
    try:
        apps_v1 = ""
        try:
            config.load_kube_config()
            apps_v1 = client.AppsV1Api()
        except MaxRetryError as e:
            logger.error("MaxRetryError ",e.message)
            raise   

    # Create pod argument class object
        pd=poddeploy(int(replicas),version,name)
    # Create a deployment object with client-python API. The deployment we
    # created is same as the `nginx-deployment.yaml` in the /examples folder. 
        deployment = create_deployment_object(pd)     
        try:
            getDeploymentStatus(apps_v1,pd)
            printProgressBar(" Retrieving Pod Deployment Status")
        except client.exceptions.ApiException as e1:
            #print("Exception when calling AppsV1Api->getDeploymentStatus: %s\n" % e1)
            create_deployment(apps_v1, deployment)
            printProgressBar(" Creating Pod Deployment")
        else:
            try:
                update_deployment(apps_v1, deployment,pd)
                printProgressBar(" Updating Pod Deployment")
            except client.exceptions.ApiException as e1:
                logger.exception("Exception when calling AppsV1Api->update_deployment: %s\n" % e1)
    except Exception as ex:
        logger.exception("Exception Occurred.")
        print(ex.message)
        raise
    except:
        logger.error("Unexpected error:", sys.exc_info()[0])



    #sys.stdout.flush()