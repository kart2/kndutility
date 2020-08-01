#!/usr/bin/python3

import sys
import podcreate
import os
import click

def main():
    cli()
@click.command()
@click.argument('replicas')
@click.argument('nginxversion')
@click.argument('deploymentname')
def cli(replicas,nginxversion,deploymentname):
    #if len(sys.argv) != 4:
     #   raise Exception('Invalid number of agruments. Expected 4. Received ' + str(len(sys.argv)))

        replicas = replicas
        version = nginxversion
        deploymentName = deploymentname
        try:
            podcreate.k8Deploy(int(replicas),version,deploymentName)
        except ValueError:
            logger.error("Check your input, int, string, string")
        except:
            print("***Connection error. Please check for the kubernetes cluster availability*****")
            logger.error("Unexpected error:", sys.exc_info()[0])
    #os.system("sudo systemctl start docker && chmod +x /var/run/docker.sock && /home/vagrant/vmware/kind/kind create cluster")
    #podcreate.k8Deploy(replicas,version,deploymentName)
        else:
            podcreate.printProgressBar(" Pod Deployment Complete.")
    
if __name__ == "__main__":
    main()