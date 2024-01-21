import os
import boto3
from boto3 import client

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_REGION_NAME')
aws_bucket_name = os.getenv('AWS_BUCKET_NAME')
aws_bucket_folder = os.getenv('AWS_BUCKET_FOLDER')

def create_s3_client() -> client:
    client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
    return client

def upload_to_s3(s3_client, file_path):
    file_name = os.path.basename(file_path)

    s3_key = os.path.join(aws_bucket_folder, file_name)

    s3_client.upload_file(file_path, aws_bucket_name, s3_key, ExtraArgs={'ACL': 'public-read'})

    return f"https://{aws_bucket_name}.s3.{region_name}.amazonaws.com/{s3_key}"