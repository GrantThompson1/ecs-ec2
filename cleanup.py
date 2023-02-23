import json, time, boto3, logging, gzip, shutil, os
#boto3.set_stream_logger('', logging.DEBUG)

def lambda_handler(event, context):
    client = boto3.client('codepipeline')
    print(event)

    sJobId = event['CodePipeline.job']['id']
    ct = event['CodePipeline.job']['data'].get('continuationToken')

    s3 = boto3.resource('s3',
                    aws_access_key_id=event['CodePipeline.job']['data']['artifactCredentials']['accessKeyId'],
                    aws_secret_access_key=event['CodePipeline.job']['data']['artifactCredentials']['secretAccessKey'],
                    aws_session_token=event['CodePipeline.job']['data']['artifactCredentials']['sessionToken'])

    s3.Bucket(event['CodePipeline.job']['data']['inputArtifacts'][0]['location']['s3Location']['bucketName']).download_file(event['CodePipeline.job']['data']['inputArtifacts'][0]['location']['s3Location']['objectKey'], '/tmp/my_file.json')

    dictionary = {
        "Key1": "new_file_confirmation"
    }

    json_object = json.dumps(dictionary, indent=4)

    with open("/tmp/my_file.json", "w") as outfile:
        outfile.write(json_object)
    
    with open('/tmp/my_file.json', 'rb') as f_in:
        with gzip.open('/tmp/zip_out.zip', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(os.listdir("/tmp"))
    s3.Bucket(event['CodePipeline.job']['data']['outputArtifacts'][0]['location']['s3Location']['bucketName']).upload_file('/tmp/zip_out.zip', event['CodePipeline.job']['data']['outputArtifacts'][0]['location']['s3Location']['objectKey'], ExtraArgs={
        'ServerSideEncryption': 'aws:kms',
        'SSEKMSKeyId': 'arn:aws:kms:us-east-1:997477333591:key/67b7e822-e9ee-4a40-85c7-6d418864cef4'
    })

    response = client.put_job_success_result(
            jobId=sJobId)

    return response