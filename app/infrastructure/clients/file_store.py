from botocore.client import BaseClient
from botocore.config import Config
import boto3

from app.application.ports.ports import FileStorePort

# S3FileStore는 AWS S3에서 PDF 파일을 다운로드하는 구현체입니다.
class S3FileStore(FileStorePort):
    def __init__(
        self,
        bucket: str,
        region: str | None = None,
    ) -> None:
        self.bucket = bucket
        self.client: BaseClient = boto3.client(
            "s3",
            region_name=region,
            config=Config(retries={"max_attempts": 3, "mode": "standard"}),
        )

    def download(self, file_key: str) -> bytes:
        key = file_key
        print("log : downloading file from S3 with key:", key)

        self.client.head_object(Bucket=self.bucket, Key=key)
        response = self.client.get_object(Bucket=self.bucket, Key=key)
        return bytes(response["Body"].read())

    def _build_key(self, file_asset_id: int) -> str:
        filename = f"{file_asset_id}.pdf"
        return filename
