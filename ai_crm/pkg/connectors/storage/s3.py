"""S3-compatible storage implementation (Yandex Cloud S3)."""

from ai_crm.pkg.connectors.storage.base import BaseStorage
from ai_crm.pkg.logger import logger as logger_lib

logger = logger_lib.get_logger(__name__)


class S3Storage(BaseStorage):
    """S3-compatible storage implementation for Yandex Cloud S3.

    TODO: Implement when migrating to Yandex Cloud S3.
    Will use aioboto3 or similar async S3 client.
    """

    def __init__(
        self,
        bucket_name: str,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
    ):
        self.bucket_name = bucket_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint_url = endpoint_url
        logger.info(f"S3Storage initialized for bucket {bucket_name}")

    async def save_file(self, file_path: str, file_content: bytes) -> str:
        raise NotImplementedError(
            "S3 storage not yet implemented. " "Use LocalStorage for now."
        )

    async def get_file(self, file_path: str) -> bytes:
        raise NotImplementedError(
            "S3 storage not yet implemented. " "Use LocalStorage for now."
        )

    async def delete_file(self, file_path: str) -> bool:
        raise NotImplementedError(
            "S3 storage not yet implemented. " "Use LocalStorage for now."
        )

    async def file_exists(self, file_path: str) -> bool:
        raise NotImplementedError(
            "S3 storage not yet implemented. " "Use LocalStorage for now."
        )

    def get_storage_type(self) -> str:
        return "s3"
