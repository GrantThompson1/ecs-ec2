import json, time, boto3, logging, gzip, shutil, os
from botocore.exceptions import ClientError
#boto3.set_stream_logger('', logging.DEBUG)

def force_delete_service(cluster, service):
    client = boto3.client('ecs')
    try:
        response = client.update_service(
            cluster=cluster,
            service=service,
            desiredCount=0
        )
        response = client.delete_service(
            cluster=cluster,
            service=service,
            force=True
        )
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'ClusterNotFoundException':
            print(f"Cluster '{cluster}' not found.")
        elif e.response['Error']['Code'] == 'ServiceNotFoundException':
            print(f"Service '{service}' not found in cluster '{cluster}'.")
        else:
            print("Unexpected error: %s" % e)

def lambda_handler(event, context):
    pipeline_client = boto3.client('codepipeline')
    cluster = 'ecs-ec2'
    service = 'scaling-replication-clone'
    print(event)

    sJobId = event['CodePipeline.job']['id']
    ct = event['CodePipeline.job']['data'].get('continuationToken')

    completion = False

    while completion is False:
        print('Not done')
        
    force_delete_service('my-cluster', 'my-service')

    response = pipeline_client.put_job_success_result(
            jobId=sJobId)

    return response