import os
import boto3
# from object_storage import s3
from config import settings

class S3Repository():
    def __init__(self) -> None:

        self.session = boto3.session.Session()
        self.client_s3 = self.session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )



    def save_message(self, hash_value: str, body: str) -> str:
        """Save and returns url"""
        res = self.client_s3.put_object(
            Bucket=settings.S3_BUCKET,
            Key=str(hash_value)+'.txt',
            Body=body   
        )


        mes_url = self.client_s3.generate_presigned_url(
            'get_object',
            Params={
                "Bucket":settings.S3_BUCKET,
                "Key": str(hash_value)+'.txt'
            },
            # ExpiresIn=3600
        )

        return mes_url


    def delete_message(self, hash_value: str):
        self.client_s3.delete_object(
            Bucket=settings.S3_BUCKET,
            Key=hash_value+'.txt',
        )




