import os
import boto3
# from object_storage import s3
from config import settings


session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)



def save_message(hash_value: str, body: str) -> str:
    """Save and returns url"""
    res = s3.put_object(
        Bucket=settings.BUCKET,
        Key=hash_value+'.txt',
        Body=body   
    )

    print(res)

    mes_url = s3.generate_presigned_url(
        'get_object',
        Params={
            "Bucket":settings.BUCKET,
            "Key": hash_value+ ".txt"
        },
        # Expires_In=3600
    )

    return mes_url


def delete_message(hash_value: str):
    s3.delete_object(
        Bucket=settings.BUCKET,
        Key=hash_value+'.txt',
    )


