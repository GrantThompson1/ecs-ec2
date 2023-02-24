import json, time, boto3, logging, gzip, shutil, os
from botocore.exceptions import ClientError
#boto3.set_stream_logger('', logging.DEBUG)

def force_delete_service(cluster, service):
    client = boto3.client('ecs')
    try:
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

def check_queue():
    sqs = boto3.client('sqs', region_name='us-east-1')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/997477333591/my-queue'
    response = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['ApproximateNumberOfMessages']
    )
    num_messages = int(response['Attributes']['ApproximateNumberOfMessages'])
    if num_messages > 0:
        return False
    else:
        return True

def lambda_handler(event, context):
    pipeline_client = boto3.client('codepipeline')
    cluster = 'ecs-ec2'
    service = 'scaling-replication-clone'
    print(event)
    completion = False

    sJobId = event['CodePipeline.job']['id']
    ct = event['CodePipeline.job']['data'].get('continuationToken')
    
    if ct is None:
        ct = 0
    else:
        ct = int(ct)
    
    attempts = ct + 5


    while completion is False:
        completion = check_queue()
        if completion is True:
            break
        else:
            time.sleep(10)
            ct += 1
            print('Attempt', ct, 'Failed')
            if (attempts>ct):
                print('Maximum Attempts Tried. Retrying with Continuation Token Value:', ct)
                response = pipeline_client.put_job_success_result(
                    jobId=sJobId,
                    continuationToken=str(ct))
                exit()   


        
    force_delete_service(cluster, service)

    response = pipeline_client.put_job_success_result(
            jobId=sJobId)

    return response