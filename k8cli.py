#!/usr/bin/python3
"""
Karthick Udayakumar
KND Utility
"""
import sys
import podcreate
import os
import click


logger=""
def main():

    cli()

@click.command()
@click.argument('replicas')
@click.argument('nginxversion')
@click.argument('deploymentname')
def cli(replicas,nginxversion,deploymentname):
    # KND utilty cli method
        try:
            replicas = replicas
            version = nginxversion
            deploymentName = deploymentname
            podcreate.nginx_deploy(int(replicas),version,deploymentName)
        except ValueError:
            print("Check your input, int, string, string")
            logger.error("Check your input, int, string, string")
        except:
            print("***Connection error. Please check for the kubernetes cluster availability*****",sys.exc_info())
            #logger.error("Unexpected error:", sys.exc_info()[0])
        else:
            podcreate.print_progress_bar(" Pod Deployment Complete.")
    
if __name__ == "__main__":
    main()