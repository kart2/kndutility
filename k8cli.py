#!/usr/bin/python3
"""
Karthick Udayakumar
KND Utility
"""
import sys
import podcreate
import os
import click

logger=podcreate.logger_obj()
def main():
    try:
        cli()
    except:
        podcreate.print_progress_bar(" Unexpected error occurred. Check your logs at ./poddeploy.log")

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
            
            podstatus = podcreate.nginx_deploy(int(replicas),version,deploymentName)
        except ValueError:
            print("Check your input, int, string, string")
            logger.error("Check your input, int, string, string")
        except AttributeError:
            print("AttributeError")
            logger.error("AttributeError")
        except:
            #print("***Connection error. Please check for the kubernetes cluster availability*****",sys.exc_info())
            logger.error("Unexpected error:")
            raise
        else:
            if podstatus is not None:
                podcreate.print_progress_bar(" Pod Deployment Complete.")
            else:
                podcreate.print_progress_bar(" Pod Deployment Failed. Please check logs at ./poddeploy.log")
    
if __name__ == "__main__":
    main()