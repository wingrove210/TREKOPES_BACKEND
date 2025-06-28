from interfaces.storage import Storage
import boto3
from core.config import settings

class S3Storage(Storage):
    def __init__(self):
        self.session = boto3.session.Session()
        self.bucket = "suno-bot"
        self.endpoint = settings.AWS_ENDPOINT_URL
        self.s3 = self.session.client(
            service_name="s3",
            endpoint_url=settings.AWS_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self._bucket_exist()
        
    def _bucket_exist(self):
        try:
            self.s3.head_bucket(Bucket=self.bucket)
        except:
            self.s3.create_bucket(Bucket=self.bucket)
            
    def save(self, filename, file):
        self.s3.put_object(
            Bucket=self.bucket,
            Key=filename,
            Body=file,
            StorageClass="COLD"
        )
    def get(self, filename):
        return f"{self.endpoint}/{self.bucket}/{filename}"