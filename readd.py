import json, time, boto3, logging, gzip, shutil, os
#boto3.set_stream_logger('', logging.DEBUG)

def lambda_handler(event, context):
    pipeline_client = boto3.client('codepipeline')
    client = boto3.client('application-autoscaling')
    cluster = 'ecs-ec2'
    service = 'scaling-replication'
    print(event)

    sJobId = event['CodePipeline.job']['id']
    ct = event['CodePipeline.job']['data'].get('continuationToken')

    response = client.register_scalable_target(
        ServiceNamespace='ecs',
        ScalableDimension='ecs:service:DesiredCount',
        ResourceId=f'service/{cluster}/{service}',
        SuspendedState={
            'DynamicScalingInSuspended': True,
            'DynamicScalingOutSuspended': True,
            'ScheduledScalingSuspended': True
        }
    )

    response = pipeline_client.put_job_success_result(
            jobId=sJobId)

    return response