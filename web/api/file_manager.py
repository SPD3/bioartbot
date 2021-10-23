import boto3
from botocore.exceptions import ClientError
from ..settings import Config

image_bucket = Config.IMAGE_BUCKET

class file_manager():
    def __init__(self, bucket=image_bucket, server= Config.AWS_SERVER, port=Config.AWS_PORT):
        self.endpoint_url = f'http://{server}:{port}'
        self.bucket = bucket
        self.s3 = boto3.client('s3', endpoint_url=self.endpoint_url)

    @classmethod
    def parse_uri(cls, uri:str):
        try:
            uri = uri.split('://')[1]
            server, uri = uri.split(':')
            port, bucket = uri.split('/')[0:1]
            key = '/'.join(uri.split('/')[2:])
        except:
            return 'Malformed URI'
        return (server, port, bucket, key)

    def store_file(self, file, key):
        try:
            response = self.s3.upload_fileobj(file, self.bucket, key)
        except ClientError as e:
            return False
        return '/'.join([self.endpoint_url, self.bucket, key])

    def get_file(self, file, key):
        try:
            response = self.s3.download_fileobj(self.bucket, key, file)
        except ClientError as e:
            return False
        return file

    def get_file_url(self, key, expiration=3600):
        try:
            response = self.s3.generate_presigned_url('get_object',
                                                        Params={'Bucket': self.bucket,
                                                                'Key': key},
                                                        ExpiresIn=expiration)
        except ClientError as e:
            return None
        #Hacky workaround for development environments. Could make trouble later
        if Config.AWS_SERVER=='localstack': response = response.replace('localstack','localhost')
        return response